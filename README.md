# self-diffusion-in-NMR


### Сборка Docker образа и запуск контейнеров с FastAPI и Streamlit
```bash
# сборка docker image
docker build -t sdnmr:latest .

# запуск контейнера с FastAPI сервером в фоновом режиме:
docker run -d --rm -v $PWD:/app -p 8000:8000 sdnmr:latest uvicorn main:app --host 0.0.0.0 --port 8000 

# запуск контейнера с фронтендом на Streamlit в фоновом режиме:
docker run -d --rm -v $PWD:/app -p 8501:8501 sdnmr:latest streamlit run app.py
```