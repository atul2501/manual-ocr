import json
import os
import requests


from openai import OpenAI
from dotenv import load_dotenv

from fieldname import InvoiceExtractor

load_dotenv()

def build_invoice_prompt(invoice_text:str) -> str:
    structure=json.dumps(InvoiceExtractor.get_invoice_structure(), indent= 2)


    return f"""
    You are an invoice data extraction specialist

    Extract invoice data from the supplied document text.

    RULES:
    1.Use only information present in the document.
    2.DO not guess or invent missing values.
    3.Return null for missing values.
    4.Preserve invoice number and refernence as strings.
    5.Return invoice number and refernce as string.
    6.Return dates in YYYY-MM-DD format when unabiguous.
    7.Extract every genuine invoice line item.
    8.Do not treak bank details,address,or footer text as line item.
    9.Put additional labelled reference in additional_fields when they do not belong to the main invoice header.
    10. Return valid Json only,Without Markdown
    11.Return JSON with exactly this structure and these keys {structure}

    DOCUMENT TEXT:
    {invoice_text}
    """


def extract_invoice_json(invoice_text: str) -> dict:
    api_key = os.getenv("ollama_api_key")
    model=os.getenv("OLLAMA_MODEL","gemma4:31b")
    base_url=os.getenv("OLLAMA_API_URL","https://ollama.com/")
    chat_url=base_url.rstrip("/") + "/api/chat"

    if not api_key:
        raise ValueError("ollama_api_key is missing from .env")

    response= requests.post(
        chat_url,
        headers={
            "Authorization":f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
                "model": model,
                "messages":[
                    {
                        "role":"user",
                        "content": build_invoice_prompt(invoice_text),
                    }
                ],
                "format":"json",
                "stream":False,
                "options":{"temperature":0}
                },
        timeout=600,
    )

    response.raise_for_status()
    content=response.json()["message"]["content"]
    data=json.loads(content)

    if not isinstance(data.get("invoice_header"),dict):
        raise ValueError("Invalid invoice_header")
    if not isinstance(data.get("line_item"),list):
        raise ValueError("Invalid line_item")

    if not isinstance(data.get("additional_fields"),list):
        raise ValueError("Invalid additional_fields")

    return data    