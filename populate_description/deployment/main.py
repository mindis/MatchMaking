

import random
import time
import pandas as pd
import numpy as np




## AGENT

def get_agent(p_ag_name, p_phone):
    p_phone   = str(p_phone)
    p_ag_name = str(p_ag_name)

    if len(p_phone) > 1: phone_list = random.choice( (',ph '+ p_phone, 'at '+ p_phone, '( phone '+ p_phone+')')) 
    else: phone_list=''

    if len(p_ag_name)<=1: p_ag_name = 'agent'

    #ag_seperator = ('-','!','--','!!','***','**','*')

    ag_begin = ( 'Please contact', 
                 'Please request',
                 'Please speak with',
                 'For questions, please contact',
                 'Contact',
                 'Please communicate with',
                 'Reach out to',
                 'Get hold of',
                 'Touch base with',
                 'Please meet',
                 'Please call',
                 'Don\'t wait! Call',
                 'Call',
                 'Text',
                 'Please call, text or email',
                 'Consider calling',
                 'Make a request to',
                 'This one won\'t last long so be sure to reach out to',
                ' You are invited to explore the purchase of your new home by contacting',
                )

    ag_middle = ('agent',
                 'agent',
                'realtor',
                'responsible person',
                'Agent',
                'listing agent',
                'broker',
                'us',
                p_ag_name,
                p_ag_name)



    ag_end =(phone_list+'!', 
             'for appointment '+phone_list+'.',
             'for visit!', 
             'to visit property '+phone_list+'.', 
             'for showing!', 
             'for showing on this one!',
             'for showing appointments.',
             'for all showing requests '+phone_list+'.',
             'asap!!',
             'at the earliest!', 
             'to schedule a showing.',
             'for more details!', 
             'for details!',
             'for access!',
             'to see property '+p_phone+'.',
             'for showing times ' +phone_list+'.',
             'for all property questions!',
             'for inquiries!!',
             'for further queries.',
             'for queries!',
             'for private viewing!',
             'today before this gem gets away.',
             'for booking visits!',
             'for booking appointments!',
             'for booking property visit.',
             'for more information.',
             'for more information, but don\'t wait too long or someone else will be enjoying this spectacular offering.',
             'for more details and to arrange your private viewing.',
             'to arrange for your personal viewing of this rare offering.',
             'to arrange your personal viewing before this one is gone.',
             'for detailed list of features and finishes.',
             'for your personal viewing right away!',
             'to find out how you can own this home!',
             'to book your appointment to view !!',
            )




    #num = random.randrange(0,5)
    #print (nouns[num] + ' ' + verbs[num] + ' ' + adv[num] + ' ' + adj[num])

    ag_sentence=''
    ag_sentence=  (random.choice(ag_begin) + ' ' + random.choice(ag_middle)+ ' ' + random.choice(ag_end))

    #combinations=0
    #combinations = combinations + len(ag_begin)*len(ag_middle)*len(ag_end)
    #print(combinations)

    return ag_sentence


# In[22]:


# SQFT

def get_sqft(p_sqft):
    
    if ( (p_sqft==None) | (p_sqft=='') | (p_sqft==0) ): 
        
        return ''

        '''
        the large 9,432 sq.ft.

        this spacious 4/3

        'Mansion',

        two generous sized bedrooms 
        spaciuous bedrooms


        '''
    else:
        
        sqft_sentence=''

        sqft_list= ('Measuring approximately '+str(p_sqft)+' sq ft!',
                    'Sized at '+str(p_sqft)+' sq ft!',
                    'Features over '+str(p_sqft)+' sq ft!',
                    'Size is '+str(p_sqft)+' sq ft!',
                    'Area is '+str(p_sqft)+' sq ft!',
                   )

        sqft_sentence=  ( random.choice(sqft_list))



        #combinations = combinations + len(sqft_list)

        return sqft_sentence


# In[23]:


# LOCATION

