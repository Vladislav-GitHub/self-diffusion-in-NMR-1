# self-diffusion-in-NMR
docker run -d --rm -v $PWD:/app -p 8000:8000 sdnmr:0.1 uvicorn main:app --host 0.0.0.0 --port 8000
docker run -d --rm -v $PWD:/app -p 8501:8501 sdnmr:0.1 streamlit run app/app.py