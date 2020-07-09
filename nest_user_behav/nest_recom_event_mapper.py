# Name: - nest_event_mapping_replace
# Input:- events weight mapping using replace function
# Description: - Function to apply event weights mapping
# calling :- df=nest_event_mapping_replace("df")

from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import col

from  nest_recom_default_weights import (
	EVENTS_WEIGHT, 
	DEFAULT_WEIGHT
	)

def map_weights(data,sc,sqlContext):
    
    data.registerTempTable("table")

    df=sqlContext.sql("select userId," 
    						+ " substr(context.page.path,11,length(context.page.path)) as propertyId,"
    						+ " event as weight" 
							+ " from table"
							+ " where userId is not null"
							+ " and event in" 
							+ " ("
							+ "  'ScheduleVisit',"
							+ "  'Unfavorited',"
							+ "  'PhotoClicked',"
							+ "  'CalculateClicked',"
							+ "  'MortgageCalculatorCTAClicked',"
							+ "  'ContactPartnerClicked',"
							+ "  'RequestInformationClicked',"
							+ "  'SimilarPropertyClicked',"
							+ "  'PartnerBanner',"
							+ "  'MapPinClicked',"
							+ "  'CallClicked',"
							+ "  'Prop-page-email',"
							+ "  'ChatClicked',"
							+ "  'AgentCall',"
							+ "  'AgentEmail',"
							+ "  'ComponentTriggered'"
							+ "  )" 
							+ "  order by userId")
    	
   # file_name="UserEvents/events_mapping.json"
   # events_mapping=sqlContext.read.json(file_name)
   # events=sc.textfile(events.txt)

    

    # give weights to each event
    df2 = df.replace(to_replace=EVENTS_WEIGHT, subset=['weight'])
    

    # weighted average
    df3 = df2.groupBy("userId","propertyId") \
    		 .agg({'weight':'avg'}) \
    		 .withColumnRenamed('avg(weight)', 'weight') \
    		 .fillna({'weight':DEFAULT_WEIGHT})

 
    # fill null with default weight
    #df5 = df4.fillna({'weight':DEFAULT_WEIGHT})
    #df6 = df5.na.drop()
    
    

    return df3

def numeric_conversion(data):
    indexers = [StringIndexer(inputCol=column, outputCol="new_"+column).fit(data) for column in list(set(data.columns)-set(['weight'])) ]
    pipeline = Pipeline(stages=indexers)
    df_r = pipeline.fit(data).transform(data)
    
    df_r = df_r.withColumn("new_userId", col("new_userId").cast("int"))
    df_r = df_r.withColumn("new_propertyId", col("new_propertyId").cast("int"))
    df_r = df_r.withColumn("weight", col("weight").cast("int"))
    
    
    ## TBD
    df_r = df_r.filter(df_r["new_propertyId"]!=0)
   
    
    return df_r
    
    '''
    stringIndexer = StringIndexer(inputCol="userId", outputCol="new_userId")
    model = stringIndexer.fit(sql_data)
    df_spark_index = model.transform(sql_data).withColumn("new_userId", col("new_userId").cast("int"))
    df_spark_index.show()
   
    # Convert into numerical IDs
     data['new_userId'] = data['userId'].astype("category").cat.codes
     data['new_propertyId'] = data['propertyId'].astype("category").cat.codes

     # Create a lookup frame so we can get the propertyId names back in 
     # readable form later.
     item_lookup = data[['new_propertyId', 'propertyId']].drop_duplicates()
     item_lookup['new_propertyId'] = item_lookup.new_propertyId.astype(str)

     data = data.drop(['user', 'propertyId'], axis=1)

    # Drop any rows that have 0 weight
     data = data.loc[data.weight != 0]

     # Create lists of all users, properties and weights
     users = list(np.sort(data.new_userId.unique()))
     artists = list(np.sort(data.new_propertyId.unique()))
     weight = list(data.weight)

     # Get the rows and columns for our new matrix
     rows = data.new_userId.astype(int)
     cols = data.new_propertyId.astype(int)

     '''
    

