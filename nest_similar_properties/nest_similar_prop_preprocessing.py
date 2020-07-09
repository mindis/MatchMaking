from pyspark.sql import SQLContext,functions as F
import sys
import logging


def get_images(df):


	try:
		tmp_images = df.withColumn("images", F.explode("images")) \
		                	.groupBy("_id").count()

		df_images=df.join(tmp_images, '_id','left') \
		            		.withColumnRenamed("count", "images_count") \
		            		.drop("images")

	except Exception as e:
		#print("Error in get_images() function  -  "+  str(e))
		logging.exception("EXCEPTION -  get_images() function")
		raise e   
    
	return df_images  		
	



def get_utilities(df):

	#counting total no of utilities			
	try:

		df_ca_f2 = df.withColumn("utilities",F.split(F.regexp_replace("utilities", r"(^\[)|(\]$)|(')", ""), ", "))
		df1 = df_ca_f2.withColumn("utilities_array",F.explode("utilities")).groupBy("_id").count()
		df_utilities=df_ca_f2.join(df1, '_id','outer').withColumnRenamed("count", "utilities_count")
	except Exception as e:
		#print("Error in get_utilities() function  -  "+  str(e))
		logging.exception("EXCEPTION -  get_utilities() function")
		raise e   
    
	return df_utilities  		
	    		


