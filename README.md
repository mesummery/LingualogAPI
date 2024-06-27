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

# Develop
## Develop Backend Deploy
```
gcloud config set project lingualog-dev
gcloud run deploy lingualog --region=us-central1 --source .

```
## Develop Gateway Deploy
```
export CONFIG_ID=
export API_ID=lingualog-api
export PROJECT_ID=lingualog-dev
export SERVICE_ACCOUNT_EMAIL=lingualog-dev-backend@lingualog-dev.iam.gserviceaccount.com

# Set Config
gcloud api-gateway api-configs create $CONFIG_ID \
  --api=$API_ID --openapi-spec=openapi2-run.yaml \
  --project=$PROJECT_ID --backend-auth-service-account=$SERVICE_ACCOUNT_EMAIL

# Show Config
gcloud api-gateway api-configs describe $CONFIG_ID \
  --api=$API_ID --project=$PROJECT_ID

# Deploy
export GATEWAY_ID=lingualog-api-gateway
export GCP_REGION=us-central1

## create
#gcloud api-gateway gateways create $GATEWAY_ID \
#  --api=$API_ID --api-config=$CONFIG_ID \
#  --location=$GCP_REGION --project=$PROJECT_ID

## update
gcloud api-gateway gateways update $GATEWAY_ID \
  --api-config=$CONFIG_ID --api=$API_ID --location=$GCP_REGION --project=$PROJECT_ID

# Show info
gcloud api-gateway gateways describe $GATEWAY_ID \
  --location=$GCP_REGION --project=$PROJECT_ID
```

# Prod 
## Prod Backend Deploy
```
gcloud config set project lingualog-9b671
gcloud run deploy lingualog --region=us-central1 --source .
```

## Prod Gateway Deploy
```
export CONFIG_ID=
export API_ID=lingualog-api
export PROJECT_ID=lingualog-9b671
export SERVICE_ACCOUNT_EMAIL=lingualog-prod-backend@lingualog-9b671.iam.gserviceaccount.com

# Set Config
gcloud api-gateway api-configs create $CONFIG_ID \
  --api=$API_ID --openapi-spec=openapi2-run.yaml \
  --project=$PROJECT_ID --backend-auth-service-account=$SERVICE_ACCOUNT_EMAIL

# Show Config
gcloud api-gateway api-configs describe $CONFIG_ID \
  --api=$API_ID --project=$PROJECT_ID

# Deploy

export GATEWAY_ID=lingualog-api-gateway
export GCP_REGION=us-central1

## create
#gcloud api-gateway gateways create $GATEWAY_ID \
#  --api=$API_ID --api-config=$CONFIG_ID \
#  --location=$GCP_REGION --project=$PROJECT_ID

## update
gcloud api-gateway gateways update $GATEWAY_ID \
  --api-config=$CONFIG_ID --api=$API_ID --location=$GCP_REGION --project=$PROJECT_ID

# Show info
gcloud api-gateway gateways describe $GATEWAY_ID \
  --location=$GCP_REGION --project=$PROJECT_ID
```