def get_location(p_sqft,
             p_location,
             p_address_street,
             p_property_type='house',
             p_property_sub_type='house'
            ):
    

    if ( (p_property_type.upper()=='OTHER') | (p_property_type==None) | (p_property_type=='')): p_property_type='house'

    if ( (p_property_sub_type.upper()=='OTHER') |(p_property_sub_type==None) | (p_property_sub_type=='')): p_property_sub_type=p_property_type

    loc_begin = ('Excellent', 'This is an excellent', 'One of the excellent', 'What an excellent',
                 'Great', 
                 'Impressive',
                 'Remarkable',
                 'Marvelous', 
                 'Beautiful', 
                 'Nice', 
                 'Super Nice',
                 'Very-Nice',
                 'Efficient',
                 'Gorgeous',
                 'A unique',
                 'Fantastic',
                 'Wonderful',
                 'Terrific',
                 'Grand',
                 'Well maintained',
                 'Charming',
                 'Immaculate',
                 'Experience the',
                 'Peace and privacy abound at this impeccably maintained', 
                 'Elegant','This is an elegant',
                 '',
                 'A meticulously maintained',
                 'A meticulously kept',
                 'Lovely and bright',
                 'Gorgeous looking',
                 'Best Buy',
                 'Vaow! What a great',
                 'Majestic', 'What a majestic',
                 'Well built', 'This is a well-built',
                 'Looking for your new home, look nowhere else. This is an excelent',
                 'Still searching for a new home to call your own, well this could be it! This stunning',
                 'Must see',
                 'Sophisticated',
                 'Contemporary',
                 'Come check out this gem',
                 'Open the doors to this fabulous',
                 'Looking for the WOW factor? words and pictures cannot describe this gorgeous and immaculate',
                 'Welcome to highly desired',
                 'Welcome to another exciting project',
                 'Consider this premier',
                 'Eye-pleasing',
                 'One of a kind iconic',
                 'Visit this paradise',
                 'Discover the beauty of this',
                 'Unbelievable opportunity to own a',
                 'Absolutely stunning! this spectacular century',
                 'Prepare to fall in love with this',
                 'Own a',
                 'Your dream',
                 'Absolutely gorgeous',
                )





    #unique home with tremendous rental potential. use it as a family compound
    if ( (p_sqft <= 2000) & (p_sqft > 1500)):
        l_size = random.choice(('medium sized ', 'descent sized ','','',''))

    elif p_sqft > 2000:
        l_size = random.choice(('large ', 'spacious ','big ','huge ','','',''))

        #'has plenty of space for a growing family'

    else:
        l_size=''


    loc_middle  = ('home',
                   'home',
                   'house',
                   'house',
                   'household',
                   'listing',
                   'property',
                   'property',
                   'dwelling',
                   'residence',
                  # p_property_sub_type, 
                  # p_property_type
                   )



    loc_end   = ('located in '+p_location,
                 'located in '+p_location,
                 'located at '+p_address_street,
                 'located at '+p_address_street,
                 'located in a thriving locality',
                 'located in an exceptional neighborhood',
                 'currently located in a popular vicinity',
                 'perfectly located in '+p_location,
                 'located in a quiet neighborhood in the heart of '+p_location,
                 'with perfect location',
                 'thoughtfully located in '+p_location, 
                 'thoughtfully located in '+p_location, 
                 'thoughtfully located at '+p_address_street, 
                 'thoughtfully located at '+p_address_street, 
                 'conveniently located in '+p_location,
                 'conveniently located at '+p_address_street,
                 'situated in '+p_location,
                 'situated at '+p_address_street,
                 'placed in popular vicinity',
                 'nestled in '+p_location, 
                 'situated in one of the most desirable locations',
                 'situated on a desirable street',
                 'in an established area',
                 'in a great location',
                 'in a nice location',
                 'thoughtfully-oriented in '+p_location
                ) 
