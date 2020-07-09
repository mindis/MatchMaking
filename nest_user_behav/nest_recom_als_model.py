from pyspark.ml.recommendation import ALS
import time
from pyspark.sql import SQLContext,functions as F
from pyspark.ml.recommendation import ALSModel

    

class nest_recom_als:

    def als_algo(self,data,MODE):
        
        als = ALS(userCol="new_userId", 
                  itemCol="new_propertyId", 
                  ratingCol="weight",
                  coldStartStrategy="nan"
                  )
        
        #start_time = time.time()
        #train_time = time.time() - start_time
        #print("Took {} seconds for training.".format(train_time))
    
        '''
        Save and Load Models
        model.write().overwrite().save("nest_recom_trained_model2")
        from pyspark.ml.recommendation import ALSModel
        h=ALSModel.load("nest_recom_trained_model")
        

        from pyspark.ml import Pipeline
        from pyspark.ml import PipelineModel

        pipeTrain.write().overwrite().save(outpath)
        model_in = PipelineModel.load(outpath)

        '''

        if (MODE=='DAILY'):

            # Load the trained model
            trained_model=ALSModel.load("nest_recom_trained_model")
            model=trained_model.fit(data)
           
        else:
            model = als.fit(data)
          
        # Save trained Model
        model.write().overwrite().save("nest_recom_trained_model")
       
        return model


    def recommend(self,num,model1,df2,user= None):

        model=ALSModel.load("nest_recom_trained_model")
        #model=trained_model.fit(data)

        userRecs = model.recommendForAllUsers(num)
        

        aa = userRecs.withColumn("recommendations",F.explode("recommendations"))

        aa = aa.select("new_userId","recommendations.new_propertyId","recommendations.rating")
        
        #aa_joined = aa.join(df2,['new_userId','new_propertyId'],'inner')
        aa_joined = aa.join(df2,['new_userId','new_propertyId'])

        #df = df1.join(df2, (df1.x1 == df2.x1) & (df1.x2 == df2.x2))
        
        final_df1= (aa_joined.select("userId","propertyId","rating").withColumn("Recommendations", F.struct(F.col("propertyId"), F.col("rating")))).select("userId","Recommendations")

        #final_df2 = final_df1.filter(final_df1.new_userId==userId)


        ##final_json=final_df1.groupby("userId").agg(F.collect_list("Recommendations").alias("Recommendations"))
        ##final_json.coalesce(1).write.format('json').save('cc.json')



        return final_df1    
    

    def popularity_matrix(self,data):

        '''
          df.cache() \
            .filter("Recommendations.rating <=10") \
            .groupBy("Recommendations.propertyId") \
            .agg({'Recommendations.rating':'avg'}) \
            .withColumnRenamed('avg(Recommendations.rating AS `rating`)', 'avg_rating') \
            .orderBy('avg_rating', ascending=False)

        '''

        df = data.cache() \
            .groupBy("propertyId") \
            .agg(F.sum(data.weight)) \
            .withColumnRenamed('sum(weight)', 'avg_weight') \
            .orderBy('avg_weight', ascending=False)
    
    
            #.agg({'weight':'avg'}) \
            #.withColumnRenamed('avg(weight)', 'avg_weight') \
          


        return df


    def tune_model(self, maxIter, regParams, ranks, split_ratio=(6, 2, 2)):
        """
        Hyperparameter tuning for ALS model
        Parameters
        ----------
        maxIter: int, max number of learning iterations
        regParams: list of float, regularization parameter
        ranks: list of float, number of latent factors
        split_ratio: tuple, (train, validation, test)
        """
        # split data
        train, val, test = self.ratingsDF.randomSplit(split_ratio)
        # holdout tuning
        self.model = tune_ALS(self.model, train, val,
                              maxIter, regParams, ranks)
        # test model
        predictions = self.model.transform(test)
        evaluator = RegressionEvaluator(metricName="rmse",
                                        labelCol="rating",
                                        predictionCol="prediction")
        rmse = evaluator.evaluate(predictions)
        print('The out-of-sample RMSE of the best tuned model is:', rmse)
        # clean up
        del train, val, test, predictions, evaluator
        gc.collect()


    def tune_ALS(model, train_data, validation_data, maxIter, regParams, ranks):
        """
        grid search function to select the best model based on RMSE of
        validation data
        Parameters
        ----------
        model: spark ML model, ALS
        train_data: spark DF with columns ['userId', 'movieId', 'rating']
        validation_data: spark DF with columns ['userId', 'movieId', 'rating']
        maxIter: int, max number of learning iterations
        regParams: list of float, one dimension of hyper-param tuning grid
        ranks: list of float, one dimension of hyper-param tuning grid
        Return
        ------
        The best fitted ALS model with lowest RMSE score on validation data
        """
        # initial
        min_error = float('inf')
        best_rank = -1
        best_regularization = 0
        best_model = None

        for rank in ranks:
            for reg in regParams:
                # get ALS model
                als = model.setMaxIter(maxIter).setRank(rank).setRegParam(reg)
                # train ALS model
                model = als.fit(train_data)
                # evaluate the model by computing the RMSE on the validation data
                predictions = model.transform(validation_data)
                evaluator = RegressionEvaluator(metricName="rmse",
                                                labelCol="rating",
                                                predictionCol="prediction")
                rmse = evaluator.evaluate(predictions)
                print('{} latent factors and regularization = {}: '
                      'validation RMSE is {}'.format(rank, reg, rmse))
                if rmse < min_error:
                    min_error = rmse
                    best_rank = rank
                    best_regularization = reg
                    best_model = model
        print('\nThe best model has {} latent factors and '
              'regularization = {}'.format(best_rank, best_regularization))
        return best_model



                