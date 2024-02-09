import os
import base64

css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 100%;
  padding: 0 1.5rem;
  color: #fff;
}

.chat-message .message img, .chat-message .message audio {
    max-width: 100%; /* Adjust this value as needed */
    border-radius: 0.25rem;
}
'''

def get_bot_template(MSG):
    bot_template = f'''
    <div class="chat-message bot">
        <div class="avatar">
            <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>
        <div class="message">{MSG}</div>
    </div>
    '''
    return bot_template

def get_user_template(MSG):
    if os.path.exists("image.txt"):
        with open("image.txt", "r") as f:
            img_src = f.read()
    else:
        img_src = "https://i.ibb.co/rdZC7LZ/Photo-logo-1.png"
        
    user_template = f'''
    <div class="chat-message user">
        <div class="avatar">
            <img src="{img_src}" width="350" alt="Grab Vector Graphic Person Icon | imagebasket" /></a>
        </div>    
        <div class="message">{MSG}</div>
    </div>
    '''
    return user_template

def get_text_template(MSG, sender_type):
    if sender_type == "human":
        return get_user_template(MSG)
    else:
        return get_bot_template(MSG)

def get_media_template(MSG, media_type, sender_type):
    """
    Generate HTML template for messages, including support for text, image, and audio.
    
    :param MSG: The message content or description for image/audio.
    :param media_type: The type of the content ('text', 'image', 'audio').
    :param src: Source URL for image or audio content.
    :return: HTML template string.
    """
    # Avatar source can be dynamic or fixed based on your requirements
    avatar_src = "https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" if sender_type != 'human' else get_user_image()
    
    media_content = MSG
    if media_type == 'image':
        media_content = f'<img src="{get_image_data_url(MSG)}" alt="Image">'
    elif media_type == 'audio':
        media_content = f'<audio controls><source src="{get_audio_data_url(MSG)}" type="audio/mpeg">Your browser does not support the audio element.</audio>'
    
    template = f'''
    <div class="chat-message {'bot' if sender_type != 'human' else 'user'}">
        <div class="avatar">
            <img src="{avatar_src}" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>    
        <div class="message">{media_content}</div>
    </div>
    '''
    return template

def get_image_data_url(image_bytes, image_format="png"):
    """
    Convert image bytes to a Data URL.
    
    :param image_bytes: Byte representation of the image.
    :param image_format: Format of the image (e.g., 'png', 'jpg').
    :return: Data URL string.
    """
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/{image_format};base64,{base64_image}"

def get_audio_data_url(audio_bytes, audio_format="mpeg"):
    """
    Convert audio bytes to a Data URL.
    
    :param audio_bytes: Byte representation of the audio.
    :param audio_format: Format of the audio (e.g., 'mpeg', 'wav').
    :return: Data URL string.
    """
    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')
    return f"data:audio/{audio_format};base64,{base64_audio}"

def get_user_image():
    if os.path.exists("image.txt"):
        with open("image.txt", "r") as f:
            img_src = f.read()
    else:
        img_src = "https://i.ibb.co/rdZC7LZ/Photo-logo-1.png"
    return img_src