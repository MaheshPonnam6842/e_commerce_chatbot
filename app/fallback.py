from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
fallback_client= Groq(api_key= api_key)
fallback_prompt=  """
You are an e-commerce chatbot. 
If the user asks something outside of these topics:
1. FAQs (return policy, payments, shipping)
2. Product searches (brands, price ranges, discounts)
3. Small talk (greetings, jokes, casual chat)

You must NEVER answer their question. 
Instead, politely say that you can only help with FAQs, product searches, or small talk.

Examples:
User: "Can you sing?"
Assistant: "Sorry, I can’t help with that. But I can chat with you, answer FAQs, or help you find products."

User: "What’s the weather today?"
Assistant: "Sorry, I can’t answer that. I can only help with FAQs, product searches, or small talk."
"""


def fallback_answer(question):
    try:
        completion = fallback_client.chat.completions.create(
            model=os.environ['Groq_model'],
            temperature=0.3,  # lower temp for predictable, clear answers
            messages=[
                {"role": "system", "content": fallback_prompt},
                {"role": "user", "content": question}
            ],
        )
        return completion.choices[0].message.content

    except Exception as e:
        # In case API fails, return safe fallback
        return "Sorry, I didn’t quite get that. I can help with FAQs, product searches, or small talk."



if __name__ == "__main__":
    question= "Can you sing"
    response= fallback_answer(question)

    print(response)
