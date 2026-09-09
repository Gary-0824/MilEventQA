# MilEventQA: A Military Domain Event-Centric QA Benchmark for RAG

## 📖 Introduction

**MilEventQA** is a Chinese military domain question-answering benchmark designed for evaluating **Retrieval-Augmented Generation (RAG)** systems in terminology-intensive specialized domains. It consists of two independent components:

1. **Training data** (`data/train/`): 12,948 contrastive learning triplets (query-positive-negative) for fine-tuning text embedding models on military domain corpus.
2. **Evaluation data** (`data/eval/`): 15,334 question-answer pairs with a 54,369-document corpus and 25,015 relevance judgments, derived from the [CMNEE](https://github.com/RichardMingda/ZhuMingda-CMNEE) military event extraction dataset.

The training and evaluation data are **sourced independently** (military magazines vs. CMNEE military news) to avoid the self-evaluation bias common in synthetic benchmarks.

## 🔖 Version History

### v2.0 (current)

A systematic audit, repair, and relevance augmentation of the evaluation benchmark:

- **Query repair**: rule-based scanning detected 700 truncated/incomplete queries; all were regenerated from their original anchors (same gold answer, same event anchor) with reinforced filtering.
- **Entry removal**: 26 queries whose gold answers cannot be objectively judged by exact match were removed (16 relative-time golds such as "本周"/"昨日", 10 vague golds such as "硬件"). QA pairs: 15,360 → 15,334.
- **Relevance augmentation**: unannotated top-10 retrieved documents were pooled, gold-string pre-filtering plus LLM consistency filtering were applied, and 9,682 additional relevance judgments were appended. qrels: 25,015 judgments total; 5,565 queries (36.3%) have multiple positives, averaging 1.63 positives per query.
- **Full LLM quality audit**: all 15,344 queries were audited on four dimensions (correctness, naturalness, answerability, ambiguity) with a 99.8% pass rate; flagged entries are released in `quality_audit.jsonl`.
- **Human validation**: an independent human annotator re-labeled a 300-item random sample under the same four-dimension protocol; judgment-level agreement with the LLM audit was 93.3% (released in `human_validation.jsonl`).
- **Human-written subset**: 350 queries independently written by two team members from the same document-answer anchors as the synthetic queries (released in `human_subset/`).

### v1.0

Initial release: 15,360 QA pairs, single-positive qrels. Available via the `v1.0` tag.

## 📁 Repository Structure

```
MilEventQA/
├── data/
│   ├── train/
│   │   └── finetune_triplets.jsonl    # 12,948 contrastive triplets (Git LFS)
│   └── eval/                           # MilEventQA benchmark (v2)
│       ├── queries.jsonl               # 15,334 queries
│       ├── corpus.jsonl                # 54,369 documents (Git LFS)
│       ├── qrels.tsv                   # 25,015 relevance judgments
│       ├── answers.jsonl               # 15,334 short gold answers
│       ├── quality_audit.jsonl         # full 4-dimension LLM audit results
│       ├── human_validation.jsonl      # 300-item human re-labeling (agreement 93.3%)
│       └── human_subset/               # 350 human-written queries
│           ├── queries_human.jsonl     # human-written queries
│           ├── answers_human.jsonl     # gold answers
│           ├── qrels_human.tsv         # relevance judgments
│           └── anchor_map.json         # anchor mapping to synthetic queries
├── scripts/
│   └── load_data.py                    # Data loading example
├── README.md
├── LICENSE
└── CITATION.bib
```

## 📊 Dataset Statistics

### Training Triplets

| Statistic | Value |
|:---|:---|
| Total triplets | 12,948 |
| Fields | `query`, `pos`, `neg[]` |
| Avg. query length | 23.9 chars |
| Hard negatives per query | 7 (designed), 6.3 (avg.) |
| Fully allocated ratio | ~90% |

### MilEventQA Benchmark (v2)

| Statistic | Value |
|:---|:---|
| QA pairs | 15,334 |
| Corpus documents | 54,369 |
| Relevance judgments | 25,015 |
| Queries with multiple positives | 5,565 (36.3%) |
| Avg. positives per query | 1.63 |
| Event types | 8 (Experiment, Deploy, Support, Exhibit, Manoeuvre, Accident, Conflict, Injure) |
| Argument roles | 11 (Subject, Equipment, Date, Location, Militaryforce, Object, Materials, Content, Result, Area, Quantity) |

## 📋 Data Format

### `finetune_triplets.jsonl` (Training)

Each line is a JSON object:

```json
{
  "query": "此次反舰导弹实射训练验证了什么能力？",
  "pos": "近日，xx海军某舰载航空兵团，在某海域开展反舰导弹实射训练……",
  "neg": [
    "反舰导弹编队攻击的交叉定位与发射协同要素……",
    "xx舰载机首次执行反舰训练任务……",
    "...(up to 7 hard negatives)"
  ]
}
```

### `queries.jsonl` / `answers.jsonl` (Evaluation)

```json
{"_id": "q0", "text": "哪个机构在负责这项持续约五周的三阶段测试项目？"}
```
```json
{"_id": "q0", "answer": "美国特种作战司令部"}
```

### `qrels.tsv` (Relevance)

TSV format (no header): `query_id \t document_id \t relevance`

```
q0    cmnee_valid_2    1
q1    cmnee_test_5     1
```

Note: a query may have multiple positive documents (36.3% of queries).

### `quality_audit.jsonl` (LLM Audit, v2)

Per-query audit results over four dimensions:

```json
{"qid": "q7", "dims": {"correctness": {"pass": true, "reason": "..."}, "naturalness": {"pass": true, "reason": "..."}, "answerability": {"pass": true, "reason": "..."}, "ambiguity": {"pass": true, "reason": "..."}}, "pass": true, "flags": []}
```

### `human_validation.jsonl` (Human Validation, v2)

Independent human re-labeling of a 300-item random sample (judgment-level agreement with the LLM audit: 93.3%):

```json
{"qid": "q13", "human": {"correctness": "pass", "naturalness": "pass", "answerability": "pass", "ambiguity": "pass"}}
```

Entries with a `note` field contain the annotator's reason for failed dimensions.

### `human_subset/` (Human-Written Queries, v2)

350 queries independently written by two team members from the same document-answer anchors as the synthetic queries (writers could not see the synthetic questions). Formats mirror the main benchmark (`queries_human.jsonl`, `answers_human.jsonl`, `qrels_human.tsv`); `anchor_map.json` maps each human-written query to its synthetic counterpart for paired comparison.

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
    answers = {}
    for line in f:
        d = json.loads(line)
        answers[d["_id"]] = d["answer"]

# Load qrels (note: multiple positives per query)
qrels = {}
with open("data/eval/qrels.tsv") as f:
    for line in f:
        qid, docid, rel = line.strip().split("\t")
        qrels.setdefault(qid, {})[docid] = int(rel)
```

## 📌 Data Sources

| Component | Source | Description |
|:---|:---|:---|
| Training corpus | *World Military*, *Ordnance Knowledge*, *Military Digest* (public magazines) | 7,735 high-quality passages after 3-stage filtering |
| Training queries | LLM-synthesized from military magazine corpus | 14,446 query-positive pairs with hard negative mining |
| Evaluation corpus | [CMNEE](https://github.com/RichardMingda/ZhuMingda-CMNEE) (Zhu et al., LREC-COLING 2024) | 54,369 documents from Chinese military news |
| Evaluation QA | Constructed from CMNEE event argument annotations | 15,334 question-answer pairs with semanticized queries (v2, after audit and repair) |

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
