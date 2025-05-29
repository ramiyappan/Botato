import streamlit as st
from agent import agent_graph
import time
from utils.logger import setup_logger
import uuid
from langchain_core.messages import HumanMessage

# --- Logger ---
logger = setup_logger("app")

st.markdown(
    """
    <style>
        .fixed-title {
            position: fixed;
            width: 100%;
            top: 50px;
            font-size: 35px;
            font-weight: bold;
            color: white;
            padding: 10px 20px;
            z-index: 1000;
        }
        .chat-container {
            position: fixed;
            bottom: 60px; /* Leaves space for input */
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="fixed-title">Botato 🥔</div>', unsafe_allow_html=True)
st.markdown('<div class="chat-container"></div>', unsafe_allow_html=True)

def initialize_session():
    """Initialize session state variables to avoid redundant processing."""
    # Store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Store thread ID
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    # Initialize Agent
    if "agent" not in st.session_state:
        st.session_state.agent = agent_graph()

def display_messages():
    """Displays the chat history with appropriate alignment for user and assistant messages."""
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.markdown(f'<div style="text-align: right; padding: 8px; border-radius: 10px; width: fit-content; max-width: 100%; margin-left: auto;">{message["content"]}</div>', unsafe_allow_html=True)
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.markdown(f'<div style="text-align: left; padding: 8px; border-radius: 10px; width: fit-content; max-width: 100%; margin-right: auto;">{message["content"]}</div>', unsafe_allow_html=True)

def process_agent_response(messages, config):
    """Handles the agent's response and updates the chat interface."""
    
    try:
        with st.chat_message("assistant"):
            response_container = st.empty()

            with st.spinner("Thinking..."):
                response = st.session_state.agent.invoke({"messages": messages}, config)
                response_text = response["messages"][-1].content

                logger.info(f"Received response from assistant: {response_text}")

                lines = response_text.split("\n")
                streamed_text = ""

                # Stream lines
                for line in lines:
                    words = line.split()
                    # Stream words within a line
                    for word in words:
                        streamed_text += word + " "
                        
                        response_container.markdown(
                            f'''
                            <div style="text-align: left; padding: 8px; border-radius: 10px; width: fit-content; max-width: 100%; margin-right: auto;">
                                {streamed_text}
                            </div>
                            ''',
                            unsafe_allow_html=True
                        )
                        time.sleep(0.02)  # inner delay between words

                    streamed_text += "\n"
                    time.sleep(0.05) 

    except Exception as e:
        error_message = f"❌ Error executing query: {str(e)}"
        logger.exception(f"Error executing query: {str(e)}")
        st.markdown(error_message)
    
    st.session_state.messages.append({"role": "assistant", "content": response_text})

def chat_interface():
    """Handles the chat interface and user interactions."""

    if len(st.session_state.messages) == 0:
        st.session_state.messages.append({"role": "assistant", "content": "How can I assist you today?"})

    display_messages()
    
    user_input = st.chat_input("Send a message")

    if user_input:
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        messages = [HumanMessage(content=user_input)]

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f'<div style="text-align: right; padding: 8px; border-radius: 10px; width: fit-content; max-width: 100%; margin-left: auto;">{user_input}</div>', unsafe_allow_html=True)

        logger.info(f"Starting session with thread ID: {config['configurable']['thread_id']}")
        process_agent_response(messages, config)

def main():
    """Main function to run the Streamlit app."""
    initialize_session()  
    chat_interface()     

if __name__ == "__main__":
    main()