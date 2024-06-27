#!/usr/bin/env python3
"""Using the model to generate dynamic content."""

import random


# from fastai.collab import Embedding
from fastai.tabular.all import (
    Module,
    Embedding,
    sigmoid_range,
    pd,
    load_learner,
    tensor,
    nn,
)


# The class, as defined in the actual module,
class DotProduct(Module):
    """Dot Product Class that is used to construct
    the behaviour of the collab filtering
        model."""

    def __init__(self, n_users, n_items, n_factors, y_range=(-9.5, 10.5)):
        self.user_factors = Embedding(n_users, n_factors)
        self.user_bias = Embedding(n_users, 1)
        self.item_factors = Embedding(n_items, n_factors)
        self.item_bias = Embedding(n_items, 1)
        self.y_range = y_range
        pass

    def forward(self, x):
        """Define the forward propagation."""
        users = self.user_factors(x[:, 0])
        items = self.item_factors(x[:, 1])
        res = (users * items).sum(dim=1, keepdim=True)
        res += self.user_bias(x[:, 0]) + self.item_bias(x[:, 1])
        return sigmoid_range(res, *self.y_range)


# Load in our pickled dataframe.
ratings_df = pd.read_pickle("./mini_ratings-df.pkl")

# Load in our learner.
learn_inf = load_learner("./export-3-10.pkl")


def generate_random(n: int = 10) -> list:
    """Generate random JokeIds from 0 - 140"""
    return random.sample(range(141), n)


def generate_dynamic(include_ids: list, n: int = 5):
    """Generate dynamic specifc contents"""
    if len(include_ids) == 1:
        dls_inf = learn_inf.dls
        joke_factors_inf = learn_inf.model.item_factors.weight
        idx_int = list(
            include_ids[0]
        )  # You can change this id, to get different results.
        cls_idx = tensor(dls_inf.classes["jokeId"].o2i[idx_int])
        int_joke_emb = joke_factors_inf[cls_idx, None]
        distances = nn.CosineSimilarity(dim=1)(joke_factors_inf, int_joke_emb)
        # Top 5 closest jokes.
        closest_emb_idx = distances.argsort(descending=True)[1 : n + 1]
        closest_idx = dls_inf.classes["jokeId"][closest_emb_idx]
        return closest_idx
    closest_idxs = []
    for idx in random.sample(list(include_ids), 2):
        dls_inf = learn_inf.dls
        joke_factors_inf = learn_inf.model.item_factors.weight
        idx_int = idx  # You can change this id, to get different results.
        cls_idx = tensor(dls_inf.classes["jokeId"].o2i[idx_int])
        int_joke_emb = joke_factors_inf[cls_idx, None]
        distances = nn.CosineSimilarity(dim=1)(joke_factors_inf, int_joke_emb)
        # Top 5 closest jokes.
        closest_emb_idx = distances.argsort(descending=True)[1 : n + 1]
        closest_idxs.extend(dls_inf.classes["jokeId"][closest_emb_idx])
    return random.sample(closest_idxs, n)


def generate_text_from_id(joke_ids: list[int]):
    """This is used to generate the appropriate text from a list of joke
    ids.
    """
    closest_jokes = ratings_df[ratings_df["jokeId"].isin(joke_ids)].drop_duplicates(
        "jokeId"
    )["jokeText"]
    return list(closest_jokes)
