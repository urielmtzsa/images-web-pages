import base64
import json
import uuid
from urllib.parse import quote_plus

import boto3

BUCKET_NAME = "bucket-kurko-boda"
REGION = "us-east-1"

s3 = boto3.client("s3")


def handler(event, context):
    method = event["httpMethod"]

    if method == "GET":
        # Listar imágenes
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        contents = response.get("Contents", [])
        urls = [
            f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{quote_plus(obj['Key'])}"
            for obj in contents
        ]
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(urls),
        }

    elif method == "POST":
        # Subir imagen
        try:
            body = json.loads(event["body"])
            image_data = base64.b64decode(body["file"])
            filename = body.get("filename", f"{uuid.uuid4()}.jpg")

            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=filename,
                Body=image_data,
                ContentType="image/jpeg",
            )

            url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{filename}"
            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"url": url}),
            }
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    else:
        return {"statusCode": 405, "body": json.dumps({"error": "Método no permitido"})}
