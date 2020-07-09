from pyspark.sql.types import *
#P_INPUT_HOST_NAME="mongodb://127.0.0.1/backend_production.properties"

P_INPUT_HOST_NAME = "mongodb://3.210.155.32/backend_production.properties"

P_OUTPUT_HOST_NAME="mongodb://127.0.0.1/backend_production.properties"

P_APP_NAME="similar_properties"

P_MASTER="local[2]"

P_DRIVER_MEMORY="50g"

P_EXECUTOR_MEMORY="6g"

P_EXECUTOR_CORES=4

P_EXECUTOR_INSTANCES=1

P_PIVOT_MAX_VALUES=100000

P_MONGO_SPARK_CONNECTOR="org.mongodb.spark:mongo-spark-connector_2.11:2.4.0"

P_DEFAULT_SOURCE="com.mongodb.spark.sql.DefaultSource"

P_DB="backend_production"

P_COLLECTION="properties"

P_DEBUG="logging.DEBUG"
         
#P_SIMILAR_PROP_S3_PATH="/Users/jatinmalhotra/Desktop/NestReady_Recommendation_System/CODING/nest_recommendation_engine/similar_properties"
P_CA_SIMILAR_PROP_S3_PATH="s3://aws-logs-966730287427-us-east-1/ca_similar_property_json"
P_US_SIMILAR_PROP_S3_PATH="s3://aws-logs-966730287427-us-east-1/us_similar_property_json"


P_SCHEMA=StructType(  (
                StructField('_id',StringType(),True),
                StructField('address_street',StringType(),True),
                StructField('bathrooms',IntegerType(),True),
                StructField('beds',IntegerType(),True),
                StructField('city',StringType(),True),
                StructField('country',StringType(),True),
                StructField('created_at',TimestampType(),True),
                StructField('external_type',StringType(),True),
                StructField('has_basement',BooleanType(),True),
                StructField('has_fireplace',BooleanType(),True),
                StructField('has_garage',BooleanType(),True),
                StructField('has_pool',BooleanType(),True),
                StructField('images',ArrayType(StructType((StructField('_id',StringType(),True),StructField('sha1',StringType(),True))),True),True),
                StructField('parking_types',StringType(),True),
                StructField('postal',StringType(),True),
                StructField('price_cents',IntegerType(),True),
                StructField('property_sub_type',StringType(),True),
                StructField('utilities',StringType(),True),
                StructField('province',StringType(),True),
                StructField('year_built',IntegerType(),True),
                
               )
             
            )
