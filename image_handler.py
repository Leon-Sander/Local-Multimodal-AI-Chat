from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
import base64

def convert_bytes_to_base64(image_bytes):
    encoded_string=  base64.b64encode(image_bytes).decode("utf-8")
    return "data:image/jpeg;base64," + encoded_string

def handle_image(image_bytes, user_message):

    chat_handler = Llava15ChatHandler(clip_model_path="./models/llava/mmproj-model-f16.gguf")
    llm = Llama(
    model_path="./models/llava/llava_ggml-model-q5_k.gguf",
    chat_handler=chat_handler,
    logits_all=True,
    n_ctx=1024 # n_ctx should be increased to accomodate the image embedding
    )
    image_base64 = convert_bytes_to_base64(image_bytes)

    output = llm.create_chat_completion(
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

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string=  base64.b64encode(image_file.read()).decode("utf-8")
        return "data:image/jpeg;base64," + encoded_string
    
if __name__ == "__main__":
    image_path = "Image26.jpg"
    image_base64 = convert_image_to_base64(image_path)
    with open("image.txt", "w") as f:
        f.write(image_base64)