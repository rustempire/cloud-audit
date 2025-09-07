from typing import List

from BCEmbedding import EmbeddingModel

model = EmbeddingModel(model_name_or_path="/workspace/bce-embedding-base_v1")


def encode(sentences: List[str]):
    return model.encode(sentences)
