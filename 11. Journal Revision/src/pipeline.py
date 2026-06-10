import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from preferences import neighborhoods_satisfying, features

# ---- CF backend ----
def make_itemcf_backend(train_matrix):
    """Build an ItemCF score_fn(nace) from a training interaction matrix
    (rows = NACE classes, columns = neighbourhoods)."""
    sim = cosine_similarity(train_matrix.T.values)
    sim_df = pd.DataFrame(sim, index=train_matrix.columns, columns=train_matrix.columns)

    def itemcf_backend(nace):
        return pd.Series(sim_df.values @ train_matrix.loc[nace].values,
                         index=train_matrix.columns)
    return itemcf_backend

# ---- pipeline components ----
def extract_constraints(query):
    """Parse a query into preference terms.
    STUB for now: returns no constraints (pure CF). LLM version comes in 08.
    Shape: {'hard': set(of terms), 'soft': set(of terms)}."""
    return {'hard': set(), 'soft': set()}


def apply_filter(scores, constraints, feats=features):
    """Set the score of any neighbourhood that violates a hard constraint to
    -inf, preserving CF ordering among the survivors. Uses the SAME
    neighborhoods_satisfying that built the benchmark ground truth — so the
    filter and the answer key can never drift apart."""

    hard = constraints.get('hard', set())
    if not hard:
        return scores
    satisfying = neighborhoods_satisfying(hard)
    filtered = scores.copy()
    filtered[~filtered.index.isin(satisfying)] = -np.inf
    return filtered

def rerank(scores, constraints, feats=features):
    """Soft-preference re-ranking. STUB: pass-through (soft is a later layer)."""
    return scores

def make_pipeline_score_fn(cf_backend, query=None, constraints=None, extractor=extract_constraints, feats=features):
    def score_fn(nace):
        candidates = cf_backend(nace)
        cons = constraints if constraints is not None else extractor(query)
        filtered = apply_filter(candidates, cons, feats)
        ranked = rerank(filtered, cons, feats)
        return ranked
    return score_fn
