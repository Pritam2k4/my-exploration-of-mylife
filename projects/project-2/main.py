import gradio as gr
from transformers import pipeline

def chatbot_interface(user_input, history):
    chat_pipeline = pipeline("conversational", model="facebook/blenderbot-400M-distill")
    conversation = history + [[user_input, ""]]
    response = chat_pipeline(user_input)[0]['generated_text']
    conversation[-1][1] = response
    return "", conversation

def clear_history():
    return []

def main():
    with gr.Blocks() as demo:
        gr.Markdown("# Python AI Assistant")
        chatbox = gr.Chatbot(label="Chat with AI")
        user_input = gr.Textbox(placeholder="Type your message here...", label="Your Message")
        clear_button = gr.Button("Clear Chat")
        send_button = gr.Button("Send")

        history_state = gr.State([])

        send_button.click(
            chatbot_interface,
            inputs=[user_input, history_state],
            outputs=[user_input, chatbox]
        )
        clear_button.click(clear_history, outputs=chatbox)

    demo.launch()

if __name__ == "__main__":
    main()

