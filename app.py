import sys
import os 

import certifi
ca=certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from fastapi.import FastAPI,File,UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)

from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME

db=client.get_database("NetworkSecurity")
collection=db.get_collection("Network_security_collection")

app=FastAPI()
origins=["*"]

app.add_middleware(
    CORSMiddleware,     
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train",tags=["train"])
async def train_route():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.start_training_pipeline()
        return Response(content="Training successful!!")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    

if __name__=="__main__":
    try:
        app_run(app,host="localhost",port=8080)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
    