#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Data loading example for MilEventQA dataset."""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_train_triplets():
    """Load contrastive learning triplets for embedding fine-tuning."""
    path = os.path.join(DATA_DIR, "train", "finetune_triplets.jsonl")
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def load_eval_queries():
    """Load evaluation queries."""
    path = os.path.join(DATA_DIR, "eval", "queries.jsonl")
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def load_eval_answers():
    """Load gold answers keyed by query ID."""
    path = os.path.join(DATA_DIR, "eval", "answers.jsonl")
    answers = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            answers[d["_id"]] = d["answer"]
    return answers


def load_eval_qrels():
    """Load query-document relevance judgments."""
    path = os.path.join(DATA_DIR, "eval", "qrels.tsv")
    qrels = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            qid, docid, rel = line.strip().split("\t")
            qrels.setdefault(qid, {})[docid] = int(rel)
    return qrels


def load_eval_corpus():
    """Load evaluation corpus documents."""
    path = os.path.join(DATA_DIR, "eval", "corpus.jsonl")
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


if __name__ == "__main__":
    triplets = load_train_triplets()
    print(f"Training triplets: {len(triplets)}")
    print(f"  Example query: {triplets[0]['query'][:50]}...")
    print(f"  Negatives per query: {len(triplets[0]['neg'])}")

    queries = load_eval_queries()
    answers = load_eval_answers()
    qrels = load_eval_qrels()
    corpus = load_eval_corpus()
    print(f"\nEvaluation queries: {len(queries)}")
    print(f"Gold answers: {len(answers)}")
    print(f"Relevance judgments: {len(qrels)} queries")
    print(f"Corpus documents: {len(corpus)}")
