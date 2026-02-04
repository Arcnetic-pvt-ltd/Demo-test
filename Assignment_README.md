
# AI Engineering Assignment

## 📌 Project Overview

This project demonstrates the implementation of a hybrid AI processing pipeline combining cloud-based inference and local transformer inference.

Parts implemented:
- Part A – Cloud AI Agent (Inference API)
- Part B – Local Transformer Agent
- Part C – Hybrid Pipeline
- Part D – Performance Comparison

The objective is to analyze performance trade-offs and demonstrate efficient AI pipeline design.

----------------------------------------------------------------------------------------

## 📁 Project Directory Structure

```
Demo-test/
│
├── README.md                 # Main project documentation
├── Assignment_README.md      # Assignment report (this file)
│
├── ai_agents/
│   ├── agent_cloud.py        # Part A - Cloud Agent
│   ├── agent_local.py        # Part B - Local Agent
│   └── hybrid_audit.py       # Part C - Hybrid Pipeline
│
├── requirements.txt
└── .env
```

----------------------------------------------------------------------------------------

## 🏗 System Requirements

- Python 3.10+
- HuggingFace Account & API Token
- Internet connection (for cloud inference)

----------------------------------------------------------------------------------------

## Installed Libraries

huggingface-hub  
sentence-transformers  
torch  
pydantic  
python-dotenv  
requests  

----------------------------------------------------------------------------------------

## Environment Setup

Create a `.env` file in the project root:

```
HUGGINGFACE_TOKEN=your_huggingface_api_token
HF_TOKEN=your_huggingface_api_token
```

Install dependencies:

```
pip install -r requirements.txt
```

----------------------------------------------------------------------------------------

# Part A — Cloud Agent

## Description

Part A implements a cloud-based AI agent using HuggingFace Inference API.  
The agent processes raw website text and extracts structured metadata.

## Features

- API-based inference
- Structured JSON output
- External cloud computation

## Performance

Execution Time: **1.67 seconds**

## Reason for Higher Time

Cloud inference includes:
- Network latency
- API routing and authentication
- Model queueing
- Server-side inference
- Response parsing

These factors increase overall execution time.

## How To Run (Part A)

From project root: python ai_agents/agent_cloud.py

----------------------------------------------------------------------------------------

# Part B — Local Transformer Agent

## Description

Part B uses a local transformer model (`all-MiniLM-L6-v2`) to generate embeddings and perform semantic processing.

## Features

- Offline processing after model download
- Fast embedding generation
- Similarity computation support

## Performance

Execution Time: **0.03 seconds**

## Reason for Faster Execution

Local inference avoids:
- Network delays
- API overhead
- Cloud queue latency

Once the model is loaded into memory, embedding generation is executed directly on the local machine.

## How To Run (Part B)

From project root: python ai_agents/agent_local.

----------------------------------------------------------------------------------------

# Part D — Performance Comparison

| Method               | Execution Time |
|----------------------|----------------|
| Cloud Agent (Part A) | 1.67 seconds   |
| Local Agent (Part B) | 0.03 seconds   |

### Observation

Local inference is significantly faster, while cloud inference provides scalability and access to powerful hosted models.

----------------------------------------------------------------------------------------

# Part C — Hybrid Pipeline

## Objective

Combine local filtering and cloud inference into a single intelligent processing pipeline.


## Hybrid Workflow

```
Input Text
     ↓
Local Relevance Check (SEO keywords)
     ↓
Cloud Summarization
     ↓
Pydantic Validation
     ↓
Final Output
```

## Hybrid Benefits

- Reduced cloud API usage
- Faster response for irrelevant input
- Lower operational cost
- Production-grade AI pipeline design


## How To Run (Part C)

From project root: python ai_agents/hybrid_audit.py

----------------------------------------------------------------------------------------

## Conclusion

This assignment demonstrates efficient AI pipeline design by combining cloud intelligence with fast local processing. Performance benchmarking highlights the trade-offs between scalability and speed, validating the need for hybrid AI architectures in real-world applications.

----------------------------------------------------------------------------------------

## 👨‍💻 Author

Binil K Joseph
Full Stack Developer Intern
Arcnetic Pvt.Ltd
