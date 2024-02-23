# Local Multimodal AI Chat
## Overview

Local Multimodal AI Chat is a hands-on project aimed at learning how to build a multimodal chat application. This project is all about integrating different AI models to handle audio, images, and PDFs in a single chat interface. It's a great way for anyone interested in AI and software development to get practical experience with these technologies.

The main purpose here is to learn by doing. You'll see how different pieces like Whisper AI for audio, LLaVA for image processing, and Chroma DB for PDFs come together in a chat application. A full tutorial on how I created this repository can be found on my [youtube channel](https://youtu.be/CUjO8b6_ZuM).
But, this is still a work in progress. There's plenty of room for improvement, and that's where you come in.

I'm really open to pull requests. Whether you have ideas for new features, ways to make the code better, or just want to fix a bug, your contributions are welcome. This project is as much about learning from each other as it is about building something cool.

So, if you're interested in AI chat applications and want to dive into how they're built, join in. Your code and ideas can help make this project better for everyone who wants to learn more about building with AI.

## Features

- **Quantized Model Integration**: This app uses what are called "quantized models." These are special because they are designed to work well on regular consumer hardware, like the kind most of us have at home or in our offices. Normally, the original versions of these models are really big and need more powerful computers to run them. But quantized models are optimized to be smaller and more efficient, without losing much performance. This means you can use this app and its features without needing a super powerful computer. [Quantized Models from TheBloke](https://huggingface.co/TheBloke)

- **Audio Chatting with Whisper AI**: Leveraging Whisper AI's robust transcription capabilities, this app offers a sophisticated audio messaging experience. The integration of Whisper AI allows for accurate interpretation and response to voice inputs, enhancing the natural flow of conversations.
[Whisper models](https://huggingface.co/collections/openai/whisper-release-6501bba2cf999715fd953013)

- **Image Chatting with LLaVA**: The app integrates LLaVA for image processing, which is essentially a fine-tuned LLaMA model equipped to understand image embeddings. These embeddings are generated using a CLIP model, making LLaVA function like a pipeline that brings together advanced text and image understanding. With LLaVA, the chat experience becomes more interactive and engaging, especially when it comes to handling and conversing about visual content. [llama-cpp-python repo for Llava loading](https://github.com/abetlen/llama-cpp-python)

- **PDF Chatting with Chroma DB**: The app is tailored for both professional and academic uses, integrating Chroma DB as a vector database for efficient PDF interactions. This feature allows users to engage with their own PDF files locally on their device. Whether it's for reviewing business reports, academic papers, or any other PDF document, the app offers a seamless experience. It provides an effective way for users to interact with their PDFs, leveraging the power of AI to understand and respond to content within these documents. This makes it a valuable tool for personal use, where one can extract insights, summaries, and engage in a unique form of dialogue with the text in their PDF files. [Chroma website](https://docs.trychroma.com/)


## Getting Started

To get started with Local Multimodal AI Chat, clone the repository and follow these simple steps:

1. **Create a Virtual Environment**: I am using Python 3.10.12 currently

2. **Upgrade pip**: ```pip install --upgrade pip```

3. **Install Requirements**: ```pip install -r requirements.txt```
   
   **Windows Users:** The installation might differ a bit for you, if you encounter errors you can't solve, please open an Issue here on github.

4. **Setting Up Local Models**: Download the models you want to implement. [Here](https://huggingface.co/mys/ggml_llava-v1.5-7b/tree/main) is the llava model I used for image chat (ggml-model-q5_k.gguf and mmproj-model-f16.gguf). 
And the [quantized mistral model](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF) form TheBloke (mistral-7b-instruct-v0.1.Q5_K_M.gguf).

5. **Customize config file**: Check the config file and change accordingly to the models you downloaded.

6. **Optional - Change Profile Pictures**: Place your user_image.pnd and/or bot_image.png inside the chat_icons folder. 

7. **Enter commands in terminal**: 
   1. ```python3 database_operations.py``` This will initialize the sqlite database for the chat sessions.
   2. ```streamlit run app.py```


## Changelog
### 17.02.2024:
- **Input Widget Update**: Replaced st.text_input with st.chat_input to enhance interaction by leveraging a more chat-oriented UI, facilitating user engagement.
- **Sidebar Adjustment**: Relocated the audio recording button to the sidebar for a cleaner and more organized user interface, improving accessibility and user experience.

### 10.02.2024:
- **License Added**: Implemented the GNU General Public License v3.0 to ensure the project is freely available for use, modification, and distribution under the terms of this license. A comprehensive copyright and license notice has been included in the main file (app.py) to clearly communicate the terms under which the project is offered. This addition aims to protect both the contributors' and users' rights, fostering an open and collaborative development environment. For full license details, refer to the LICENSE file in the project repository.
- **Caching for Chat Model**: Introduced caching for the chat model to prevent it from being reloaded with every script execution. This optimization significantly improves performance by reducing load times 
- **Config File Expansion**: Expanded the configuration file to accommodate new settings and features, providing greater flexibility and customization options for the chat application.


### 09.02.2024:

- **SQLite Database for Chat History**: Implemented a SQLite database to store the chat history.
- **Displaying Images and Audio Files in Chat**: Chat history now supports displaying images and audio files.
- **Added Button to delete Chat History**
- **Updated langchain**: Runs now with the current langchain version 0.1.6

### 16.01.2024:
- **Windows User DateTime Format Issue:** Windows users seemed to have problems with the datetime format of the saved JSON chat histories. I changed the format in the `ultis.py` file to `"%Y_%m_%d_%H_%M_%S"`, which should solve the issue. Feel free to change it to your liking.
- **UI Adjustment for Chat Scrolling:** Scrolling down in the chat annoyed me, so the text input box and the latest message are at the top now.

### 12.01.2024:
- **Issue with Message Sending:** After writing in the text field and pressing the send button, the LLM would not generate a response. 
- **Cause of the Issue:** This happened because the `clear_input_field` callback from the button changes the text field value to an empty string after saving the user question. However, changing the text field value triggers the callback from the text field widget, setting the `user_question` to an empty string again. As a result, the LLM is not called.
- **Implemented Workaround:** As a workaround, I added a check before changing the `user_question` value.

## Possible Improvements
- ~~Add Model Caching.~~
- ~~Add Images and Audio to Chat History Saving and Loading.~~
- ~~Use a Database to Save the Chat History.~~
- Integrate Ollama, OpenAI, Gemini, or Other Model Providers.
- Add Image Generator Model.
- Authentication Mechanism.
- Change Theme.
- Separate Frontend and Backend Code for Better Deployment.

## Contact Information

For any questions, please contact me at:

- Email: leonsander.consulting@gmail.com
- Twitter: [@leonsanderai](https://twitter.com/leonsanderai)
