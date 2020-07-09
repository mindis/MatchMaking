from __future__ import print_function
import logging
import time


from nest_similar_prop_constants import *
from nest_similar_prop_spark import set_spark_session

from nest_similar_prop_spark import load_mongo_data


from pyspark.sql import SparkSession
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext,functions as F
from pyspark.sql.functions import col


# drop unecessary features (more than 50% records are null)

from nest_similar_prop_preprocessing import preprocessing
from nest_similar_prop_training import nest_similar_prop_training




def write_to_s3(df, path):

	
	#####################################################################################
	## Write JSON to S3/ Local
	#####################################################################################
	logging.warning("  saving to S3  -  ")
		
	try:
			'''
			df.coalesce(1) \
			  .write.format('json') \
			  .mode("overwrite") \
			  .save(path)
			'''
			df.repartition(1) \
			  .write.format('json') \
			  .mode("overwrite") \
			  .save(path)
			  
	except Exception as e:
		print("Error in write_to_s3() function  -  "+  str(e))
		raise e  		  




def write_to_es(df):
	print("ES")

def write_to_mongo(df):
	print("Mongo")


if __name__ == "__main__":


	#https://realpython.com/python-logging/

	from datetime import datetime
	log_file = 'similar_properties_' + str(datetime.utcnow().strftime('%m_%d_%Y')) + '.log'

	logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.WARNING)
	
	# ORDER
	#logging.debug('DEBUG')
	#logging.info('INFO')
	#logging.warning('WARNING')
	#logging.exception("EXCEPTION")
	#logging.error("ERROR")
	

	
