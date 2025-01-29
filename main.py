from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
import os,io
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI,File,UploadFile
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os

import pandas as pd 

env_file_path=os.path.join(os.getcwd(),"env.yaml")

def set_env_variable(env_file_path):

    if os.getenv('MONGO_DB_URL',None) is None:
        env_config = read_yaml_file(env_file_path)
        os.environ['MONGO_DB_URL']=env_config['MONGO_DB_URL']


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if model_resolver.is_model_exists():
            return Response("Model already trained and saved.")

        train_pipeline = TrainPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        
        train_pipeline.run_pipeline()
        return Response("Training successful and model saved!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/predict")
async def predict_route(file: UploadFile = File(...)):
    try:
        
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

       
        model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available", status_code=400)

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)


        if "class" in df.columns:
            df.drop(columns=["class"], inplace=True)

        required_features = list(model.feature_names_in_) if hasattr(model, "feature_names_in_") else None
        if required_features:
            missing_features = [feature for feature in required_features if feature not in df.columns]
            if missing_features:
                return Response(
                    f"Missing required features in the uploaded file: {missing_features}",
                    status_code=400
                )
            df = df[required_features]

        df.fillna(0, inplace=True)

        predictions = model.predict(df)

        target_mapping = TargetValueMapping()
        df['predicted_column'] = [target_mapping.reverse_mapping().get(pred, pred) for pred in predictions]

        response_data = df.head(100).to_json(orient="records")
        return Response(response_data, media_type="application/json")

    except pd.errors.EmptyDataError:
        return Response("Uploaded file is empty or invalid CSV format.", status_code=400)
    except Exception as e:
        logging.exception(f"Error during prediction: {e}")
        return Response(f"Error Occurred! {str(e)}", status_code=500)



def main():
    try:
        set_env_variable(env_file_path)
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)


if __name__=="__main__":
    #main()
    # set_env_variable(env_file_path)
    app_run(app, host=APP_HOST, port=APP_PORT)