#' awaiting to be your home.',
                 

    loc_extra = (' offering a respite from the daily grind.',  ## offering
                 ' makes it welcoming.',
                 ' awaits your enjoyment.',
                 ' offering a magestic view.',
                 ' waiting for its new owner to enjoy and love.',
                 ' having a nice view.',
                 ' having tremendous potential.',
                 '. Opportunity To Build Your Dream Home.',
                 '. This house has it all!!',  
                 '. Won\'t last long! so hurry up.',
                 '. Put your feet up in your new beautiful home!',
                 '. Owner have meticulously cared for this beauty.',
                 '. Enjoy the peace of living.',
                 '. Don\'t let this pristine home get away!',  
                 '. Hurry on this one and make it your own!',
                 '. Such a great home to start living!',
                 '. Wait there is more!',
                 '. please remember to take the tour!',
                 '. A truly warm & wonderful home!',  
                 '. Check out nice looking photos!',
                 '. Various amenities!',
                 '. This home will satisfy the most discerning of buyers!',
                 '. Click on the photos to see a birds eye view.',
                 '. This property is truly a one-of-a-kind.',
                 '. Have your family come and enjoy the beautiful views.',
                 '. Don\'t miss out on this opportunity to own your piece of paradise.',
                 '. Truly amazing home! don\'t miss it!',
                 '. The combination of location, amenities, and pricing provides unmatched value.',
                 '. A definite must see!',
                 '. A must see property!',
                 '. Well worth a look!',
                 '. One has to visit this property to truly see the features of this prime real estate.',
                 '. Once in a lifetime opportunity!!',
                 '. A dream come true for the discerning buyer looking for a special home!',
                 '. The view speaks for itself and will capture your heart and imagination!',
                 '. This one is sure to check off all those boxes on your wish list.',
                 '. Come see what this lovely area has to offer.',
                 '. This is the one you have been waiting for!',
                 '. This home is priced to sell!',
                 '. Visit to see for yourself all it has to offer',
                 '. Come see this amazing home!',
                 '. This is a truly unique opportunity!',
                 '. This home is a must to be viewed!!',
                 '. This is a home truly built to excite!',
                 '. This is an Estate not-to-be missed!',
                 '. A very rare opportunity for someone looking for a well-appointed home.',
                 '. A place to call HOME!!',
                 '. ',
                 '. ',
                 '. ')


    loc_sentence=''
    loc_sentence=  ( random.choice(loc_begin) + ' ' + l_size +random.choice(loc_middle)+ ' ' + random.choice(loc_end) + random.choice(loc_extra))

   
   # combinations = combinations + len(loc_begin)*len(loc_middle)*len(loc_end)*len(loc_extra)
    #combinations
    
    return loc_sentence


# In[24]:


# BEDS
def get_beds(p_beds,p_baths=0):

    import inflect
    
    p = inflect.engine()
    l_beds_words  = p.number_to_words(p_beds)
    l_baths_words = p.number_to_words(p_baths)


    #del str
    l_str_beds =str(p_beds)
    l_str_baths=str(p_baths)



    beds_sentence=''
    
    beds_list= ('Bedroom '+ l_str_beds+'!',
                'Bedroom '+ l_beds_words+'!',
                'Fantastic '+l_beds_words+' '+ 'Bedroom!',
                'Fantastic '+ l_str_beds +' '+ 'Bedroom!',
                'Lovely '+l_beds_words+' '+ 'Bedroom!',
                'Lovely '+ l_str_beds +' '+ 'Bedroom!',
                 l_str_beds +' '+ 'beds!',
                 l_beds_words +' '+ 'beds!',
                'This fabulous house offers '+l_str_beds +' '+ 'beds!',
                'Number of Bedroom:'+ l_str_beds+'!',
                'Number of Bedroom:'+ l_beds_words+'!',
                'Num. of Bedroom:'+ l_str_beds+'!',
                'Num. of Bedroom:'+ l_beds_words+'!',
                'Offers '+l_str_beds+' Bedroom!',
                'Offers '+l_beds_words+' Bedroom!',
                'Has '+l_beds_words+' Bedroom!',
                'Has '+l_str_beds+' Bedroom!',
                'Having '+l_beds_words+' Bedroom!',
                'Having '+l_str_beds+' Bedroom!',
                'Features '+l_str_beds+' Bedroom!',
                'Features '+l_beds_words+' Bedroom!',
                'There are '+l_str_beds+' Bedroom!',
                'There are '+l_beds_words+' Bedroom!',
                'This beauty of a home has '+l_str_beds +' '+ 'beds!',
                'The home offers '+l_str_beds +' '+ 'beds!',
                
               )

    if p_baths > 0:

        baths_list= ('Bathroom '+l_str_baths+'!',
                     'Bathroom '+l_baths_words+'!',
                      l_baths_words +' '+ 'baths!!',
                      l_str_baths +' '+ 'baths!!',
                      l_baths_words +' '+ 'baths!!',
                      l_str_baths +' '+ 'baths!!',
                      l_str_baths +' '+ 'baths!',
                      l_baths_words +' '+ 'baths!!',
                      l_str_baths +' '+ 'baths!!',
                      l_str_baths +' '+ 'baths!!',
                     'Bathroom:'+ l_baths_words+'!',
                     'Bathroom:'+ l_str_baths+'!',
                     'Bathroom:'+ l_baths_words+'!',
                     'Bathroom:'+ l_str_baths+'!!',
                      l_baths_words+' Bathroom!',
                      l_baths_words+' Bathroom!',
                      l_str_baths+' Bathroom!',
                      l_baths_words+' Bathroom!',
                      l_str_baths+' Bathroom!',
                      l_str_baths+' Bathroom!!',
                      l_baths_words+' Bathroom!!',
                      l_str_baths+' Bathroom!!',
                      l_baths_words+' Bathroom!!',
                      l_str_baths+' Bathroom!!',
                      l_str_baths+' Bathroom!!'
                     )



        new=[]
        for i in range(len(beds_list)):
            new.append( beds_list[i][0:-1] + ' '+random.choice(('and','and','&','&','and',',','plus'))+' ' + baths_list[i] )

        beds_list=new    


    beds_sentence=  ( random.choice(beds_list))

    
    #combinations = combinations + len(beds_list)
    #combinations
    
    return beds_sentence
    
    #beds_list


