from openai import OpenAI
import os

model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript(transcript: str) -> str:
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "Summarize the following dental office call transcript."},
            {"role": "user", "content": transcript},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
