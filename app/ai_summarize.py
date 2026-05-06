import base64
import os
import requests

HACKCLUB_API_URL = "https://ai/hackclub.com/proxy/v1/chat/completions"
DEFAULT_MODEL = "qwen/qwen3.6-35b-a3b"

SYSTEM_PROMPT = (
    "You summarize uploaded documents for users."
    "Return a concise summary in as less points as possible, preferablly less than 7 pointers."
    "Be factual. Do not invent details. "
)

def summarize_file(content: bytes, filename:str) -> str:
    api_key = os.getenv("HACKCLUB_AI_API_KEY")
    if not api_key:
        raise RuntimeError("Hackclub AI API key not set in env")
        

        model = os.getenv("HACKCLUB_AI_MODEL", DEFAULT_MODEL, "qwen/qwen3-32b" )

        is_pdf = filename.lower().endswith(".pdf")

        if is_pdf:
            b64 = base64.b64encode(content).decode("utf-8")
            file_data = f"data:application/pdf;base64,{b64}"
            user_content = [
                {"type": "text","text": "Return a concise summary in as less points as possible, preferablly less than 7 pointers."},
                {
                    "type":"file",
                    "file":{
                        "filename":filename,
                        "file_data": file_data,
                    },
                },
            ]
            plugins = [{"id":"file-parser", "pdf":{"engine": "native"}}]
        else:
            try:
                text = content.decode("utf-8")[:40_000]
            except UnicodeDecodeError:
                raise RuntimeError(
                    "Only pdf and text file(utf-8) are supported right now"
                )

            user_content = f"Return a concise summary in as less points as possible, preferablly less than 7 pointers."
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
            raise RuntimeError(f"AI API error {resp.status.code}: {resp.text[:300]}")

        data = resp.json()
        try:
            summary = data["choices"][0]["message"]["content"].strip()
        
        except (KeyError,IndexError):
            raise RuntimeError("AI returned unexpected format")
        
        if not summay:
            raise RuntimeError("Empty summary")
        return summary
        




            