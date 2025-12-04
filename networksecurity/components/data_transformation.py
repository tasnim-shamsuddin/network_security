import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException    
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_object, load_object, save_numpy_array_data

class DataTransformation:
    def __init__(self, data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact = data_validation_artifact
            self.data_transformation_config:DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(self)->Pipeline:
        try:
            #knn imputer
            knn_imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            return knn_imputer
            processor:Pipeline = Pipeline(steps=[
                ('imputer', knn_imputer)
            ])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
 

    def initiate_data_Transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            #reading validated train and test file path
            valid_train_file_path = self.data_validation_artifact.valid_train_file_path
            valid_test_file_path = self.data_validation_artifact.valid_test_file_path
            
            train_df = pd.read_csv(valid_train_file_path)
            test_df = pd.read_csv(valid_test_file_path)
            
            logging.info("Splitting input and target feature from both train and test dataframe")
            #splitting input and target feature from both train and test dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            
            #imputer object
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Fitting imputer on training data")
            #fitting on training data
            imputer.fit(input_feature_train_df)
            
            logging.info("Transforming training and testing data using imputer")
            #transforming training and testing data
            input_feature_train_arr = imputer.transform(input_feature_train_df)
            input_feature_test_arr = imputer.transform(input_feature_test_df)
            
            #target feature as numpy array
            target_feature_train_arr = target_feature_train_df.to_numpy()
            target_feature_test_arr = target_feature_test_df.to_numpy()
            
            #concatinating input and target features array
            train_arr = np.c_[input_feature_train_arr, target_feature_train_arr]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_arr]
            
            preprocessor=self.get_data_transformer_object()
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_arr=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_arr=preprocessor_object.transform(input_feature_test_df)

            #saving numpy array data
            logging.info("Saving transformed training and testing array")
            save_numpy_array_data(self.data_transformation_config.data_transformation_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.data_transformation_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.preprocessed_object_file_path,
                        obj=preprocessor_object)
            save_object("final_model/preprocessor.pkl",preprocessor_object)

            #saving imputer object
            logging.info("Saving imputer object")
            save_object(self.data_transformation_config.preprocessed_object_file_path, obj=imputer)
            
            #prepare artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.data_transformation_train_file_path,
                transformed_test_file_path=self.data_transformation_config.data_transformation_test_file_path,
                preprocessor_object_file_path=self.data_transformation_config.preprocessed_object_file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
            