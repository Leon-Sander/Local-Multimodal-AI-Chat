from datetime import datetime
import base64
import yaml
import requests
from dotenv import load_dotenv
import os
load_dotenv()


def list_openai_models():
    response = requests.get("https://api.openai.com/v1/models", headers={"Authorization": f"Bearer {os.getenv("OPENAI_API_KEY")}"}).json()
    if response.get("error", False):
        return [item["id"] for item in response["data"]]
    else:
        return ["gpt-4o-mini"]


def list_ollama_models():
    json_response = requests.get(url = "http://ollama:11434/api/tags").json()
    models = [model["name"] for model in json_response["models"] if "embed" not in model["name"]]
    return models

def load_config(file_path = "config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)
    
def convert_bytes_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode("utf-8")
    
def convert_bytes_to_base64_with_prefix(image_bytes):
    return "data:image/jpeg;base64," + convert_bytes_to_base64(image_bytes)

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_avatar(sender_type):
    if sender_type == "user":
        return "chat_icons/user_image.png"
    else:
       return "chat_icons/bot_image.png"