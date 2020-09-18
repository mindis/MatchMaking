

import pandas as pd
from decimal import Decimal
import re


def load_agents():
    '''
    import os
    file_name=os.environ.get('file_name', 'file_name environment variable is not set.')
    agents = pd.read_csv(file_name)
    '''
    agents = pd.read_csv(file_name)
    
    return agents



def match_locations_one(agents, p_user_locations, p_state):
    
    error_flag= False
    error_message= ''
    error_code=''
    
    #agents.loc[ (agents['areaServed'].str.contains(p_user_locations[0], na=False)) &  (agents['state'].str.contains(p_state[0], na=False)), 'location_match'] = 1
    
    agents.loc[ (agents['areaServed'].str.contains(p_user_locations, na=False)) &  (agents['state'].str.contains(p_state, na=False)), 'location_match'] = 1
    
    if agents[ (agents["location_match"] > 0 )].shape[0]<=0:
        error_flag=True
        error_message='No realtor found in input location. Please try a different location.'
        error_code=400
    
    
    return agents, error_flag, error_message,error_code



def match_price(agents, p_min_price, p_max_price, tolerance_per=10):
    
    l_min_price = p_min_price + (p_min_price * tolerance_per)/100
    l_max_price = p_min_price - (p_min_price * tolerance_per)/100

    agents.loc[ (l_min_price >= agents.min_price) & (l_max_price <= agents.max_price), 'price_match'] = 1
    return agents


def validate_input_json(d):
    validation_error = ''
    validation_error_code=400
    validation_flag  = False
    
    # Global Variables
    global g_locations_flag, g_state_flag,g_listing_price_flag
    g_locations_flag, g_state_flag, g_listing_price_flag = False,False,False
    
    global g_locations_value, g_state_value,g_listing_price_value
    g_locations_value, g_state_value, g_listing_price_value='','',0

    for i in d.keys():
        j=i
        i=i.lower()
        
        if 'location' == i:
            g_locations_flag=True
            g_locations_value = d[j]
        elif 'state' == i:
            g_state_flag=True
            g_state_value = d[j]
        elif 'listing_price' == i:
            g_listing_price_flag=True
            g_listing_price_value = d[j]
        else:
            validation_error = "Invalid key found in input: "+ i + "; "
            validation_flag = True
            
        
    ### Validate locations     
    if g_locations_flag is False:
        validation_error= validation_error + 'location key is missing ; '
        validation_flag = True
    else:
        if ( (not isinstance(g_locations_value,str)) ):
            validation_error= validation_error + 'location must be a string ; '
            validation_flag = True
            
        elif len(g_locations_value) < 3:
            validation_error= validation_error + 'location value must be minimum of 3 chars ; '
            validation_flag = True
            
    
     ### Validate state     
    if g_state_flag is False:
        validation_error= validation_error + 'state key is missing ; '
        validation_flag = True   
    else:
        if (not isinstance(g_state_value, str)):
            validation_error= validation_error + 'state must be two char string (code) following UPSC standards; '
            validation_flag = True
        elif (len(g_state_value)!=2):
            validation_error= validation_error + 'state must be two char string (code) following UPSC standards; '
            validation_flag = True
    
    ### Validate price (listing_price for in-house and min & max price for partners/clienta)     
    if (g_listing_price_flag is False):
        validation_error= validation_error + 'listing_price is missing ; '
        validation_flag = True
    elif ( (not isinstance(g_listing_price_value,int)) & (not isinstance(g_listing_price_value,float))):
        validation_error= validation_error + 'listing_price must be an integer ; '
        validation_flag = True
            
    return validation_error, validation_flag, validation_error_code



def find_realtor_v3(request):
   
    
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        '''
        Step 1 - Validate Incoming json 
        '''
        error_message, error_flag, error_code =validate_input_json(request_json)
        
        if error_flag is True:
            error={'error_message':[error_message],'error_code':[error_code]}
            return pd.DataFrame(data=error).to_json(orient="records")
            
        else:
             
            '''
            load agents data to search from
            '''
            agents=load_agents()
            
            
            '''
            Step 2 - Locations Logic
            '''
            
            l_locations_value = g_locations_value.replace('-',' ').lower().replace('city','').strip()
            l_locations_value = re.sub(r'^(st.|st|\$t|\$t.)\s', r'saint ',l_locations_value, flags=re.IGNORECASE) # matches st,st.,$st at the beg to saint
            l_locations_value = re.sub(r'\s(st.|st|\$t|\$t.)$', r' street',l_locations_value, flags=re.IGNORECASE)# matches st.. in the end to street
            l_locations_value = re.sub('[ \t]+', ' ', l_locations_value) # removes extra space in between 2/3 grams
            
            #j_user_locations.append(l_locations_value)
    		
            #j_user_states.append(g_state_value.strip().upper())
            
            #agents,error_flag,error_message,error_code= match_locations_one(agents, j_user_locations, j_user_states,g_state_flag)
            
            agents,error_flag,error_message,error_code= match_locations_one(agents, l_locations_value, g_state_value.strip().upper())
             
            if error_flag is True:
                error={'error_message':[error_message],'error_code':[error_code]}
                return pd.DataFrame(data=error).to_json(orient="records")
            
            agents=match_price(agents, int(g_listing_price_value), int(g_listing_price_value),20)
            
            
            agents['price_match'].fillna(0,inplace=True)
            #agents['score'] = agents.location_match + agents.price_match * .60
            
            
            
            result = agents.nlargest(2,['price_match','properties_count'],keep='first')[{"agent_name","agent_phone","agent_email"}]
            #result.replace(0,'',inplace=True)
            result_json= result.to_json(orient='records')
            
            return result_json


