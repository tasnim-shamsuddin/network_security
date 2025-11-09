from datetime import datetime
import os
import sys
from networksecurity.constants.training_pipeline import training_pipeline
print(training_pipeline.PIPELINE_NAME)
print(training_pipeline.ARTIFACT_DIR)

class TrainingPipelineConfig:
    def __init__(self,time_stamp=datetime.now()):    
        time_stamp=timestamp.strftime("%m%d%Y__%H%M%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,time_stamp)
        self.timestamp:str=time_stamp    
                
class DataIngestionConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_ingestion_dir : str= os.path.join(
                training_pipeline_config.artifact_dir,
                training_pipeline.DATA_INGESTION_DIR,
                f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"
            )

            self.feature_store_file_path:str = os.path.join(
                self.data_ingestion_dir,
                "network_traffic.csv"
            )

            self.train_file_path :str= os.path.join(
                self.data_ingestion_dir,
                training_pipeline.TRAIN_FILE_NAME
            )

            self.test_file_path :str= os.path.join(
                self.data_ingestion_dir,
                training_pipeline.TEST_FILE_NAME
            )

            self.train_test_split_ratio :float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name :str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name :str = training_pipeline.DATA_INGESTION_DATABASE_NAME
          
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
class DataValidationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.data_validation_dir : str= os.path.join(
                training_pipeline_config.artifact_dir,
                training_pipeline.DATA_VALIDATION_DIR_NAME,
                f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"
            )

            self.valid_data_dir : str= os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_VALID_DIR
            )

            self.invalid_data_dir : str= os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_INVALID_DIR
            )

            self.valid_train_file_path : str= os.path.join(
                self.valid_data_dir,
                training_pipeline.TRAIN_FILE_NAME
            )

            self.valid_test_file_path : str= os.path.join(
                self.valid_data_dir, 
                training_pipeline.TEST_FILE_NAME
            )

            self.invalid_train_file_path : str= os.path.join(
                self.invalid_data_dir,
                training_pipeline.TRAIN_FILE_NAME
            )

            self.invalid_test_file_path : str= os.path.join(
                self.invalid_data_dir,                  
                training_pipeline.TEST_FILE_NAME
            )   


            self.drift_report_file_path : str= os.path.join(
                self.data_validation_dir,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
                training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
            )

            self.base_file_path : str = os.path.join(
                "networksecurity",
                "artifact",
                "data_ingestion",
                "feature_store",
                "network_traffic.csv"
            )
        except Exception as e:
            raise NetworkSecurityException(e, sys)

class DataTransformationConfig:
    def __init__(self, training_pipeline_config):
        self.data_transformation_dir = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME
        )
        self.data_transformation_train_file_path = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRAIN_FILE_NAME
        )
        self.data_transformation_test_file_path = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TEST_FILE_NAME
        )
        self.preprocessed_object_file_path = os.path.join(
            self.data_transformation_dir, training_pipeline.PREPROCESSING_OBJECT_FILE_NAME
        )
        self.data_transformation_drift_report_file_path = os.path.join(
            self.data_transformation_dir, training_pipeline.DATA_DRIFT_REPORT_FILE_NAME
        )
