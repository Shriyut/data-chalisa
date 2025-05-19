### Build image locally
docker build -t gcr.io/us-gcp-ame-con-ff12d-npd-1/sample-script .

### Push the image to artifact registry
docker push gcr.io/us-gcp-ame-con-ff12d-npd-1/sample-script

### Deploy cloud run service
gcloud run deploy sample-script \
       --image gcr.io/us-gcp-ame-con-ff12d-npd-1/sample-script:latest \
       --platform managed \
       --region us-east4


gcloud run deploy sample-script --image gcr.io/us-gcp-ame-con-ff12d-npd-1/sample-script:latest --platform managed --region us-east4 --set-env-vars test=value,newtest=newvalue

### Trigger the cloud run service
curl -H "Authorization: bearer $(gcloud auth print-identity-token)" https://sample-script-993650900751.us-east4.run.app

curl -H "Authorization: bearer $(gcloud auth print-identity-token)" https://sample-script-993650900751.us-east4.run.app/name?name=sunny

curl -H "Authorization: bearer $(gcloud auth print-identity-token)" \
"https://sample-script-993650900751.us-east4.run.app/names?name=sunny&nicknames=sj&nicknames=shriyut"


curl -X POST "https://sample-script-993650900751.us-east4.run.app/sentences" \
-H "Content-Type: application/json" \
-d '{"sentences": ["Hello World", "FastAPI is awesome"]}'

curl -X POST "https://sample-script-993650900751.us-east4.run.app/deidentify" \
-H "Authorization: Bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json"

curl -X POST "https://sample-script-993650900751.us-east4.run.app/reidentify" \
-H "Authorization: Bearer $(gcloud auth print-identity-token)" \
-H "Content-Type: application/json"


#### In KmsWrappedCryptoKey, 'crypto_key_name': must be from location 'global'.