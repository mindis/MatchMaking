# file name: nest_recom_spark_session.py
# author: Jatin
# Description: Sets spark session locally
# Compiled at: 2019-03-25 14:12:59

import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkConf,SparkContext
from pyspark.sql import SQLContext,functions as F


class nest_get_spark_session:
    
    def start_or_get_spark( self,
                            app_name='Testing', 
                            url='local[*]', 
                            memory='12g'):

        """Start Spark if not started
        Args:
            app_name (str): Set name of the application
            url (str): URL for spark master/local.
            memory (str): Size of memory for spark driver.

        Returns:
            obj: Spark context and Sql context

        SparkSession internals sets SparkContext as well
        local is for personal computer/laptops. In production, please use master cluster 

        """
        spark = SparkSession.builder\
                .appName(app_name)\
                .master(url)\
                .config('spark.driver.memory', memory)\
                .getOrCreate()

        # Set SQL Context
        sqlContext=pyspark.SQLContext(spark)

        return spark,sqlContext
     
