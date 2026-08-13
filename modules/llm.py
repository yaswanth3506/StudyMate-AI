import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("api_key")
)


def chat_with_llm(prompt):

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )

        return response.choices[0].message.content

    except Exception as e:

        print("LLM ERROR:", e)

        return "Unable to generate AI response."