# In[25]:


# POOL
def get_pool():

    pool_sentence ='' 

    pool_list = ('lets not forget the pool which enhances the experience and comfort.',
                 'Just relax in your own resort style pool.',
                 'Just relax in the pool.',
                 'You will be duly impressed with the pool.',
                 'Has a pool!',
                 'Features a pool as well!',
                 'You will greatly appreciate the swimming pool!',
                 'You will greatly adore the pool!',
                 'A Pool adds value to your home!',
                 'Pool will make you want to dive right in!',
                 'Take a dip in the pool!',
                 'This house has a pool!',
                 'Presence of a pool increases attraction!',
                 'Enjoy the pool!',
                 'Enjoy the fantastic pool!',
                 'Has a pool for summer entertainment!',
                 'Get amazed by the pool!',
                 'Pool will surely grab your attention.'
                 
                )

    pool_sentence=  ( random.choice(pool_list))

    #combinations = combinations + len(pool_list)
    #combinations

    return pool_sentence


# In[26]:


# FIREPLACE
def get_fireplace():


    fire_sentence ='' 

    fire_list = ('Has a fireplace for the cool winter nights.',
                 'It has a fireplace.',
                 'Fireplace is available.',
                 'Has a cozy Fireplace!',
                 'Has a cozy Fireplace!',
                 'Fireplace is there!',
                 'Fireplace is present!',
                 'The fireplace enhances the ambiance in the winter.',
                 'Fireplace raises your experience whether you are relaxing or entertaining.',
                 'Comes with a cozy fireplace.',
                 'Lets not forget the cozy fireplace.',
                 'As the days get cooler, enjoy the fireplace!',
                 'Artfully designed fireplace!',
                 'Fireplace for those chilly fall and winter evenings.',
                 'Fireplace for those cooler evenings.',
                 'Fireplace for those cooler evenings.',
                 'Fireplace for chilly nights.',
                 'Enjoy the relaxing ambiance with Fireplace!',
                 'Sit cozy by the flames of the fireplace.',
                 'Enjoy the warmth of the fireplace during cold winter nights!',
                 'It also features a fireplace!',
                 'Comes with a fireplace!',
                 'Fireplace enhances your experience!'
                 )

    fire_sentence=  ( random.choice(fire_list))

    #combinations = combinations + len(fire_list)
    #combinations
    
    return fire_sentence


# In[27]:


# Parking

parking_list = ('Room for parking available in ',
               )


# UTILITIES
def get_utilities(p_utilities):

    utilities_sentence=''

    utilities_list= ('Some of the features included are:',
                     'Features are:',
                     'Inclusions are:',
                     'Utilities Include:',
                     'Utilities Include:',
                     'Nice list of utilities included:',
                     'Utilites -',
                     'Characteristics -',
                     'Attributes are :',
                     'Some of the features are:',
                     'This impressive home has',
                     'The main house features:',
                     'Amenities include',
                     'Many extra features including',   
                     'This exquisite home features',
                     'Just a few of the many features include',
                     'Separate utilities',
                     'Property consists of',
                   )

    utilities_sentence=  ( random.choice(utilities_list))

    utilities_sentence = utilities_sentence + ' ' + str(p_utilities)+ '.'
    utilities_sentence


    #combinations = combinations + len(utilities_list)
    #combinations

    return utilities_sentence


# In[28]:


# YEAR-BUILT

