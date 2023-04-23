import numpy as np
import pandas as pd
from typing import List

import redis
from redis.commands.search.indexDefinition import (
    IndexDefinition,
    IndexType
)
from redis.commands.search.query import Query
from redis.commands.search.field import (
    TextField,
    VectorField
)

# Constants
VECTOR_DIM = 1536       #len(data['title_vector'][0])    # length of the vectors
VECTOR_NUMBER = 25000   #len(data)                 # initial number of vectors
INDEX_NAME = "embeddings-index"           # name of the search index
PREFIX = "doc"                            # prefix for the document keys
DISTANCE_METRIC = "COSINE"                # distance metric for the vectors (ex. COSINE, IP, L2)


# Define RediSearch fields for each of the columns in the dataset
title = TextField(name="title")
url = TextField(name="url")
text = TextField(name="text")
title_embedding = VectorField("title_vector",
    "FLAT", {
        "TYPE": "FLOAT32",
        "DIM": VECTOR_DIM,
        "DISTANCE_METRIC": DISTANCE_METRIC,
        "INITIAL_CAP": VECTOR_NUMBER,
    }
)
text_embedding = VectorField("content_vector",
    "FLAT", {
        "TYPE": "FLOAT32",
        "DIM": VECTOR_DIM,
        "DISTANCE_METRIC": DISTANCE_METRIC,
        "INITIAL_CAP": VECTOR_NUMBER,
    }
)
fields = [title, url, text, title_embedding, text_embedding]

REDIS_HOST =  "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = "p@$$w0rdw!th0ut" # default for passwordless Redis

def search_redis(
    redis_client,
    user_query,
    index_name: str = "embeddings-index",
    vector_field: str = "title_vector",
    return_fields: list = ["title", "url", "text", "vector_score"],
    hybrid_fields = "*",
    k: int = 20,
    print_results: bool = True,
) -> List[dict]:

    # Creates embedding vector from user query

    # embedded_query = openai.Embedding.create(input=user_query,
    #                                         model="text-embedding-ada-002",
    #                                         )["data"][0]['embedding']

    # Prepare the Query
    base_query = f'{hybrid_fields}=>[KNN {k} @{vector_field} $vector AS vector_score]'
    query = (
        Query(base_query)
         .return_fields(*return_fields)
         .sort_by("vector_score")
         .paging(0, k)
         .dialect(2)
    )
    params_dict = {"vector": user_query.tobytes()}

    # perform vector search
    results = redis_client.ft(index_name).search(query, params_dict)
    if print_results:
        for i, article in enumerate(results.docs):
            score = 1 - float(article.vector_score)
            # print(f"{i}. {article.title} (Score: {round(score ,3) })")
    return results.docs


def SearchProcess():
    # Connect to Redis
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD
    )
    arr = np.random.rand(VECTOR_DIM).astype(np.float32)

    # search_redis(redis_client, arr, k=20)

    # print('hello')
    # redis_client.ping()


# SearchProcess()    