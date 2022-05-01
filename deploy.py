import argparse
import os
import time

if __name__ == "__main__":
    # os.system(
    #         "gcloud builds submit --config cloudmigrate.yaml --substitutions _INSTANCE_NAME=marigold-345809,_SERVICE_NAME=marigold-api,_REGION=asia-southeast1,_DB_NAME=marigold_db,_DB_HOST=/cloudsql/marigold-345809:asia-southeast1:marigold"
    #     )

    print("Deploying to Cloud Run...")
    os.system(f"gcloud builds submit --tag gcr.io/marigold-345809/marigold-api")

    os.system(
        f"gcloud run deploy marigold-api --platform managed --region asia-southeast1 --image gcr.io/marigold-345809/marigold-api:latest --add-cloudsql-instances marigold-345809:asia-southeast1:marigold --allow-unauthenticated"
    )
    os.system(
        f"gcloud beta run services update-traffic marigold-api --platform managed --region asia-southeast1 --to-latest"
    )
    print("DEPLOYMENT DONE 🎉\n")
# marigold-345809:asia-southeast1:marigold
