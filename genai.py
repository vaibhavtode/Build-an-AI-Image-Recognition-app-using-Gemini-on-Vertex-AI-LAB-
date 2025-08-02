from google.cloud import storage
from google import genai
from google.genai.types import HttpOptions, Part

# 1. Download image locally from GCS
def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

# Specify GCS details
bucket_name = "cloud-samples-data"
source_blob_name = "generative-ai/image/scones.jpg"
local_file_path = "scones.jpg"

download_blob(bucket_name, source_blob_name, local_file_path)

# 2. Use the downloaded image in the Gemini API
client = genai.Client(http_options=HttpOptions(api_version="v1"))
with open(local_file_path, "rb") as f:
    image_bytes = f.read()

image_part = Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[
            "What is shown in this image?",
            image_part,
        ],
    )
print(response.text)
