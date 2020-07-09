#!/bin/bash
sudo python -m pip install pandas numpy matplotlib pymongo seaborn
#mkdir code
#aws s3 cp s3://aws-logs-966730287427-us-east-1/nest_similar_prop_initiate.py /code/
aws s3 cp s3://aws-logs-966730287427-us-east-1/nest_similar_prop_initiate.py /home/hadoop/

sudo aws s3 cp s3://aws-logs-966730287427-us-east-1/mongo-spark-connectors/org.mongodb.spark_mongo-spark-connector_2.11-2.4.0.jar /usr/lib/spark/jars/

sudo aws s3 cp s3://aws-logs-966730287427-us-east-1/mongo-spark-connectors/org.mongodb_mongo-java-driver-3.9.0.jar /usr/lib/spark/jars/
