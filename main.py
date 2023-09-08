from fastapi import FastAPI, File, UploadFile
from utils.file_handler import file_to_dataframe
from models.prediction import predict_coef

app = FastAPI()

@app.get("/")
async def healthcheck():
    return "I am alive!"

@app.post("/application")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()
    results = predict_coef(contents)
    return results