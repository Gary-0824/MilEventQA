# MilEventQA: A Military Domain Event-Centric QA Benchmark for RAG

## 📖 Introduction

**MilEventQA** is a Chinese military domain question-answering benchmark designed for evaluating **Retrieval-Augmented Generation (RAG)** systems in terminology-intensive specialized domains. It consists of two independent components:

1. **Training data** (`data/train/`): 12,948 contrastive learning triplets (query-positive-negative) for fine-tuning text embedding models on military domain corpus.
2. **Evaluation data** (`data/eval/`): 15,360 question-answer pairs with a 54,369-document corpus, derived from the [CMNEE](https://github.com/RichardMingda/ZhuMingning-CMNEE) military event extraction dataset.

The training and evaluation data are **sourced independently** (military magazines vs. CMNEE military news) to avoid the self-evaluation bias common in synthetic benchmarks.

## 📁 Repository Structure

```
MilEventQA/
├── data/
│   ├── train/
│   │   └── finetune_triplets.jsonl    # 12,948 contrastive triplets (Git LFS)
│   └── eval/                           # MilEventQA benchmark
│       ├── queries.jsonl               # 15,360 queries
│       ├── corpus.jsonl                # 54,369 documents (Git LFS)
│       ├── qrels.tsv                   # Query-document relevance
│       └── answers.jsonl               # Short gold answers
├── scripts/
│   └── load_data.py                    # Data loading example
├── README.md
├── LICENSE
└── CITATION.bib
```

## 📊 Dataset Statistics

### Training Triplets

| Statistic | Value |
|-----------|-------|
| Total triplets | 12,948 |
| Fields | `query`, `pos`, `neg[]` |
| Avg. query length | 23.9 chars |
| Hard negatives per query | 7 (designed), 6.3 (avg.) |
| Fully allocated ratio | ~90% |

### MilEventQA Benchmark

| Statistic | Value |
|-----------|-------|
| QA pairs | 15,360 |
| Corpus documents | 54,369 |
| Event types | 8 (Experiment, Deploy, Support, Exhibit, Manoeuvre, Accident, Conflict, Injure) |
| Argument roles | 11 (Subject, Equipment, Date, Location, Militaryforce, Object, Materials, Content, Result, Area, Quantity) |

## 📋 Data Format

### `finetune_triplets.jsonl` (Training)

Each line is a JSON object:

```json
{
  "query": "此次反舰导弹实射训练验证了什么能力？",
  "pos": "近日，南部战区海军某舰载航空兵团，在南海某海域开展反舰导弹实射训练……",
  "neg": [
    "反舰导弹编队攻击的交叉定位与发射协同要素……",
    "歼15舰载机首次执行反舰训练任务……",
    "...(up to 7 hard negatives)"
  ]
}
```

### `queries.jsonl` / `answers.jsonl` (Evaluation)

```json
{"_id": "q0", "text": "哪个机构在负责这项持续约五周的三阶段测试项目？"}
{"_id": "q0", "answer": "美国特种作战司令部"}
```

### `qrels.tsv` (Relevance)

TSV format (no header): `query_id \t document_id \t relevance`

```
q0    cmnee_valid_2    1
q1    cmnee_test_5     1
```

### `corpus.jsonl` (Documents)

```json
{"_id": "doc_000000", "title": "", "text": "俄罗斯国防部长谢尔盖绍伊古表示……"}
```

## 🚀 Quick Start

```python
import json

# Load training triplets
with open("data/train/finetune_triplets.jsonl") as f:
    triplets = [json.loads(line) for line in f]
print(f"Loaded {len(triplets)} training triplets")

# Load evaluation queries and answers
with open("data/eval/queries.jsonl") as f:
    queries = {json.loads(line)["_id"]: json.loads(line)["text"] for line in f}

with open("data/eval/answers.jsonl") as f:
    answers = {json.loads(line)["_id"]: json.loads(line)["answer"] for line in f}

# Load qrels
qrels = {}
with open("data/eval/qrels.tsv") as f:
    for line in f:
        qid, docid, rel = line.strip().split("\t")
        qrels.setdefault(qid, {})[docid] = int(rel)
```

## 📌 Data Sources

| Component | Source | Description |
|-----------|--------|-------------|
| Training corpus | *World Military*, *Ordnance Knowledge*, *Military Digest* (public magazines) | 7,735 high-quality passages after 3-stage filtering |
| Training queries | LLM-synthesized from military magazine corpus | 14,446 query-positive pairs with hard negative mining |
| Evaluation corpus | [CMNEE](https://github.com/RichardMingda/ZhuMingda-CMNEE) (Zhu et al., LREC-COLING 2024) | 54,369 documents from Chinese military news |
| Evaluation QA | Constructed from CMNEE event argument annotations | 15,360 question-answer pairs with semanticized queries |

> **Note**: The evaluation corpus is derived from CMNEE. Please refer to the original [CMNEE dataset](https://github.com/RichardMingda/ZhuMingda-CMNEE) for licensing details of the underlying news articles.

## 📄 Citation

If you use this dataset in your research, please cite:

```bibtex
@article{mileventqa2026,
  title={To be filled upon publication},
  author={},
  journal={},
  year={2026}
}
```

## 📜 License

This project is licensed under the **Apache License 2.0** - see [LICENSE](LICENSE) for details.

The evaluation corpus is derived from [CMNEE](https://github.com/RichardMingda/ZhuMingda-CMNEE) and is subject to its respective license.
