from fastapi import FastAPI, File, UploadFile
import torch
from utils.file_processing import read_file
from models.model_utils import train_model, predict_model
import numpy as np
import pandas as pd
import os

app = FastAPI()

@app.get("/")
async def healthcheck():
    return "I am alive!"


@app.post("/train/")
async def train(file: UploadFile):
    file_path = f"{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    response_message = []  # Создаем список для сбора сообщений

    try:
        data = read_file(file_path)
        response_message.append("File read successfully")
    except Exception as e:
        response_message.append(f"An error occurred while reading the file: {str(e)}")
        return {"error": str(e), "message": response_message}

    try:
        model, history_loss = train_model(data)
        response_message.append("Model trained successfully")
    except Exception as e:
        response_message.append(f"An error occurred while training the model: {str(e)}")
        return {"error": str(e), "message": response_message}

    try:
        x_data = torch.tensor(data['Gradient'].values, dtype=torch.float32).unsqueeze(1)
        predictions = predict_model(model, x_data)
        
        # Получаем fitted_A и fitted_B
        fitted_A = model.A.detach().numpy()
        condition = lambda coeff: coeff if coeff >= 0 else 1e-6
        fitted_A = np.array(list(map(condition, fitted_A)))
        fitted_A = fitted_A / np.sum(fitted_A, axis=0, keepdims=True)
        fitted_B = model.B.detach().numpy()
    except Exception as e:
        response_message.append(f"An error occurred while predicting: {str(e)}")
        return {"error": str(e), "message": response_message}


    # Remove the temporary file
    os.remove(file_path)

    return {"loss_history": history_loss, "message": response_message, "predictions": predictions.tolist(), "fitted_A": fitted_A.tolist(), "fitted_B": fitted_B.tolist()}
