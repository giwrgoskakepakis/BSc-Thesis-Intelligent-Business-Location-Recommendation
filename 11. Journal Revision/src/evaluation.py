# src/evaluation.py
import numpy as np
import pandas as pd


def evaluate(score_fn, holdout_df, full_matrix, k_values=(1, 3, 5, 10),
             head_neighborhoods=None):
    """
    Leave-one-out ranking evaluation (all-items protocol).

    Parameters
    ----------
    score_fn : callable
        score_fn(nace) -> pd.Series indexed by neighbourhood name, giving a
        score for each of the 48 neighbourhoods for the given NACE class.
        Higher score = more recommended.
    holdout_df : pd.DataFrame
        Columns include [nace, neighborhood]. Each row is one held-out positive.
    full_matrix : pd.DataFrame
        Full interaction matrix (NACE x neighbourhood). Used to identify ALL
        positives per class, so other positives can be excluded from candidates.
    k_values : tuple of int
        K values for HR@K and NDCG@K.
    head_neighborhoods : set or None
        If provided, also report metrics on the long-tail subset (held-out
        targets NOT in head_neighborhoods).

    Returns
    -------
    summary : dict        Metrics for 'full' and (optionally) 'long_tail'.
    per_instance : DataFrame   One row per held-out instance with its rank.
    """
    records = []

    for _, row in holdout_df.iterrows():
        nace = row['nace']
        target = row['neighborhood']

        scores = score_fn(nace)  # Series over all 48 neighbourhoods

        # Exclude all OTHER positives for this class; keep the target
        positives = set(full_matrix.columns[full_matrix.loc[nace] > 0])
        other_positives = positives - {target}
        candidates = [n for n in scores.index if n not in other_positives]

        cand_scores = scores.loc[candidates]
        target_score = cand_scores.loc[target]

        # Average rank among ties (robust): strictly-better count + tie midpoint
        n_better = int((cand_scores > target_score).sum())
        n_tied = int((cand_scores == target_score).sum())  # includes target
        rank = n_better + (n_tied + 1) / 2.0

        records.append({
            'nace': nace, 'target': target,
            'rank': rank, 'n_candidates': len(candidates),
        })

    per_instance = pd.DataFrame(records)

    def compute(df):
        out = {}
        for k in k_values:
            out[f'HR@{k}'] = float((df['rank'] <= k).mean())
            out[f'NDCG@{k}'] = float(df['rank'].apply(
                lambda r: 1.0 / np.log2(r + 1) if r <= k else 0.0
            ).mean())
        return out

    summary = {'full': compute(per_instance), 'full_n': len(per_instance)}

    if head_neighborhoods is not None:
        tail = per_instance[~per_instance['target'].isin(head_neighborhoods)]
        summary['long_tail'] = compute(tail)
        summary['long_tail_n'] = len(tail)

    return summary, per_instance


def print_results(name, summary):
    print(f'{name} — full test set:')
    for m, v in summary['full'].items():
        print(f'  {m}: {v:.4f}')
    print(f"  (n = {summary['full_n']})")
    if 'long_tail' in summary:
        print(f'\n{name} — long-tail subset:')
        for m, v in summary['long_tail'].items():
            print(f'  {m}: {v:.4f}')
        print(f"  (n = {summary['long_tail_n']})")
    print()