import os
import json
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import time
# ----------------------------------
# Explicit ENV Loading (Robust)
# ----------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path=ENV_PATH)

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

print("🔍 ENV PATH:", ENV_PATH)
print("🔍 HUGGINGFACE_TOKEN Loaded:", "YES" if HF_TOKEN else "NO")

if not HF_TOKEN:
    raise ValueError("❌ HuggingFace token not found. Set HUGGINGFACE_TOKEN in .env file")

# ----------------------------------
# Model Configuration
# ----------------------------------

MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

print("🔌 Connecting to HuggingFace Inference API (LLaMA)...")

client = InferenceClient(
    token=HF_TOKEN
)

print("✅ Connected to HuggingFace Cloud Inference")

# ----------------------------------
# Cloud Extraction Function
# ----------------------------------

def extract_website_metadata(text: str):

    print("📡 Sending request to cloud model...")

    system_prompt = """
You are an information extraction system.
Return ONLY valid JSON.
"""

    user_prompt = f"""
Extract the following details from the input text if present:

1. Page title
2. Meta description (short website summary)
3. Company or brand name
4. Email address
5. Phone number
6. Website domain name

Return ONLY valid JSON in this format:

{{
  "page_title": "",
  "meta_description": "",
  "company_name": "",
  "email": "",
  "phone": "",
  "domain": ""
}}

Text:
{text}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,
            temperature=0.1
        )

        raw_output = response.choices[0].message.content

        print("📥 Raw model output:")
        print(raw_output)

        # ----------------------------------
        # JSON Parsing
        # ----------------------------------

        parsed_data = json.loads(raw_output.strip())

        print("✅ Parsed JSON Output:")
        print(parsed_data)

        return parsed_data

    except json.JSONDecodeError:
        print("❌ JSON Parsing Error")
        print("Model returned invalid JSON")
        return None

    except Exception as e:
        print("❌ API Error:", e)
        return None


# ----------------------------------
# Local Testing
# ----------------------------------

if __name__ == "__main__":

    print("\n🚀 Running Cloud Agent Test")

    test_text = """
SEO and Crawling are essential components of modern website optimization.
Search engines use crawlers to index web pages efficiently.
Businesses use SEO techniques to improve online visibility.
Contact us at support@spider.com.
"""

    extract_website_metadata(test_text)
    start = time.time()

    result = extract_website_metadata(test_text)

    end = time.time()

    print("⏱ Cloud Execution Time:", round(end - start, 2), "seconds")
