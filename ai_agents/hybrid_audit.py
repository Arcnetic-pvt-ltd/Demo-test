import os
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from pydantic import BaseModel, ValidationError

# -------------------------------
# Load Environment Variables
# -------------------------------

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

if not HF_TOKEN:
    raise ValueError("❌ HUGGINGFACE_TOKEN not found in environment")

# -------------------------------
# HuggingFace Chat Model Setup
# -------------------------------

MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

client = InferenceClient(
    token=HF_TOKEN
)

print("✅ Hybrid Pipeline Initialized")

# -------------------------------
# Step 3 — Pydantic Model
# -------------------------------

class SummarySchema(BaseModel):
    summary: str


# -------------------------------
# Step 1 — Local SEO Relevance Check
# -------------------------------

def is_seo_relevant(text: str) -> bool:

    keywords = ["seo", "crawling"]

    text_lower = text.lower()

    for keyword in keywords:
        if keyword in text_lower:
            return True

    return False


# -------------------------------
# Step 2 — Cloud Summarization (CHAT API)
# -------------------------------

def summarize_text_cloud(text: str) -> str:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a professional summarization assistant."
            },
            {
                "role": "user",
                "content": f"Summarize the following text in 2-3 sentences:\n{text}"
            }
        ],
        max_tokens=150,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


# -------------------------------
# Hybrid Pipeline Runner
# -------------------------------

def run_hybrid_audit(input_text: str):

    print("\n🚀 Starting Hybrid Audit Pipeline")

    start_time = time.time()

    # -------- Step 1: Local Logic --------

    print("🔍 Running local relevance check...")

    if not is_seo_relevant(input_text):
        print("❌ Text is NOT SEO relevant")

        end_time = time.time()

        return {
            "status": "rejected",
            "reason": "Not SEO related",
            "time_taken": round(end_time - start_time, 2)
        }

    print("✅ Text is SEO relevant")

    # -------- Step 2: Cloud Summary --------

    print("☁ Sending text to cloud summarizer...")

    summary = summarize_text_cloud(input_text)

    print("📥 Raw Summary Output:")
    print(summary)

    # -------- Step 3: Pydantic Validation --------

    print("🧪 Validating summary output...")

    try:
        validated = SummarySchema(summary=summary)

        end_time = time.time()

        print("✅ Validation successful")

        return {
            "status": "success",
            "summary": validated.summary,
            "time_taken": round(end_time - start_time, 2)
        }

    except ValidationError as e:

        end_time = time.time()

        print("❌ Validation failed")

        return {
            "status": "failed",
            "error": str(e),
            "time_taken": round(end_time - start_time, 2)
        }


# -------------------------------
# Test Run
# -------------------------------

if __name__ == "__main__":

    test_input = """
SEO and Crawling are important components of website optimization.
Search engines use crawlers to index web pages efficiently.
"""

    result = run_hybrid_audit(test_input)

    print("\n🎯 Final Output:")
    print(result)