def get_year_built(p_year_built, p_old):

    year_built_list=('Immaculate new construction!',
                     'Newly constructed!',
                     'Newly built!',
                     'Recently constructed!',
                     'Recently constructed!',
                     'Built in '+ str(p_year_built)+'!',
                     'This home is only '+str(p_old)+' years old!',
                     'Pleasantly new!',
                     'Brand new property!',
                     'New quality construction!'
                    )


    year_built_sentence=  ( random.choice(year_built_list))



    #combinations = combinations + len(year_built_list)
    #combinations
    return year_built_sentence


# In[32]:


def get_waterfront():

    waterfront_sentence ='' 

    waterfront_list = ('Has a Waterfront.',
                       'Opens on a Waterfront.',
                       'Opens on a Waterfront.',
                       'It has a Waterfront.',
                       'The Waterfront enhances the ambiance.',
                       'The Waterfront enhances the experience.',
                       'Incredible high bank waterfront views.',
                       'This property is set by a serene waterfront.',
                       'Miles of scenic waterfront to enjoy.',
                       'Amaing Waterfront!',
                       'Enjoy stunning waterfront view!',
                       'Enjoy spectacular waterfront view!',
                       'Amazing waterfront living at its best where the scenery is constantly changing!',
                       'Mere steps to waterfront trail!',
                       'The waterfront is suitable for folks of all ages!',
                       'Year round waterfront home!',
                       'Offers incredible waterfront view!',
                       'Offers stunning waterfront view!',
                       'Scenic waterfront view!',
                       'Hardly any other waterfront property like this avaiable in the market.',
                       'If you are looking for a beautiful waterfront property in the city this is your chance!',
                       'Rare opportunity to own waterfront property!',
                       'Waterfront trails!',
                       'Offers waterfront!',
                       'Enjoy the amazing view of the waterfront',
                       'Situated on a waterfront community',
                       'Waterfront living at its finest!',
                       'It has an excellent view of waterfront!',
                       'Comes with a Waterfront!'
                     )


    waterfront_sentence=  ( random.choice(waterfront_list))

    #combinations = combinations + len(waterfront_list)
    #combinations
    
    return waterfront_sentence



