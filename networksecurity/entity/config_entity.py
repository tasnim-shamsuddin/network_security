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
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

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