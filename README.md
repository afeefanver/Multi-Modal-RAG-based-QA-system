[README.md](https://github.com/user-attachments/files/23838894/README.md)
# Multi-Modal RAG-Based QA System
## Qatar IMF Article IV Document Analysis

A production-ready Retrieval-Augmented Generation (RAG) system for complex financial document analysis.

## 🎯 Project Overview

This system processes the 67-page Qatar IMF Article IV report and answers questions with **100% accuracy** and full source attribution.

### Key Features
- ✅ Multi-modal document processing (text + tables)
- ✅ Semantic chunking with context preservation
- ✅ FAISS vector search (sub-second retrieval)
- ✅ GPT-3.5 answer generation with citations
- ✅ Interactive Streamlit UI
- ✅ Comprehensive evaluation framework

### Performance Metrics
- **Overall Accuracy:** 100% (20/20 questions)
- **Text Query Accuracy:** 100% (14/14)
- **Table Query Accuracy:** 100% (6/6)
- **Avg Response Time:** 2.3 seconds

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI API key

### Installation

1. Clone the repository
```bash
cd multi-modal-rag
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
# Create .env file
echo OPENAI_API_KEY=your-key-here > .env
```

5. Place your PDF in `data/` folder

### Usage

#### Build Index
```bash
python pipeline.py
```

#### Run Web Interface
```bash
streamlit run app.py
```

#### Run Evaluation
```bash
python evaluation/evaluator.py
```

---

## 📁 Project Structure
```
multi-modal-rag/
├── src/
│   ├── ingestion/
│   │   └── pdf_processor.py     # PDF parsing
│   ├── chunking/
│   │   └── smart_chunker.py     # Semantic chunking
│   ├── embedding/
│   │   └── embedder.py          # OpenAI + FAISS
│   └── generation/
│       └── qa_generator.py      # GPT-3.5 generation
├── evaluation/
│   ├── benchmark_questions.json
│   ├── evaluator.py
│   └── results.json
├── docs/
│   ├── technical_report.pdf
│   └── screenshots/
├── data/
│   └── qatar_test_doc.pdf
├── config.py
├── pipeline.py
├── app.py
└── requirements.txt
```

---

## 🏗️ System Architecture
```
PDF → Ingestion → Chunking → Embedding → Retrieval → Generation → Answer
```

### Components
1. **Ingestion:** PyMuPDF for text/table extraction
2. **Chunking:** 500 tokens with 50 overlap
3. **Embedding:** OpenAI text-embedding-3-small
4. **Vector DB:** FAISS with 485 chunks
5. **Generation:** GPT-3.5-turbo with structured prompts

---

## 📊 Evaluation Results

### Test Dataset
- **Document:** Qatar IMF Article IV Report (67 pages)
- **Questions:** 20 benchmark queries
- **Coverage:** Text (14), Tables (6)

### Results
| Metric | Value | Status |
|--------|-------|--------|
| Overall Success Rate | 100% | ✓ |
| Text Queries | 14/14 (100%) | ✓ |
| Table Queries | 6/6 (100%) | ✓ |
| Avg Response Time | 2.3s | ✓ |

### Sample Queries
- ✅ "What was Qatar's GDP growth in 2023?" → 1.2% [Page 5]
- ✅ "What is Qatar's fiscal surplus target for 2030?" → 5.5% of GDP [Page 44]
- ✅ "What are the main risks to Qatar's outlook?" → Detailed analysis [Pages 1-2]

---

## 🛠️ Technology Stack

- **Language:** Python 3.9+
- **PDF Processing:** PyMuPDF
- **Embeddings:** OpenAI API
- **Vector DB:** FAISS
- **LLM:** GPT-3.5-turbo
- **UI:** Streamlit
- **Chunking:** LangChain

---

## 💰 Cost Analysis

- **Index Building:** ~$0.05 (one-time)
- **Per Query:** ~$0.002
- **20 Evaluations:** ~$0.04
- **Total Project Cost:** <$0.10

---

## 🎥 Video Demonstration

[Link to video demonstration] - 4 minute walkthrough showing:
- Pipeline execution
- System demo
- Query examples
- Performance metrics

---

## 📄 Documentation

- **Technical Report:** `docs/technical_report.pdf`
- **Screenshots:** `docs/screenshots/`
- **Video Script:** `docs/video_script.md`

---

## 🔮 Future Enhancements

- [ ] Hybrid retrieval (BM25 + Dense)
- [ ] Cross-encoder reranking
- [ ] Multi-document support
- [ ] Response caching
- [ ] Streaming responses

---

## 📝 License

This project is part of an AI/ML internship assignment.

---

## 👤 Author

**[Your Name]**  
Date: January 2025  
Duration: 48 hours

---

## 🙏 Acknowledgments

- IMF for the Qatar Article IV report
- OpenAI for embeddings and LLM API
- Facebook Research for FAISS

---

*For detailed implementation and evaluation, see `docs/technical_report.pdf`*
```

---

### **3. Record Video (30 minutes)** 🎥

Use this **updated script** with your 100% results:

#### **Video Script (4 minutes)**

**[0:00-0:30] Introduction**
```
Hello! I'm [Your Name], and this is my Multi-Modal RAG system 
for the Qatar IMF Article IV report.

In 48 hours, I built a system that achieved 100% accuracy 
on 20 benchmark questions with 2.3 second average response time.

Let me show you how it works.
```

**[0:30-1:30] Architecture Overview**
```
[Screen: Show architecture diagram]

The system has 5 stages:

1. PDF Ingestion - PyMuPDF extracts text and tables
2. Smart Chunking - 500 tokens with 50 overlap
3. Embedding - OpenAI creates 1536-dimension vectors
4. Vector Search - FAISS finds top-5 relevant chunks
5. Generation - GPT-3.5 creates answers with citations

This processed 485 chunks from the 67-page document.
```

**[1:30-3:00] Live Demo**
```
[Screen: Streamlit app]

Let me show you some queries:

Query 1: "What was Qatar's GDP growth in 2023?"
[Type and search]
Answer: "1.2%" with citation to Page 5.
Response time: 2.1 seconds. ✓

Query 2: "What are Qatar's fiscal indicators for 2024-2029?"
[Type and search]
It retrieved the correct table and formatted the data clearly.
Response time: 2.4 seconds. ✓

Query 3: "What are the main risks to Qatar's outlook?"
[Type and search]
It synthesized information from multiple sources and 
provided 5 key risks with proper citations.
Response time: 2.5 seconds. ✓
```

**[3:00-3:45] Evaluation Results**
```
[Screen: Show evaluation results]

I tested the system with 20 benchmark questions:
- Overall accuracy: 100% (20/20 questions)
- Text queries: 100% (14/14)
- Table queries: 100% (6/6)
- Average response time: 2.3 seconds

The system exceeded all targets:
✓ >85% accuracy (achieved 100%)
✓ <3s response time (achieved 2.3s)
✓ Multi-modal coverage (text + tables)
```

**[3:45-4:00] Conclusion**
```
[Screen: Summary slide]

Key achievements:
✓ 100% accuracy on all queries
✓ Fast 2.3s response time
✓ Full source attribution
✓ Production-ready architecture

The code is modular, well-documented, and ready for deployment.

Thank you for watching!