#	logging.warning('Admin logged out')
#	logging.exception("Exception occurred")
#	logging.error("error occurred")

	
	
	#df.registerTempTable("df_tbl")
	sqlContext,my_spark = set_spark_session()
		
	l_obj = nest_similar_prop_training()  # get an instance of the class
	

	

	############################
	## Run it for the CA
	############################
	

	try:
		
		logging.warning(" CA RUN started -  ")
		ca_start_time = time.time()
		
		sqlContext.clearCache()
		#pipeline1 = "{'$match': {'external_type':'list_hub', 'status':'active', 'country': 'US' }}"
		ca_pipeline="[{'$match': {'status':'active', 'country': 'CA' }},{ $project : {'external_type':1,'beds':1,'bathrooms':1,'year_built':1,'images':1,'price_cents':1,'has_garage':1,'has_fireplace':1,'has_pool':1,'has_basement':1,'province':1,'property_sub_type':1,'parking_types':1,'postal':1,'address_street':1,'country':1,'city':1,'created_at':1,'utilities':1} } ]"

		ca_df = load_mongo_data(ca_pipeline,my_spark)

		ca_df.registerTempTable("ca_df_tbl")
		
		
		################################
		# Caching the data in MEMORY
		################################
		#sqlContext.cacheTable("ca_df_tbl")
		
		my_spark.catalog.cacheTable("ca_df_tbl")
		
		#sqlContext.cacheTable("ca_df_tbl")
		# or its good idea to directly cache a dataframe instead of table like below
		# ca_df.cache()


		df_ca_filter = sqlContext.sql("select * from ca_df_tbl")
		
	
		#df_ca_filter=df.filter((df["country"]=='CA') & (df["status"]["symbol"] =='active'))
		
		
		#df_ca_filter = df.filter( (col("country")=='CA') & (col("status.symbol")=='active'))

		#df_ca_filter=df_ca_filter.filter(df_ca_filter["city"]=="Toronto")
			
		logging.warning("  preprocessing called -  ")
		df1_ca=preprocessing(df_ca_filter,sqlContext)

		
		
		logging.warning("  transformation called -  ")
		df1_2_ca=l_obj.transformation(df1_ca,sqlContext)

			
		################################
		# Clear cache()
		################################
		#my_spark.catalog.uncacheTable("ca_df_tbl")
		#sqlContext.clearCache()

		logging.warning("  training called -  ")
		df2_ca=l_obj.training(df1_2_ca,sqlContext)

		
		################################
		# Caching the data in MEMORY
		################################
		#df2_ca.cache()

		
		logging.warning("  optimization called -  ")
		df3_ca=l_obj.optimization(df2_ca,sqlContext)
		#my_spark.catalog.uncacheTable("ca_df_tbl")

		
		df3_ca.registerTempTable("df3_ca_tbl")
		my_spark.catalog.cacheTable("df3_ca_tbl")

		df3_ca = sqlContext.sql("select * from df3_ca_tbl")

		write_to_s3(df3_ca,P_CA_SIMILAR_PROP_S3_PATH)

		
		# Clearning the memory for specific table
		my_spark.catalog.uncacheTable("df3_ca_tbl")

		# clearning memory for all
		#my_spark.clearCache()

		
		#df3_ca.registerTempTable("df3_tbl")
		#print("running show query now ")
		#sqlContext.sql("select * from df3_tbl where propertyid in ('5c1b0a92bc09e70001a4378f','5c818502be7c7e00011850bf','5c3eef2ca4fab100010eb651') ").show(10, False)

		
		print("CA took ", (time.time() -  ca_start_time))
		logging.warning(" CA RUN took {} seconds for training.".format( time.time() -  ca_start_time))
	
	except Exception as e:
		logging.exception("EXCEPTION in MAIN  -  CA RUN ")
		raise e 	
	

	
    
	#ca_start_time = time.time()
	#logging.warning(" CA WRITING TO S3 took {} seconds for training.".format( time.time() -  ca_start_time))

	
	
	############################
	## Run it for the US
	############################
	try:
		
		logging.warning(" US RUN started -  ")
		us_start_time = time.time()
		
		
		#pipeline1 = "{'$match': {'external_type':'list_hub', 'status':'active', 'country': 'US' }}"
		#us_pipeline="[{'$match': {'external_type':'list_hub', 'status':'active', 'country': 'US' }},{ $project : {'external_type':1,'beds':1,'bathrooms':1,'year_built':1,'images':1,'price_cents':1,'has_garage':1,'has_fireplace':1,'has_pool':1,'has_basement':1,'province':1,'property_sub_type':1,'parking_types':1,'postal':1,'address_street':1,'country':1,'city':1,'created_at':1,'utilities':1} } ]"

		#us_pipeline="[{'$match': {'external_type':{ $in: [ 'crea', 'list_hub' ] }, 'status':'active', 'country': 'US' }},{ $project : {'external_type':1,'beds':1,'bathrooms':1,'year_built':1,'images':1,'price_cents':1,'has_garage':1,'has_fireplace':1,'has_pool':1,'has_basement':1,'province':1,'property_sub_type':1,'parking_types':1,'postal':1,'address_street':1,'country':1,'city':1,'created_at':1,'utilities':1} } ]"

		#sqlContext.clearCache()

		us_pipeline="[{'$match': {'status':'active', 'country': 'US' }},{ $project : {'external_type':1,'beds':1,'bathrooms':1,'year_built':1,'images':1,'price_cents':1,'has_garage':1,'has_fireplace':1,'has_pool':1,'has_basement':1,'province':1,'property_sub_type':1,'parking_types':1,'postal':1,'address_street':1,'country':1,'city':1,'created_at':1,'utilities':1} } ]"

		us_df = load_mongo_data(us_pipeline,my_spark)

		us_df.registerTempTable("us_df_tbl")
		
		################################
		# Caching the data in MEMORY
		################################
		my_spark.catalog.cacheTable("us_df_tbl")


		df_us_filter = sqlContext.sql("select * from us_df_tbl")
		
	
		#df_ca_filter=df.filter((df["country"]=='CA') & (df["status"]["symbol"] =='active'))
		
		
		#df_ca_filter = df.filter( (col("country")=='CA') & (col("status.symbol")=='active'))

		#df_ca_filter=df_ca_filter.filter(df_ca_filter["city"]=="Toronto")
			
		logging.warning("  preprocessing called -  ")
		df1_us=preprocessing(df_us_filter,sqlContext)

		
		logging.warning("  transformation called -  ")
		df1_2_us=l_obj.transformation(df1_us,sqlContext)

		################################
		# Clear cache()
		################################
		#my_spark.catalog.uncacheTable("us_df_tbl")
		#my_spark.clearCache()

			
		logging.warning("  training called -  ")
		df2_us=l_obj.training(df1_2_us,sqlContext)
		
		################################
		# Caching the data in MEMORY
		################################
		#df2_us.cache()



		logging.warning("  optimization called -  ")
		df3_us=l_obj.optimization(df2_us,sqlContext)

		#df3_us.cache()


		my_spark.catalog.uncacheTable("us_df_tbl")

		
		df3_us.registerTempTable("df3_us_tbl")
		my_spark.catalog.cacheTable("df3_us_tbl")

		df3_us = sqlContext.sql("select * from df3_us_tbl")
		
		write_to_s3(df3_us,P_US_SIMILAR_PROP_S3_PATH)

		
		# Clearning the memory for specific table
		my_spark.catalog.uncacheTable("df3_us_tbl")
		
		# clearning memory for all
		#sqlContext.clearCache()

		
		#df3_ca.registerTempTable("df3_tbl")
		#print("running show query now ")
		#sqlContext.sql("select * from df3_tbl where propertyid in ('5c1b0a92bc09e70001a4378f','5c818502be7c7e00011850bf','5c3eef2ca4fab100010eb651') ").show(10, False)

		
		print("US took ", (time.time() -  ca_start_time))
		logging.warning(" US RUN took {} seconds for training.".format( time.time() -  us_start_time))
	
	except Exception as e:
		logging.exception("EXCEPTION in MAIN  -  US RUN ")
		raise e 	
	