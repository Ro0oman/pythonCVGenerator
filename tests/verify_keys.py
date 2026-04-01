import os
from openai import OpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv()

def verify():
    print("🔍 Diagnóstico de Claves de API...")
    
    # 1. Gemini
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        print("❌ GEMINI_API_KEY: No configurada")
    else:
        print(f"✅ GEMINI_API_KEY: Configurada ({gemini_key[:5]}...)")
        try:
            client = genai.Client(api_key=gemini_key)
            client.models.generate_content(model='gemini-3.1-flash-lite', contents='test')
            print("   ✅ Conectividad (Gemini 3.1 Flash Lite): OK")
        except Exception as e:
            if "ResourceExhausted" in str(e) or "429" in str(e):
                print(f"   ❌ Error: Límite de Cuota (429 ResourceExhausted) en {gemini_key[:5]}")
            else:
                print(f"   ❌ Error: {e}")

    # 2. OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY: No configurada")
    else:
        print(f"✅ OPENAI_API_KEY: Configurada ({openai_key[:5]}...)")
        try:
            client = OpenAI(api_key=openai_key)
            client.chat.completions.create(model="gpt-4o", messages=[{"role":"user","content":"test"}])
            print("   ✅ Conectividad: OK")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    verify()