def preprocessing(df,sqlContext):


	try:
		'''
		drop_features=  ["has_pond", #100
							"has_dock",
							"foreclosure",              
							"is_wired",                 
							"has_barbecue_area",        
							"is_new_construction",      
							"intercom",                 
							"heating_systems",          
							"heating_fuels",            
							"has_wet_bar",              
							"has_vaulted_ceiling",      
							"has_sprinkler_system",     
							"has_sports_court",         
							"has_skylight",             
							"has_security_system",      
							"has_sauna",                
							"has_rv_parking",           
							"has_porch",                
							"has_ceiling_fan",         
							"has_patio",                
							"has_mother_in_law",        
							"has_jetted_bath_tub",      
							"has_hot_tub_spa",          
							"has_green_house",          
							"has_gated_entry",          
							"has_garden",               
							"has_deck",                
							"has_disabled_access",      
							"has_elevator",
							"cooling_systems",#            100.00
							"brokerage_website_url",#      100.00
							"lead_routing_email",#         100.00
							"architecture_style",#         100.00
							"has_double_pane_windows",#    100.00
							"agent_phone",#                100.00
							"has_doorman",#                100.00
							"brokerage_logo_url",#         100.00
							"fees",#                       100.00
							"external_url",#               100.00
							"agent_id",#                   100.00
							"num_floors",#                 100.00
							"open_houses",#                100.00
							"exterior_types",#             100.00
							"price_cents_sqft",#           100.00
							"brokerage_phone",#            100.00
							"agent_email",#                100.00
							"rooms",#                      100.00
							"tax_amount",#                 100.00
							"tags",#                       100.00
							"agent_avatar_url",#           100.00
							"scoring",#                    100.00
							"school",#                     100.00
							"brokerage_email",#            100.00
							"room_count",#                 100.00
							"building_sqft",#              99.33
							"lot_sqft",#                   97.40
							"total_sqft",#                 94.25
							"roof_types",#                 86.29
							"unit_number",#                81.94
							"building_utilities",#         79.65
							"floors",#                     65.05
							"partial_bathrooms", #         54.05  
							"is_waterfront",
							"mls_number",
							"address_number",
							"location_ids",
							"lower_location_id",
							"location",
							"listing_status",
							"agent_fname",
							"agent_lname",
							"external_type",
							"agent_key",
							"brokerage_external_id",
							"brokerage_name",
							"building_type",
							"external_id",
							"geocoded",
							"agent_external_id",
							"agent_name",
							"available_showing",
							"basement",
							"brokerage",
							"cover_public_url",
							"description",
							"disclose_address",
							"fireplaces",
							"floors_number",
							"full_baths",
							"furnished",
							"garage",
							"half_baths",
							"has_attic",
							"is_cable_ready",
							"listing_category",
							"listing_date",
							"listing_title",
							"listing_type",
							"listing_url",
							"living_area",
							"main_level_sqft",
							"mls_id",
							"mls_name",
							"modified_at",
							"one_quarter_bathrooms",
							"open_house_count",
							"parking",
							"participant",
							"patio",
							"pool",
							"provider_category",
							"provider_name",
							"provider_url",
							"roof",
							"short_term",
							"showing_date",
							"state",
							"status",
							"stories",
							"three_quarter_bathrooms",
							"type",
							"water",
							"water_heater",
							"property_type"# to be used                  
							    ]

		#####################################################################################
		# Use relevant features only, drop others (check python notebook to see the logic) 
		# filter active properties only
		#####################################################################################

		df_sub_f1=df.drop(*drop_features)					    

		'''
		#####################################################################################
		# Feature Engineer Images 
		#####################################################################################
		#df_sub_f1 = df

		df_sub_f2 = get_images(df)


		df_sub_f3 = get_utilities(df_sub_f2)





				
		df_sub_f3.registerTempTable("df_sub_f3_tbl")


		'''
		mean_values=sqlContext.sql(
	                select ceil(mean(beds)),
	                       ceil(mean(bathrooms)),
	                       round(mean(price_cents))
	                from df_sub_f3_tbl
	               ).collect()

		
		df1=sqlContext.sql(
	                 select _id.*,
	                        created_at,
	                        updated_at,
	                        CAST (NVL(year_built,'UNKNOWN') as VARCHAR(500)) as year_built1,
	                        NVL(images_count,0) as images_count,
	                        nvl(beds,{0}) as beds ,
	                        nvl(bathrooms,{1}) as bathrooms,
	                        CAST ((nvl(price_cents,{2})) as INTEGER) as price_cents,
	                        nvl(city, 'UNKNOWN') as city,
	                        (CASE has_garage
	                           WHEN TRUE THEN 1
	                           ELSE 2
	                        END) as has_garage,
	                        (CASE has_fireplace
	                           WHEN TRUE THEN 1
	                           ELSE 2
	                        END) as has_fireplace,
	                        (CASE has_pool
	                           WHEN TRUE THEN 1
	                           ELSE 2
	                        END) as has_pool,
	                        (CASE has_basement
	                           WHEN TRUE THEN 1
	                           ELSE 2
	                        END) as has_basement,
	                         NVL(trim(province), 'UNKNOWN') province,
	                        CASE WHEN (replace(trim(property_sub_type),' ',''))='' THEN 'UNKNOWN' ELSE nvl(replace(trim(property_sub_type),' ',''),'UNKNOWN') END property_sub_type,
	                        NVL(CAST (parking_types as VARCHAR(500)),'UNKNOWN') parking_types,
	                        CASE WHEN (replace(trim(postal),' ',''))='' THEN 'UNKNOWN' ELSE nvl(replace(trim(postal),' ',''),'UNKNOWN') END postal,
	                        CAST (NVL(utilities_count, 0) as INTEGER) as utilities_count,
	                        utilities,
	                        CASE WHEN (replace(trim(address_street),' ',''))='' THEN 'UNKNOWN' ELSE nvl(replace(trim(address_street),' ',''),'UNKNOWN') END address_street
                   
	                        
	                from df_sub_f3_tbl
	                \
	               .format(\
	                       mean_values[0][0],\
	                       mean_values[0][1],\
	                       mean_values[0][2]),\
	              )
		'''

		

		df1=sqlContext.sql('''
                 select _id,
                 		created_at,
                        NVL(year_built,0) as year_built,
                        CAST( NVL(images_count,0) as INTEGER) as images_count,
                        nvl(beds,0) as beds ,
                        nvl(bathrooms,0) as bathrooms,
                        nvl(price_cents,0) as price_cents,
                        nvl(city,'UNKNOWN') as city,
                        (CASE has_garage
                           WHEN TRUE THEN 1
                           ELSE 2
                        END) as has_garage,
                        (CASE has_fireplace
                           WHEN TRUE THEN 1
                           ELSE 2
                        END) as has_fireplace,
                        (CASE has_pool
                           WHEN TRUE THEN 1
                           ELSE 2
                        END) as has_pool,
                        (CASE has_basement
                           WHEN TRUE THEN 1
                           ELSE 2
                        END) as has_basement,
                        nvl(province,'UNKNOWN') as province,
                        NVL(trim(property_sub_type), 'UNKNOWN') property_sub_type,
                        NVL(parking_types,'UNKNOWN') as parking_types,
                        CASE WHEN (replace(trim(postal),' ',''))='' THEN 'UNKNOWN' ELSE nvl(replace(trim(postal),' ',''),'UNKNOWN') END postal,
                        CAST (nvl(utilities_count,0) as INTEGER) as utilities_count,
                        CASE WHEN (replace(trim(address_street),' ',''))='' THEN 'UNKNOWN' ELSE nvl(replace(trim(address_street),' ',''),'UNKNOWN') END address_street1
                from df_sub_f3_tbl
                ''')

		
		return df1
	except Exception as e:
		#print("Exception raised in preprocessing() function : "+ str(e) )
		logging.exception("EXCEPTION -  preprocessing() function")
		raise e
		