def validate_input_json(d):
    validation_error = ''
    validation_error_code=400
    validation_flag  = False
    
    '''
    data={
    "agent_phone":"12344", \
    "agent_name":"Charles J.", \
    "property_type":"property_type", \
    "property_sub_type":"sub_type", \
    "utilities":"Dishwasher, Dryer",\
    "year_built":"2018", \
    "beds":"2", \
    "baths":"2", \
    "location":"Denver", \
    "address_street":"1184 Audobon Dr.",\
    "fireplace":"T",\
    "waterfront":"T",\
    "pool":"T",\
    "sqft":"1200", \
    "deck":"T", \
    "porch":"T", \
    "patio":"T", \
    "ceiling_fan":'T', \
    "security_system":"T", \
    "vaulted_ceiling":"T",\
    "garden":"T", \
    "basement":"T"}
    
    '''
    
    
    # Global Variables Values
    global g_agent_phone_val,  g_agent_name_val,  g_property_type_val,  g_property_sub_type_val,  g_utilities_val,      g_year_built_val, g_beds_val, g_baths_val,  g_city_val,  g_address_street_val,  g_fireplace_val,     g_waterfront_val,  g_pool_val,  g_sqft_val,  g_deck_val, g_porch_val, g_patio_val,  g_ceiling_fan_val,     g_security_system_val,  g_vaulted_ceiling_val,  g_garden_val,  g_basement_val, g_user_id_val,g_parking_types_val,    g_rooms_val, g_building_utilities_val
    
     # Global Variables Flags
    global g_agent_phone_flag,  g_agent_name_flag,  g_property_type_flag,  g_property_sub_type_flag,  g_utilities_flag,      g_year_built_flag, g_beds_flag, g_baths_flag,  g_city_flag, g_address_street_flag,  g_fireplace_flag,     g_waterfront_flag,  g_pool_flag,  g_sqft_flag,  g_deck_flag, g_porch_flag, g_patio_flag,  g_ceiling_fan_flag,     g_security_system_flag,  g_vaulted_ceiling_flag,  g_garden_flag,  g_basement_flag,g_user_id_flag,g_user_key_flag,    g_parking_types_flag,g_rooms_flag, g_building_utilities_flag
    
    
    #Default Values
    g_agent_phone_val,  g_agent_name_val,  g_property_type_val,  g_property_sub_type_val,  g_utilities_val,      g_year_built_val, g_beds_val, g_baths_val,  g_city_val, g_address_street_val,  g_fireplace_val,     g_waterfront_val,  g_pool_val,  g_sqft_val,  g_deck_val, g_porch_val, g_patio_val,  g_ceiling_fan_val,     g_security_system_val,  g_vaulted_ceiling_val,  g_garden_val,  g_basement_val,g_user_id_val,g_parking_types_val,    g_rooms_val,g_building_utilities_val='','','','','','','','','','','','','','','','','','','','','','','','','',''
   
    #Default Values
    g_agent_phone_flag,  g_agent_name_flag,  g_property_type_flag,  g_property_sub_type_flag,  g_utilities_flag,      g_year_built_flag, g_beds_flag, g_baths_flag,  g_city_flag, g_address_street_flag,  g_fireplace_flag,     g_waterfront_flag,  g_pool_flag,  g_sqft_flag,  g_deck_flag, g_porch_flag, g_patio_flag,  g_ceiling_fan_flag,     g_security_system_flag,  g_vaulted_ceiling_flag,  g_garden_flag,  g_basement_flag,g_user_id_flag,     g_user_key_flag,g_parking_types_flag,g_rooms_flag, g_building_utilities_flag =     False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,    False,False,False,False,False,False, False, False, False, False
    
    for i in d.keys():
        j=i
        i=i.lower()
        
        if 'user_id' ==i:
            g_user_id_flag=True
            g_user_id_val = d[j]
        elif 'user_key' == i:
            g_user_key_flag=True
            g_user_key_val = d[j]
            
        elif  'agent_phone' == i:
            g_agent_phone_flag = True
            g_agent_phone_val  = d[j]
            
        elif 'agent_name' == i:
            g_agent_name_flag=True
            g_agent_name_val = d[j]
            
        elif 'property_type' == i:
            g_property_type_flag  = True
            g_property_type_val = d[j]
            
        elif 'property_sub_type' == i:
            g_property_sub_type_flag  = True
            g_property_sub_type_val   = d[j]
        
        elif 'utilities' == i:
            g_utilities_flag=True
            g_utilities_val = d[j]
            print(type(g_utilities_val))
        
        elif 'year_built' == i:
            g_year_built_flag = True
            g_year_built_val  = d[j]
        
        elif 'beds' == i:
            g_beds_flag=True  
            g_beds_val = d[j]
        
        elif 'baths' == i:
            g_baths_flag=True 
            g_baths_val = d[j]
        
        elif 'city' == i:
            g_city_flag=True 
            g_city_val = d[j]
        
        elif 'address_street' == i:
            g_address_street_flag=True 
            g_address_street_val = d[j]
   
   
        elif 'has_fireplace' == i:
            g_fireplace_flag=True 
            g_fireplace_val = d[j]
   
        elif 'has_waterfront' == i:
            g_waterfront_flag=True 
            g_waterfront_val = d[j]
   
        elif 'has_pool' == i:
            g_pool_flag=True 
            g_pool_val = d[j]
   
        elif 'total_sqft' == i:
            g_sqft_flag=True 
            g_sqft_val = d[j]
   
        elif 'has_deck' == i:
            g_deck_flag=True 
            g_deck_val = d[j]
   
        elif 'has_porch' == i:
            g_porch_flag=True 
            g_porch_val = d[j]
   
        elif 'has_patio' == i:
            g_patio_flag=True 
            g_patio_val = d[j]
   
        elif 'has_ceiling_fan' == i:
            g_ceiling_fan_flag=True 
            g_ceiling_fan_val = d[j]
   
        elif 'has_security_system' == i:
            g_security_system_flag=True 
            g_security_system_val = d[j]
   
        elif 'has_vaulted_ceiling' == i:
            g_vaulted_ceiling_flag=True 
            g_vaulted_ceiling_val = d[j]
    
        elif 'has_garden' == i:
            g_garden_flag=True 
            g_garden_val = d[j]
         
        elif 'has_basement' == i:
            g_basement_flag=True 
            g_basement_val = d[j]
   
        elif 'parking_types' == i:
            g_parking_types_flag = True 
            g_parking_types_val =  d[j]
            
        elif 'rooms' == i:
            g_rooms_flag = True 
            g_rooms_val =  d[j]
   
        elif 'building_utilities' == i:
            g_building_utilities_flag = True 
            g_building_utilities_val  =  d[j]

        else:
            validation_error = "Invalid key found in input: "+ i + " "
            validation_flag = True
            
            
            
    '''        
    if ( (g_user_id_flag is False) | (g_user_key_flag is False)):
        validation_error = 'User_Id and (or) User_Key is missing'
        validation_flag = True
        return validation_error, validation_flag,validation_error_code
    else:
        #authenticate = pd.read_json('gs://nest-agents/authentication.json',orient='columns')
        authenticate = pd.read_json('authentication.json',orient='columns')
        if (( authenticate['userid'].where( (authenticate['userid'] == g_user_id_val) & (authenticate['userkey'] == g_user_key_val))
           ).dropna().shape[0]
           ) == 0:
            validation_error = 'Invalid User_Id and (or) User_Key - Access denied! '
            validation_flag = True
            validation_error_code='401'
            return validation_error, validation_flag,validation_error_code
        
    '''
    if ( (g_city_flag is False) | (len(str(g_city_val))<=1 ) ):
        validation_error= validation_error + 'city must be atleast 3 character long ; '
        validation_flag = True
    
    if g_address_street_flag is False:
        validation_error= validation_error + 'address street cannot be null ; '
        validation_flag = True
        
            
    return validation_error, validation_flag, validation_error_code


