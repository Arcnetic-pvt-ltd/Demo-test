import time
import numpy as np
from sentence_transformers import SentenceTransformer, util

# ---------------------------
# Load Local Embedding Model
# ---------------------------

print("🔌 Loading local transformer model...")

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

print("✅ Model loaded successfully")

# ---------------------------
# Generate Embedding Function
# ---------------------------

def generate_embedding(text: str):
    """
    Convert input text into vector embedding
    """

    print("\n📡 Generating embedding...")

    embedding = model.encode(text, convert_to_tensor=True)

    print("✅ Embedding generated")
    print("📏 Vector dimension:", embedding.shape)

    return embedding


# ---------------------------
# Similarity Calculation
# ---------------------------

def calculate_similarity(text1: str, text2: str):
    """
    Compute cosine similarity between two text inputs
    """

    print("\n📊 Calculating similarity...")

    emb1 = generate_embedding(text1)
    emb2 = generate_embedding(text2)

    similarity_score = util.cos_sim(emb1, emb2)[0][0].item()

    print("✅ Similarity Score:", similarity_score)

    return similarity_score


# ---------------------------
# Integration With Part A Output
# ---------------------------

def embed_part_a_output(part_a_data: dict):
    """
    Convert structured output from cloud agent (Part A)
    into a single semantic embedding
    """

    print("\n🔗 Integrating Part A output with Local Agent...")

    combined_text = f"""
    {part_a_data.get('page_title', '')}
    {part_a_data.get('meta_description', '')}
    {part_a_data.get('company_name', '')}
    {part_a_data.get('email', '')}
    {part_a_data.get('phone', '')}
    {part_a_data.get('domain', '')}
    """

    combined_text = combined_text.strip()

    print("📝 Combined Text For Embedding:")
    print(combined_text)

    embedding = generate_embedding(combined_text)

    return embedding


# ---------------------------
# Local Benchmark Test (Part D)
# ---------------------------

if __name__ == "__main__":

    print("\n🚀 Running Local Embedding Agent Benchmark")

    # SAME INPUT USED IN PART A (IMPORTANT)
    benchmark_text = """
SEO and Crawling are essential components of modern website optimization.
Search engines use crawlers to index web pages efficiently.
Businesses use SEO techniques to improve online visibility.
Contact us at support@spider.com.
"""

    # -------- Measure Local Execution Time --------

    start_time = time.time()

    embedding = generate_embedding(benchmark_text)

    end_time = time.time()

    print("\n⏱ Local Execution Time:", round(end_time - start_time, 2), "seconds")

    print("\n📏 Final Vector Dimension:", embedding.shape)
