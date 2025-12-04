import os 
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.models.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (AdaBoostClassifier, GradientBoostingClassifier,
                              RandomForestClassifier)
from networksecurity.utils.main_utils.utils import evaluate_models
import mlflow 

class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_config = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
        def track_mlflow(self, best_model_name, best_model, classification_metric_artifact:ClassificationMetricArtifact):
        try:
            import mlflow
            mlflow.set_experiment("Network_Security_Classification")
            with mlflow.start_run():
                f1_score=classification_metric_artifact.f1_score
                accuracy=classification_metric_artifact.accuracy_score
                precision=classification_metric_artifact.precision_score
                recall=classification_metric_artifact.recall_score

                mlflow.log_metric("F1_Score", f1_score)
                mlflow.log_metric("Accuracy", accuracy)
                mlflow.log_metric("Precision", precision)
                mlflow.log_metric("Recall", recall)
                mlflow.sklearn.log_model(best_model, best_model_name)


        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            logging.info("Training the model")
            # Add model training code here
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

     def train_model(self,x_train,y_train,x_test,y_test):
        models={
            "LogisticRegression":LogisticRegression(verbose=1),
            "DecisionTree":DecisionTreeClassifier(),
            "KNeighbors":KNeighborsClassifier(),
            "RandomForest":RandomForestClassifier(verbose=1),
            "AdaBoost":AdaBoostClassifier(),
            "GradientBoosting":GradientBoostingClassifier()
        }
        params={
            "LogisticRegression":{
                'C':[0.01,0.1,1,10],
                'solver':['liblinear','saga']
            },
           
            "DecisionTree":{
                'criterion':['gini','entropy'],
                'max_depth':[3,5,10,None]
            },
            "KNeighbors":{
                'n_neighbors':[3,5,7,9],
                'weights':['uniform','distance']
            },
            "RandomForest":{
                'n_estimators':[50,100,200],
                'criterion':['gini','entropy'],
                'max_depth':[3,5,10,None]
            },
            "AdaBoost":{
                'n_estimators':[50,100,200],
                'learning_rate':[0.01,0.1,0.5,1.0]
            },
            "GradientBoosting":{
                'n_estimators':[50,100,200],
                'learning_rate':[0.01,0.1,0.5,1.0],
                'subsample':[0.6,0.8,1.0]
            }
        }

        model_report:dict=evaluate_models(x_train,y_train,x_test,y_test,models,params)
        
        best_model_score=max(sorted(model_report.values()))
        best_model_name=list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model=models[best_model_name]
        y_train_pred=best_model.predict(x_train)

        get_classification_score(y_true=y_train,y_pred=y_train_pred)

        classification_metric_artifact=get_classification_score(
            y_true=y_train,y_pred=y_train_pred)
        
        ##fuction to track the ml flow 
        self.track_mlflow(best_model_name,best_model,classification_metric_artifact)


        y_test_pred=best_model.predict(x_test)
        classification_metric_artifact_test=get_classification_score(
            y_true=y_test,y_pred=y_test_pred)   
        
        preprocessor=load_object(
            file_path=self.data_transformation_artifact.transformed_object_file_path
        )   
        model_dir=self.model_trainer_config.model_save_dir
        os.makedirs(model_dir,exist_ok=True)

        NetworkModel_obj=NetworkModel(
            preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,
                    obj=NetworkModel_obj)
        
        save_object("final_model/model.pkl",best_model)

        
        #model trainer artifact
        model_trainer_artifact=ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_classification_metric_artifact=classification_metric_artifact,
            test_classification_metric_artifact=classification_metric_artifact_test
        )
        logging.info(f"Model trainer artifact : {model_trainer_artifact}")
        return model_trainer_artifact
    



        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info("Loading transformed training and testing array")
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path   

            train_arr= load_numpy_array_data(train_file_path
            test_array = load_numpy_array_data(test_file_path)

            x_train,y_train,x_test,y_test =(

            )  train_arr[:,:-1], train_arr[:,-1],
                test_array[:,:-1], test_array[:,-1]
            )

            model=self.train_model(x_train,y_train)


        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
   

        


