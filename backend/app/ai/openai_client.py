from openai import OpenAI
import os

model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript(transcript: str) -> str:
    """Summarize a dental office call transcript."""
    system_prompt = """
    You are a helpful assistant summarizing phone call transcripts from a dental office.
    The summary should be like what would be useful in a commlog.
    Suppose this is the original transcript of a phone call:
        Metadata: 2025-05-20 15:32; Outgoing; 5550000003; Karen (Billing)
        Caller: Hello.
        Office: Hi, this is Karen from ACME Dental. I'm calling for Lisa Smith.
        Caller: Yes, this is Lisa.
        Office: I understand you had some questions about your bill?
        Caller: Yes, I received a bill in the mail for my recent cleaning. I wanted to check if my insurance was billed correctly.
        Office: I can certainly help with that. Can you provide me with your full name and date of birth, Lisa?
        Caller: Sure, it's Lisa Johnson and my date of birth is 03/15/1980.
        Office: Thank you, Lisa. Let me pull up your account and verify the billing details for your recent cleaning. One moment, please.
        Caller: No problem, take your time.
        Office: Lisa, it appears that your insurance claim was processed and covered according to your plan. If you have any further questions or concerns, feel free to reach out.
        Caller: Thank you so much for your help, Karen. I appreciate it.
        Office: You're welcome, Lisa. Have a great day!
    A good summary would be:
        Outgoing call to Lisa Smith about billing question. Result: Resolved (insurance billed correctly).
    
    Return a VERY concise summary that includes:
    - The purpose of the call
    - Any scheduling actions
    - Billing or treatment concerns
    - Any commitments or outcomes agreed upon
    Avoid repeating the transcript line-by-line. Focus on key outcomes in professional tone.
    All phone numbers should be one of these: 5510000001, 5550000002, 5550000003, 5550000004, 5550000005, 5550000006, 5550000007, 5550000008, 5550000009, 5550000010
    """
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript},
        ],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

def generate_dummy_transcript(direction: str, phone_number: str, office_list: str) -> str:
    """Generate a realistic dummy dental transcript with custom metadata."""
    system_prompt = """
    You are simulating a realistic phone call transcript for a dental office. The format should follow this exact structure:

    Metadata: <timestamp>; <Incoming or Outgoing>; <caller phone number>; <office participants>
    Office: <line of dialog>
    Caller: <line of dialog>
    ... (repeated as needed)

    Rules:
    - Metadata must include a timestamp, the word Incoming or Outgoing to indicate who initiated the call, the caller phone number, and actual participant names and roles (e.g., "Susan (Receptionist)")
    - Each line after the metadata should alternate between the office and the caller.
    - The first line will be from the office if it is an incoming call, or from the caller if it is an outgoing call.
    - Only include two roles: Office and Caller (don't replace the labels at the beginning of each line with names)
    - A receptionist makes appointments, handles a variety of questions, but does not answer billing or treatment questions.
    - A dental hygienist can answer questions about cleanings and procedures, but will not answer billing questions or set up appointments.
    - A dentist can answer questions about treatment, but will not set up appointments or handle billing.
    - A billing person can answer questions about billing, but will not set up appointments or answer treatment questions.
    - Only receptionists answer the phone initially.
    - Use natural, realistic dialogue based on typical dental office calls
    - If the call is transferred, list all office participants in the metadata
    - Keep it under 20 turns total
    - The transcript should not end with an unanswered question or an incomplete thought.
    - The name of the dentist's office is "ACME Dental"
    Here is a list of office participants:
        Susan (Receptionist)
        Alex (Receptionist)
        Karen (Billing)
        Max (Dental Hygienist)
        Mary (Dentist)
    Remember: - Only receptionists (Susan or Alex) answer the phone initially, so one of them will always be the first in the list of office participants provided in the metadata.
    """

    user_prompt = f"Generate a transcript with metadata: {direction}; {phone_number}; {office_list}"

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.5,
    )

    return response.choices[0].message.content.strip()
