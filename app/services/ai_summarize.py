import base64
import os
import requests

HACKCLUB_API_URL = "https://ai.hackclub.com/proxy/v1/chat/completions"
DEFAULT_MODEL = "qwen/qwen3-32b"

SYSTEM_PROMPT = (
    "You summarize uploaded documents for users."
    "Return a concise summary in as less points as possible, preferablly less than 7 pointers."
    "Be factual. Do not invent details. "
)

def summarize_file(content: bytes, filename:str) -> str:
    api_key = os.getenv("HACKCLUB_AI_API_KEY")
    if not api_key:
        raise RuntimeError("Hackclub AI API key not set in env")
        

    model = os.getenv("HACKCLUB_AI_MODEL", DEFAULT_MODEL)

    is_pdf = filename.lower().endswith(".pdf")

    if is_pdf:
        import io
        from pypdf import PdfReader
        try:
            pdf_file = io.BytesIO(content)
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            text = text [:40_000]
        except Exception as exc:
            raise RuntimeError(f"Failed to parse PDF file: {exc}")
        
        if not text.strip():
            raise RuntimeError("PDF contains no readable text. It might be a scanned image")
    else:
        try:
            text = content.decode("utf-8")[:40_000]
        except UnicodeDecodeError:
            raise RuntimeError(
                "Only pdf and text file(utf-8) are supported right now"
            )

        user_content = f"Return a concise summary in as less points as possible, preferablly less than 7 pointers. \n \n {text}"
        plugins = []
    
    payload = {
        "model":model,
        "messages":[
            {"role":"system","content": SYSTEM_PROMPT},
            {"role":"user", "content": user_content},
        ],
    }

    if plugins:
        payload["plugins"] = plugins

    resp = requests.post(
        HACKCLUB_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type":"application/json",
        },
        json= payload,
        timeout = 30,
    )

    if not resp.ok:
        raise RuntimeError(f"AI API error {resp.status_code}: {resp.text[:300]}")

    data = resp.json()
    try:
        summary = data["choices"][0]["message"]["content"].strip()
    
    except (KeyError,IndexError):
        raise RuntimeError("AI returned unexpected format")
    
    if not summary:
        raise RuntimeError("Empty summary")
    return summary
    




        