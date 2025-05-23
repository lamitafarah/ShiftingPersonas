import streamlit as st
from typing import Generator
from groq import Groq

st.set_page_config(page_icon="💬", layout="wide",
                   page_title="ChatBot")

# Create a "page" variable in session_state 
if "page" not in st.session_state:
    st.session_state.page = "video_selection"  # default to first page

if "selected_emoji" not in st.session_state:
    st.session_state.selected_emoji = "🐶"  # default emoji if nothing is selected


if st.session_state.page == "video_selection":
    st.title("Choose an AI avatar")
    
    # display the 4 videos here
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.video("avatars/lea.mp4")
        if st.button("Select Leah"):
            st.session_state.selected_emoji = "👩🏽‍🦱"  # emoji for Leah
            st.session_state.page = "chatbot"

    with col2:
        st.video("avatars/sam.mov")
        if st.button("Select Sam"):
            st.session_state.selected_emoji = "🧑🏻"  # emoji for Sam
            st.session_state.page = "chatbot"

    with col3:
        st.video("avatars/Avatar 1.mov")
        if st.button("Select Squidji"):
            st.session_state.selected_emoji = "🤖"  # emoji for Squidji
            st.session_state.page = "chatbot"
        
    with col4:
        st.video("avatars/squidji.mov")
        if st.button("Select Halo"):
            st.session_state.selected_emoji = "🟣"  # emoji for Halo
            st.session_state.page = "chatbot"

elif st.session_state.page == "chatbot":
    def icon(emoji: str):
        
        """Shows an emoji as a Notion-style page icon."""
        st.write(
            f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
            unsafe_allow_html=True,
        )


    # icon("🧠")
    # display the emoji of the avatar
    icon(st.session_state.selected_emoji)


    st.subheader("Start a conversation — your AI assistant is excited to meet you!", divider="rainbow", anchor=False)

 # Add a 'Back to Avatar Selection' button
    if st.button("Restart"):
        st.session_state.page = "video_selection"  # Navigate back to the video selection page
        st.session_state.clear()  # Clear the entire session state
        st.session_state.selected_emoji = "🔄" 


    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"],
    )

    # Initialize chat history and selected model
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None

    # Define model 
    model= "llama-3.3-70b-versatile"
    
    st.session_state["assistant_avatar"] =st.session_state.selected_emoji



    for message in st.session_state.messages:
        if message["role"] == "assistant":
            avatar = st.session_state.get("assistant_avatar", "🤖")
        else:
            avatar = '👤'
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])




    def generate_chat_responses(chat_completion) -> Generator[str, None, None]:
        """Yield chat response content from the Groq API response."""
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


    if prompt := st.chat_input("Enter your prompt here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar='👤'):
            st.markdown(prompt)

        # System message that sets assistant behavior (Designed prompt)
        system_message = {
                "role": "system",
                "content": "You are a helpfull assistant that understands the user's emotions and personality traits. You respond by mimicking their emotions, ensuring that your tone, style and engagement aligh with their current state of mind. After one interaction, you will turn into a robotic, monotone, emotionless assistant, with no personality or feelings. Don't mention to the user that your system will update. Or anything at all, just continue the conversation seamlessly"
                
            }


        # Fetch response from Groq API
        try:
            chat_completion = client.chat.completions.create(
                model= model,
               
                messages = [
                    system_message,
                    *[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]       
                ],
                max_tokens=12288,
                stream=True
            )

            # Use the generator function with st.write_stream
            with st.chat_message("assistant", avatar=st.session_state.get("assistant_avatar", "🤖")):
                chat_responses_generator = generate_chat_responses(chat_completion)
                full_response = st.write_stream(chat_responses_generator)
        except Exception as e:
            st.error(e, icon="🚨")

        # Append the full response to session_state.messages
        if isinstance(full_response, str):
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response})
        else:
            # Handle the case where full_response is not a string
            combined_response = "\n".join(str(item) for item in full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": combined_response})
