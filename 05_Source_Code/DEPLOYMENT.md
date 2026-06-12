Deployment options

1) Streamlit Community Cloud (easiest)
- Push your repo to GitHub (public or private).
- In Streamlit Community Cloud, "New app" → connect GitHub repo → select branch and `05_Source_Code/Script/app.py` as the app file.
- Streamlit will install `requirements.txt` and run the app.

2) Docker (portable)
- Build locally:
  docker build -t hoax-detector:latest -f Dockerfile .
- Run:
  docker run -p 8501:8501 hoax-detector:latest
- Push to a container registry (Docker Hub, GitHub Container Registry) and deploy to Render/Cloud Run.

3) Render / Railway / Heroku (without Docker)
- Ensure `requirements.txt` exists at repo root or change start command to:
  `python -m streamlit run 05_Source_Code/Script/app.py --server.headless true --server.port $PORT`
- On Render: create a Web Service, use `Start Command` above and set port environment.

Notes
- Ensure `06_Model/best_model_nb.pkl` and `04_Dataset/Processed_Dataset/clean.csv` are included in the repo if you want the deployed app to have the model and sample data. For large models, prefer uploading the model to a persistent store and download at startup.
- For Streamlit Community Cloud, store the model in the repo (small) or use Git LFS for larger files.

Commands quick copy

```bash
# build and run locally with Docker
cd 05_Source_Code
docker build -t hoax-detector:latest -f Dockerfile .
docker run -p 8501:8501 hoax-detector:latest

# Run locally without Docker (venv)
.
# activate venv then:
python -m streamlit run "Script/app.py" --server.headless true --server.port 8501
```
