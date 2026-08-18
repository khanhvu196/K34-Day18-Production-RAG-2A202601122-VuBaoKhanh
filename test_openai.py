import os, sys
from dotenv import load_dotenv
from openai import OpenAI

# Ép console Python sử dụng UTF-8 trên Windows để không bị lỗi chữ tiếng Việt
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Tai bien moi truong tu file .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
    print("[Error] Bạn chưa điền API Key vào file .env!")
    exit(1)

print(f"[Info] Tim thay API Key: {api_key[:10]}...{api_key[-4:] if len(api_key) > 4 else ''}")

try:
    # Neu dung Gemini qua cong OpenAI, thu vien OpenAI() se tu dong lay base_url tu file .env
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model_name = "gemini-3.6-flash" if "googleapis.com" in base_url else "gpt-4o-mini"
    
    print(f"[Info] Dang thu ket noi toi {base_url} bang model {model_name}...")
    
    client = OpenAI()
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "user", "content": "Xin chao, phan hoi ngan gon bang 5 tu de test ket noi."}
        ],
        timeout=10
    )
    print("[Success] Ket noi THANH CONG!")
    print(f"[AI Response] Phan hoi tu AI: {response.choices[0].message.content}")
except Exception as e:
    print("[Fail] Ket noi THAT BAI!")
    print(f"[Details] Chi tiet loi: {e}")
