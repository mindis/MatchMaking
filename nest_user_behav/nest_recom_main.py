
import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext,functions as F

from nest_recom_spark_session import nest_get_spark_session

# Load Json to spark dataframe
from nest_recom_loader import load_spark_df

from nest_recom_event_mapper import (
	map_weights, 
	numeric_conversion
)

from nest_recom_constants import (
	FILE_PATH, 
	NUM_RECOM_PER_USR,
	MODE
	)

from nest_recom_als_model import nest_recom_als


def set_spark_local():
	l_obj=nest_get_spark_session()

	sc,sqlContext = l_obj.start_or_get_spark(
					app_name="NestReadyRecommendationEngine", 
					url='local[2]',
					memory="20g"
					)
	return sc, sqlContext

def set_spark_prod():
	
	sc = SparkContext(appName="NestReadyRecommendationEngine")
	sqlContext=SQLContext(sc)
	
	return sc, sqlContext


# comment it when running in production
sc,sqlContext = set_spark_local()


#sc,sqlContext = set_spark_prod()


data=load_spark_df(sqlContext,FILE_PATH,MODE)

#print(data.count())



df = map_weights(data,sc,sqlContext)


nest_recom_als=nest_recom_als()

# popularity matrix
popularity_df = nest_recom_als.popularity_matrix(df)
popularity_df.show()



df1 = numeric_conversion(df)





# COllaborative Filtering (User Behaviour )
model=nest_recom_als.als_algo(df1,MODE)


'''
model.write().overwrite().save("nest_recom_trained_model")
from pyspark.ml.recommendation import ALSModel
h=ALSModel.load("nest_recom_trained_model")
userRecs = h.recommendForAllUsers(5)
user85Recs = userRecs.filter(userRecs['new_userId'] == 1).collect()

for row in user85Recs:
    for rec in row.recommendations:
        print(rec.new_propertyId,rec.rating)

'''

als_df=nest_recom_als.recommend(NUM_RECOM_PER_USR,model,df1)


als_df.show()


