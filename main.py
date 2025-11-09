     
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        DataIngestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=DataIngestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        DataValidation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_validation_config=DataValidation_config, data_ingestion_artifact=data_ingestion_artifact)
        logging.info("Initiate the data validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data validation completed successfully")
        DataTransformation_config=DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        logging.info(" data transformation started")
        from networksecurity.components.data_transformation import DataTransformation
        data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,
                                               data_transformation_config=DataTransformation_config)
        data_transformation_artifact=data_transformation.initiate_data_Transformation()
        print(data_transformation_artifact) 
        logging.info("data transformation completed successfully")


      

    except Exception as e:
        raise NetworkSecurityException(e, sys)