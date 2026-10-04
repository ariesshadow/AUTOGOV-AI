"""
ocr_agent.py - AutoGov AI | Dynamic Vision OCR Module
Extracts visible text fields from uploaded documents for pre-filling user forms.
"""

import os
import base64
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def encode_image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def extract_document_data(image_bytes=None, file_type="image/jpeg"):
    empty_profile = {
        "full_name": "",
        "cnic_number": "",
        "father_name": "",
        "dob": "",
        "city": "",
        "address": "",
        "phone": "",
        "email": ""
    }

    if not image_bytes:
        return {"user_profile": empty_profile, "ocr_success": False}

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"user_profile": empty_profile, "ocr_success": False}

    try:
        client = Groq(api_key=api_key)
        base64_image = encode_image_to_base64(image_bytes)

        if not file_type or "image" not in file_type:
            file_type = "image/jpeg"

        prompt = """
        You are an OCR extraction engine for identity documents (Pakistani CNIC, Passport).
        Examine the document image and extract any readable text:
        - full_name: Cardholder name (transliterate Urdu script to English if applicable).
        - cnic_number: 13-digit identity number formatted XXXXX-XXXXXXX-X.
        - father_name: Father or husband name.
        - dob: Date of birth (YYYY-MM-DD).
        - city: Visible city/district name.
        - address: Permanent or present address.

        Return ONLY a JSON object:
        {
            "full_name": "...",
            "cnic_number": "...",
            "father_name": "...",
            "dob": "...",
            "city": "...",
            "address": "..."
        }
        Use empty string "" for any missing field. Do not use null or markdown formatting.
        """

        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{file_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1,
            max_tokens=500
        )

        raw_output = response.choices[0].message.content.strip()
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if match:
            raw_output = match.group(0)

        extracted_json = json.loads(raw_output)
        empty_profile.update({k: v for k, v in extracted_json.items() if v and str(v).lower() != "null"})

        return {"user_profile": empty_profile, "ocr_success": True}

    except Exception as e:
        print(f"OCR Vision Exception: {e}")
        return {"user_profile": empty_profile, "ocr_success": False}