# In[322]:


def populate_description(request):
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
    
    
    #if 1==1:
        
        #request_json = request
        
        error_message, error_flag, error_code = validate_input_json(request_json)
        
        if error_flag is True:
            error={'error_message':[error_message],'error_code':[error_code]}
            return pd.DataFrame(data=error).to_json(orient="records")
        

        # If a featurs is not present in a property or having null value then do not send the feature or send it as empty string (i.e '')
        # No key found for a particular feature is assumed as not available or missing or empty.

       

        ## START SENTENCE

        start_sentence=''
        start_array=[]
        start_cnt=0
        
        
        # Get sqft
        
        if g_sqft_flag is True:
            try:
                l_sqft =int(float(g_sqft_val))
            except ValueError:
                l_sqft=0
        else:
            l_sqft=0
            
            
        # Get Location
        g_loc_sentence= get_location(l_sqft,g_city_val,g_address_street_val,g_property_type_val,g_property_sub_type_val)
        start_array.append(g_loc_sentence)
        
           # Get year built 
        if (g_year_built_flag is True):
            
            try:
                l_year_built_val =int(float(g_year_built_val))
                
            except ValueError:
                l_year_built_val=0

            l_old = int(time.strftime("%Y")) - l_year_built_val

            if l_old <=5:
                g_year_built_sentence = get_year_built(l_year_built_val, l_old)
                start_array.append(g_year_built_sentence)
                start_cnt+=1

      
        
        start_items=[]
        for i in range(start_cnt+1):
            start_items.append(i)

        random.shuffle(start_items)


        for i in range(start_cnt+1):
            start_sentence+= ( start_array[start_items[i]] + ' ')




        # MIDDLE SENTENCE

        middle_sentence=''
        middle_array=[]
        middle_cnt=-1
        
        
        # Get utilities 
        if (g_utilities_flag is True):
            
            l_utilities = str(g_utilities_val).strip()
            
            if len(l_utilities)>3:
                g_utilities_sentence = get_utilities(l_utilities)
                middle_array.append(g_utilities_sentence)
                middle_cnt+=1

        
        

        if g_beds_flag is True:
            
            # Get Beds and Baths
            if (  (not isinstance(g_beds_val, (int))) ):
                if ( (len(str(g_beds_val).strip())==0) | (g_beds_val==None) ):
                    l_beds_val=0
                else:
                    try:
                        l_beds_val = int(float(g_beds_val))
                    except ValueError:
                        l_beds_val=0
            else:
                l_beds_val = g_beds_val

            if (  (not isinstance(g_baths_val, (int))) ):
                if ( (len(str(g_baths_val).strip())==0) | (g_baths_val==None)  ):
                    l_baths_val=0
                else:
                    try:
                        l_baths_val = int(float(g_baths_val))
                    except ValueError:
                        l_baths_val=0
            else:
                l_baths_val = g_baths_val
                

            if ( (l_beds_val > 0) & (l_beds_val < 8) ):
                g_beds_sentence=get_beds(l_beds_val,l_baths_val)
                middle_array.append(g_beds_sentence)
                middle_cnt+=1

                
                
        # Get Fireplace
        if ( (g_fireplace_flag is True) & (g_fireplace_val.upper() == 'T') ):
            g_fire_sentence=get_fireplace()
            middle_array.append(g_fire_sentence)
            middle_cnt+=1

        # Get Waterfront
        if ( (g_waterfront_flag is True) & (g_waterfront_val.upper() == 'T') ):
            g_waterfront_sentence=get_waterfront()
            middle_array.append(g_waterfront_sentence)
            middle_cnt+=1

        # Get Pool
        if ( (g_pool_flag is True) & (g_pool_val.upper() == 'T') ):
            g_pool_sentence=get_pool()
            middle_array.append(g_pool_sentence)
            middle_cnt+=1
        
        if ( (g_parking_types_flag is True) & (len(str(g_parking_types_val))> 3) ): 
            g_parking_types_sentence = 'Parking Availability: '+ g_parking_types_val+'.'
            middle_array.append(g_parking_types_sentence)
            middle_cnt+=1
        
        '''
        # Remove Rooms
        if ( (g_rooms_flag is True) & (len(str(g_rooms_val))> 3) ): 
            g_rooms_sentence = 'Rooms: '+ g_rooms_val+'.'
            middle_array.append(g_rooms_sentence)
            middle_cnt+=1
        '''
            
        if l_sqft > 0:
            g_sqft_sentence=get_sqft(l_sqft)
            middle_array.append(g_sqft_sentence)
            middle_cnt+=1
            
            
        if ( (g_building_utilities_flag is True) & (len(str(g_building_utilities_val))> 3) ): 
            g_building__sentence = 'Building Utilities Include: '+ g_building_utilities_val+'.'
            middle_array.append(g_building__sentence)
            middle_cnt+=1
               


        middle_items=[]
        for i in range(middle_cnt+1):
            middle_items.append(i)

        random.shuffle(middle_items)


        for i in range(middle_cnt+1):
            middle_sentence+= ( middle_array[middle_items[i]] + ' ')
        
        
       
        # CHECK ADDITIONAL FEATURES
        
        flag=False
        additional_features=''
        deck_list = ('Deck',
                    'Deck with a great view to enjoy the evenings',
                    'Deck to enjoy beautiful view',
                    'Deck with a great view',
                    'Deck having a nice view',
                    )

        if ( (g_deck_flag is True) & (g_deck_val.upper()   == 'T')): additional_features=additional_features + ' '+random.choice(deck_list)+',' ; flag= True 
        if ( (g_porch_flag is True) & (g_porch_val.upper() == 'T')): additional_features=additional_features + ' Porch,'; flag= True 
        if ( (g_patio_flag is True) & (g_patio_val.upper() == 'T')): additional_features=additional_features + ' Patio,'; flag= True 
        if ( (g_ceiling_fan_flag is True) & (g_ceiling_fan_val.upper() == 'T')): additional_features=additional_features + ' Ceiling Fan,'; flag= True 
        if ( (g_security_system_flag is True) & (g_security_system_val.upper() == 'T')): additional_features=additional_features + ' Security System Installed,'; flag= True 
        if ( (g_vaulted_ceiling_flag is True) & (g_vaulted_ceiling_val.upper() == 'T')): additional_features=additional_features + ' Vaulted Ceiling,'; flag= True 
        if ( (g_garden_flag is True) & (g_garden_val.upper() == 'T')): additional_features=additional_features + ' Garden,'; flag= True 
        if ( (g_basement_flag is True) & (g_basement_val.upper() == 'T')): additional_features=additional_features + ' Basement,'; flag= True 

        if (flag is True):
            additional_features=random.choice( ('Has a','Additional features are','Also has a','The house has','Also has a',
                                                   'This home also provides a')
                                                 ) +' '+ additional_features[1:-1] + '! '        


        # Get Agent

        ag_sentence =get_agent(g_agent_name_val,g_agent_phone_val)


        # FINAL SENTENCE
        final_sentence = start_sentence + middle_sentence + additional_features + ag_sentence
        
        #desc_json = {"description":final_sentence}
        #return json.dumps(desc_json)
        
        desc_json={'description':[final_sentence]}
        return pd.DataFrame(data=desc_json).to_json(orient="records")
        
        #return desc_json.to_json()

