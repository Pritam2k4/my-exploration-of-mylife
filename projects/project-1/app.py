
from transformers import pipeline

# Load the text-to-text generation pipeline
chat_model = pipeline("text2text-generation", model="facebook/blenderbot-3B")

def chat():
    print("Chatbot ready! Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye!")
            break
        response = chat_model(
    user_input,
    max_length=100,
    temperature=0.3,   # Lower = more deterministic
    top_p=0.9
)[0]['generated_text']


if __name__ == "__main__":
    chat()




