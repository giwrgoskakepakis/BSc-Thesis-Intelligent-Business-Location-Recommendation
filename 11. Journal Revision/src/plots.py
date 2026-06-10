# src/plots.py
import matplotlib.pyplot as plt

K_VALUES = [1, 3, 5, 10]

def plot_metric(summaries, metric, subset, ax, k_values=K_VALUES):
    for name, s in summaries.items():
        if subset not in s:
            continue
        values = [s[subset][f'{metric}@{k}'] for k in k_values]
        ax.plot(k_values, values, marker='o', label=name)
    ax.set_xlabel('K'); ax.set_ylabel(f'{metric}@K')
    subset_label = 'full test set' if subset == 'full' else 'long-tail subset'
    ax.set_title(f'{metric}@K — {subset_label}')
    ax.set_xticks(k_values); ax.set_ylim(bottom=0)
    ax.legend(); ax.grid(True, alpha=0.3)

def plot_metric_grid(summaries, path=None, k_values=K_VALUES):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    plot_metric(summaries, 'HR',   'full',      axes[0, 0], k_values)
    plot_metric(summaries, 'HR',   'long_tail', axes[0, 1], k_values)
    plot_metric(summaries, 'NDCG', 'full',      axes[1, 0], k_values)
    plot_metric(summaries, 'NDCG', 'long_tail', axes[1, 1], k_values)
    plt.tight_layout()
    if path:
        plt.savefig(path, dpi=100, bbox_inches='tight')
    plt.show()