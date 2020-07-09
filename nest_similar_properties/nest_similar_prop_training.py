from pyspark.sql import SQLContext,functions as F
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import QuantileDiscretizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoderEstimator
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import MinMaxScaler
from pyspark.ml.feature import Normalizer
from pyspark.ml.feature import VectorIndexer
from pyspark.ml import Pipeline
from pyspark.ml.feature import MinHashLSH
from pyspark.ml.linalg import Vectors
from pyspark.sql.functions import col
import logging



class nest_similar_prop_training:
			


	def transformation(self,df1,sqlContext):

		## continous to integer buckets

		discretizer1 = QuantileDiscretizer(handleInvalid = "keep",numBuckets=15, inputCol="price_cents", outputCol="price_cents_q")
		discretizer2 = QuantileDiscretizer(handleInvalid = "keep",numBuckets=5,  inputCol="images_count", outputCol="images_count_q")
		discretizer3 = QuantileDiscretizer(handleInvalid = "keep",numBuckets=5,  inputCol="utilities_count", outputCol="utilities_q")



		#categorical/string to integers
		stringIndexer1 = StringIndexer(handleInvalid='keep', inputCol='city',              outputCol="city_i") 
		stringIndexer2 = StringIndexer(handleInvalid='keep', inputCol='province',          outputCol="province_i") 
		stringIndexer3 = StringIndexer(handleInvalid='keep', inputCol='parking_types',     outputCol="parking_types_i") 
		stringIndexer4 = StringIndexer(handleInvalid='keep', inputCol='property_sub_type', outputCol="property_sub_type_i") 
		stringIndexer5 = StringIndexer(handleInvalid='keep', inputCol='postal',            outputCol="postal_i") 
		#stringIndexer6 = StringIndexer(handleInvalid='keep', inputCol='address_street',    outputCol="address_street_i") 

  


		encoder = OneHotEncoderEstimator(inputCols=
											["price_cents_q",
                                            "images_count_q",
                                            "utilities_q",
                                            "city_i",
                                            "province_i",
                                            "parking_types_i",
                                            "property_sub_type_i",
                                            "postal_i",
                                            "year_built",
                                            "beds",
                                            "bathrooms",
                                            "has_garage",
                                            "has_fireplace",
                                            "has_pool",
                                            "has_basement"
                                            ],
                                outputCols=["price_cents_o",
                                            "images_count_o",
                                            "utilities_o",
                                            "city_o",
                                            "province_o",
                                            "parking_types_o",
                                            "property_sub_type_o",
                                            "postal_o",
                                            "year_built_o",
                                            "beds_o",
                                            "bathrooms_o",
                                            "has_garage_o",
                                            "has_fireplace_o",
                                            "has_pool_o",
                                            "has_basement_o"
                                            ]
                                            
                                )





		logging.warning("  pipeline called -  ")
		
		
		try:

			stages = [	discretizer1,
						discretizer2,
						discretizer3,
			          	stringIndexer1,
			          	stringIndexer2,
			          	stringIndexer3,
			          	stringIndexer4,
			          	stringIndexer5,
			          	encoder]

			pipeline = Pipeline(stages=stages)

			model = pipeline.fit(df1)
			df2 = model.transform(df1)

		except Exception as e:
			logging.exception("EXCEPTION -  Pipeline Logic")
			raise e 
			
		logging.warning("  pipeline finished -  ")
		
		
		features= [ "price_cents_o",
                    "price_cents_o",
                    "images_count_o",
                    "utilities_o",
                    "city_o",
                    "city_o",
                    "city_o",
                    "province_o",
                    "province_o",
                    "province_o",
                    "province_o",
                    "province_o",
                    "parking_types_o",
                    "property_sub_type_o",
                    "postal_o",
                    "postal_o",
                    "year_built_o",
                    "beds_o",
                    "beds_o",
                    "bathrooms_o",
                    "has_garage_o",
                    "has_fireplace_o",
                    "has_pool_o",
                    "has_basement_o"
		           ]


		logging.warning("  VectorAssembler called -  ")
		try:
			assembler = VectorAssembler(inputCols=features,outputCol="scaled_features")

			df3 = assembler.transform(df2)

		except Exception as e:
			print("Error in assembler logic  -  "+  str(e))
			raise e   	
	
		logging.warning("  VectorAssembler finished -  ")
	
		return df3


		#df3.registerTempTable("df3_tbl")

		#sqlContext.sql("select oid, scaled_features from df3_tbl where oid in ('5c1b0a92bc09e70001a4378f','5c818502be7c7e00011850bf','5c3eef2ca4fab100010eb651') ").show(10, False)

	
	def training(self,df3, my_spark):	

		logging.warning("  MinHash (Model) called -  ")
		try:
			mh = MinHashLSH(inputCol="scaled_features", outputCol="hashes", numHashTables=3)
			model = mh.fit(df3)

			#Cache the transformed columns
			#df3_t = model.transform(df3).cache()
	    
		
			df_model2=model.transform(df3)
		

			df_final2=model.approxSimilarityJoin(df_model2, df_model2, 0.5, distCol="JaccardDistance")\
							.filter("datasetA._id != datasetB._id")\
							.selectExpr("datasetA._id as id1", "datasetB._id as id2", "JaccardDistance as score", "datasetA.province as province", \
							           "datasetA.city as city","datasetA.created_at as id1_created_at") 

			print("training8")
		except Exception as e:
			print("Error in model training logic  -  "+  str(e))
			raise e   	

		logging.warning("  MinHash (Model) finished... returning -  ")
							
		return df_final2		




	def inference(self,model, df, key, n):

		key = df_.select("features").collect()[0]["features"]

		
		key=prediction.select("scaled_features").collect()[0]["scaled_features"]

		inference_df=model.approxNearestNeighbors(df, key, n)


		return inference_df





	#global variables

	def optimization(self,df2,sqlContext):

		df2.registerTempTable("df_final2_table")

		logging.warning("  ranking called -  ")
		
		df_final3=sqlContext.sql('''
							SELECT rs.id1,rs.id2, rs.score, rs.province, rs.city, rs.id1_created_at as last_updated_at
	    					FROM (
					        SELECT id1, id2, score, province, city, id1_created_at, row_number() over (PARTITION BY id2 ORDER BY score) as row_number
					        FROM df_final2_table
							     ) rs WHERE row_number <= 5
					 			''')

		logging.warning("  similarities format called -  ")
	
		df_final4=df_final3.select(
							    "id2",
							    F.struct(
							        F.col("id1"),
							        F.col("score"),
							        F.col('province'),
							        F.col('city'),
							        F.col('last_updated_at')
							    ).alias("values")
							).groupBy(
							    "id2"
							).agg(
							    F.collect_list("values").alias("values")
							).selectExpr("id2 propertyid", "values as similarities")
		logging.warning("  similarities format finished.. returning -  ")
				
		return df_final4

#spark.network.timeout=420000
#spark.dynamicAllocation.executorIdleTimeout 600s