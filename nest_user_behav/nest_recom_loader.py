
import os
import re
import shutil
import warnings
import pandas as pd
from zipfile import ZipFile
from pyspark import SparkConf,SparkContext
import pyspark
import json
from pyspark.sql.functions import from_json
from pyspark.sql import SQLContext,functions as F



def load_spark_df(
    sqlContext,
    file_path,
    mode
 ):
    """Loads the 


     dataset as pySpark.DataFrame.

    Download the dataset from http://files.grouplens.org/datasets/movielens, unzip, and load

    Args:
        spark (pySpark.SparkSession)
        size (str): Size of the data to load. One of ("100k", "1m", "10m", "20m").
        header (list or tuple): Rating dataset header.
            If schema is provided, this argument is ignored.
        schema (pySpark.StructType): Dataset schema. By default,
            StructType(
                [
                    StructField(DEFAULT_USER_COL, IntegerType()),
                    StructField(DEFAULT_ITEM_COL, IntegerType()),
                    StructField(DEFAULT_RATING_COL, FloatType()),
                    StructField(DEFAULT_TIMESTAMP_COL, LongType()),
                ]
            )
        local_cache_path (str): Path (directory or a zip file) to cache the downloaded zip file.
            If None, all the intermediate files will be stored in a temporary directory and removed after use.
        dbutils (Databricks.dbutils): Databricks utility object
        title_col (str): Title column name. If None, the column will not be loaded.
        genres_col (str): Genres column name. Genres are '|' separated string.
            If None, the column will not be loaded.
        year_col (str): Movie release year column name. If None, the column will not be loaded.

    Returns:
        pySpark.DataFrame: Movie rating dataset.
    """
    
    """
    Commented by Jatin - TBD
    
    #size = size.lower()
    #if size not in DATA_FORMAT:
    #    raise ValueError(ERROR_MOVIE_LENS_SIZE)

    #schema = _get_schema(header, schema)
    #if schema is None:
    #    raise ValueError(ERROR_NO_HEADER)

    #movie_col = DEFAULT_ITEM_COL if len(schema) < 2 else schema[1].name
    #"""

    #UNIX COMMAND to get latest files from S3 bucket
    #/users/jatinmalhotra/bin/aws s3 ls s3://aws-logs-966730287427-us-east-1/userevents/eventlogs/ | grep ${DATE} | awk '{print $4}'


    #################################################
    #Option 1 - (Read as RDD and convert to json )  SLOWEST
    #################################################
    def load_rdd():
        rdd=sc.textFile("s3://aws-logs-966730287427-us-east-1/eventlogs/")
        l_df=rdd.map(json.loads)

        return l_df


    #################################################
    #Option 2 - (Read with inferschema false
    #################################################
    def load_inferSchema():
        l_df = sqlContext.read.options(header='false', inferschema='true').json(file_path)
        #We are using inferSchema = True option for telling sqlContext to automatically detect the data type of each column in data frame. If we do not set inferSchema to be true, all columns will be read as string.
        return l_df



    from datetime import datetime
    l_date = datetime.today().strftime('%Y%m')
    

    '''
    if (mode=='DAILY'):
        l_file_name='/Users/jatinmalhotra/Desktop/not2/' + l_date + '/'
        
    else:
        l_file_name=file_path

    '''

    l_file_name='/Users/jatinmalhotra/Desktop/not2/' + l_date + '/' if (mode=='DAILY') else file_path
        

    #################################################
    #Option 3 - Normal json read
    #################################################
    #df = sqlContext.read.json("s3://aws-logs-966730287427-us-east-1/eventlogs/")   
    df = sqlContext.read.json(l_file_name)   

    
    if (mode == 'DAILY'):
        l_table_name='DAILY'+l_date
        l_e_flag=False

        print(l_table_name)
        
        
        try:
            sqlContext.sql("SELECT count(1) FROM {} where 1=2".format(l_table_name+'1'))
        except:
            l_e_flag=True
            pass   

         

        if (l_e_flag):
            df.write.mode("append").saveAsTable(l_table_name+'1')
            
        else:
            df.registerTempTable("df_tmp")
            df = sqlContext.sql("SELECT a.* from df_tmp a where 1=1 and not exists (select 1 from {} where a.messageId=messageId)".format(l_table_name))

    

        
    
    #################################################
    #Option 4 - (Infer Schema from one j=object )
    #################################################

   # schemadf=sqlContext.read.options(header='false', inferschema='true').json("s3://aws-logs-966730287427-us-east-1/eventlogs/006591e71461553c573829895f6d30c2_1553068752750.json")

    #df=sqlContext.read.options(header='false', schema=df1.schema).json("s3://aws-logs-966730287427-us-east-1/eventlogs/")


    
    #################################################
    #Option 5 - Read Nested directory structure, * means one directory
    #################################################
    #df1 = sqlContext.read.json("s3://aws-logs-966730287427-us-east-1/userevents/*/")


    # Merge rating df w/ item_df
    #if item_df is not None:
     #   df = df.join(item_df, movie_col, "left")

    # Cache and force trigger action since data-file might be removed.
    #df.cache()
    #df.count()

    return df

#GET .H5 FILENAMES -- TESTING PURPOSE ONLY
'''
def dbtesting():
    hdfs_file_paths = []
    for root in file_roots:
        for path, subdirs, files in os.walk(root):
            for name in files:
                hdfs_file_paths.append(os.path.join(path, name))
    print '{} filenames gathered (PYTHON)'.format(len(hdfs_file_paths))

    #DISTRIBUTED CONVERSION FROM .H5 TO PYTHON DICT WITH PYSPAR
    file_paths = sc.parallelize(hdfs_file_paths)
    rdd = file_paths.map(lambda x: h5todict(x))
    data = rdd.collect()
    print '{} data collected (PYSPARK)'.format(len(data))

    #INSERT FILES TO MONGODB
    client = MongoClient()
    db = client[dbname]
    db[collection_name].drop() #drop collection if it was created before
    collection=db[collection_name]
    # insert data here
    for d in data:
        collection.insert_one(d)

    print '{} data are inserted to collection: "{}" (MONGODB)'.format(collection.count(), collection_name)
'''




def _get_schema(header, schema):
    if schema is None or len(schema) == 0:
        # Use header to generate schema
        if header is None or len(header) == 0:
            return None
        elif len(header) > 4:
            warnings.warn(WARNING_MOVIE_LENS_HEADER)
            header = header[:4]

        schema = StructType()
        try:
            schema.add(StructField(header[0], IntegerType())).add(
                StructField(header[1], IntegerType())
            ).add(StructField(header[2], FloatType())).add(
                StructField(header[3], LongType())
            )
        except IndexError:
            pass
    else:
        if header is not None:
            warnings.warn(WARNING_HAVE_SCHEMA_AND_HEADER)

        if len(schema) > 4:
            warnings.warn(WARNING_MOVIE_LENS_HEADER)
            schema = schema[:4]

    return schema