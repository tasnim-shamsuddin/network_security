from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging import logger
from networksecurity.entity.config_entity import DataIngestionConfig

if __main__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        DataIngestion_config=DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=DataIngestion_config)
        logger.logging.info("Initiate the data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
      

    except Exception as e:
        raise NetworkSecurityException(e, sys)