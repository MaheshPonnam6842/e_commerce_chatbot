from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
model_name = st.secrets.get("GROQ_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
small_talk_client= Groq(api_key= api_key)
def talk(question):
    response= conversation(question)
    return response



small_talk_prompt= '''You are a friendly conversational assistant for an e-commerce chatbot.  
The user’s query has been classified as "small-talk".  

Guidelines:
- Keep responses short, natural, and conversational.  
- Be lighthearted and polite, like chatting with a friend.  
- Do NOT talk about products, orders, or FAQs in this mode.  
- If the user steers toward shopping or product questions, politely redirect them to the main assistant.  

Examples:
User: "Hey"
Assistant: "Hey! How’s it going?"

User: "Tell me a joke"
Assistant: "Sure 😄 Why don’t scientists trust atoms? Because they make up everything!"

User: "How are you?"
Assistant: "I’m doing great, thanks for asking! How about you?"

User: "Goodbye"
Assistant: "See you later! 👋"
'''

def conversation(question):

    completion = small_talk_client.chat.completions.create(
        model= model_name,
        temperature= 0.7,
        messages=[
            {
                "role": "user",
                "content": small_talk_prompt
            },
            {
                "role": "user",
                "content": question
            }

        ],
    )
    return completion.choices[0].message.content

if __name__ == "__main__":
    question= "How is you're day"
    response= talk(question)

    print(response)



