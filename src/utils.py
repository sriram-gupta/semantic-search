from sentence_transformers import SentenceTransformer
import numpy as np
import torch

embedder = SentenceTransformer('all-MiniLM-L6-v2')


def embeddText(str):
    return embedder.encode(str,convert_to_tensor=True)


__all__ = ['embeddText']