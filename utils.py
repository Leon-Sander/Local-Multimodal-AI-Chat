from datetime import datetime
import base64
import yaml

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