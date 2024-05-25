# Local

```
uvicorn main:app --reload

python -c "import openai; print(openai.__version__)"

Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'openai'

python -m pip install openai 
```

```
deactivate
python -m venv functions/venv --clear
source functions/venv/bin/activate
```

```
cd functions
firebase emulators:start
```

# Backend Deploy
```
gcloud config set project lingualog-dev
gcloud run deploy lingualog --region=us-central1 --source .

```

# Prod Backend Deploy
```
gcloud config set project lingualog-9b671
gcloud run deploy lingualog --region=us-central1
```

# Prod Gateway Deploy
```
gcloud endpoints services deploy openapi-run.yaml \
  --project lingualog-9b671

chmod +x gcloud_build_image

./gcloud_build_image -s lingualog-gateway-fvyuvymqkq-uc.a.run.app \
    -c 2023-12-07r0 -p lingualog-9b671

gcloud run deploy lingualog-gateway \
  --image="gcr.io/lingualog-9b671/endpoints-runtime-serverless:2.46.0-lingualog-gateway-fvyuvymqkq-uc.a.run.app-2023-12-07r0" \
  --allow-unauthenticated \
  --platform managed \
  --project=lingualog-9b671
```