from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
import base64
from utils import load_config
#import streamlit as st
config = load_config()

def convert_bytes_to_base64(image_bytes):
    encoded_string=  base64.b64encode(image_bytes).decode("utf-8")
    return "data:image/jpeg;base64," + encoded_string

#@st.cache_resource # can be cached if you use it often
def load_llava():
    chat_handler = Llava15ChatHandler(clip_model_path=config["llava_model"]["clip_model_path"])
    llm = Llama(
        model_path=config["llava_model"]["llava_model_path"],
        chat_handler=chat_handler,
        logits_all=True,
        n_ctx=1024 # n_ctx should be increased to accomodate the image embedding
        )
    return llm


def handle_image(image_bytes, user_message):

    llava = load_llava()
    image_base64 = convert_bytes_to_base64(image_bytes)

    output = llava.create_chat_completion(
        messages = [
            {"role": "system", "content": "You are an assistant who perfectly describes images."},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_base64}},
                    {"type" : "text", "text": user_message}
                ]
            }
        ]
    )
    print(output)
    return output["choices"][0]["message"]["content"]