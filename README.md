## Shifting Personas
This study investigates the influence of AI’s human-like persona and embodiment on user perception, engagement, and decision-making. Through the development and testing of various AI avatars, this project examines the impact of visual design and conversational style on user experiences. 
The interactive experiment utilised Groq's high-performance API for real-time natural language processing, the LLaMA model for diverse conversational responses, and Streamlit for a responsive user interface, creating a seamless platform for participant interactions.

### Requirements
- Streamlit
- Groq Python SDK
- Python 3.7+

###  Setup and Installation

#### 1. Install Dependencies

```bash
pip install streamlit groq
```
#### 2. Set Up Groq API Key
Ensure you have an API key from Groq. Store it securely using Streamlit's secrets management by creating a file at:
```bash
.streamlit/secrets.toml
```
With the following content:
```
GROQ_API_KEY = "your_api_key_here"
```

### Run the App
Navigate to the app's directory and run:

```bash
streamlit run streamlit_app.py
```
### Usage
Start by double-clicking on an AI avatar. You will be redirected to the chat interface, where you can interact with the AI agent in real time.
