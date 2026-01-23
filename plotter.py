import matplotlib.pyplot as plt
from scipy.stats import pearsonr, linregress
import numpy as np
from external_values import detect_outliers


def plot_weights_vs_days(weights, dates=None):
    plt.figure()
    plt.plot(dates, weights, marker="o", color='rebeccapurple')
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.ylabel("Weight (%)")
    plt.title("Mouse Weight Over Time")
    plt.tight_layout()
    plt.show()


def plot_weight_vs_external(
    weights,
    external_values,
    show_regression=False,
    mark_outliers=False,
    z_thresh=3.0
):
    weights = np.asarray(weights, dtype=float)
    external_values = np.asarray(external_values, dtype=float)

    fig, ax = plt.subplots()

    if mark_outliers:
        in_mask, out_mask = detect_outliers(
            external_values, weights, z_thresh
        )

        # Plot inliers
        ax.scatter(
            external_values[in_mask],
            weights[in_mask],
            label="Data",
            alpha=0.8,
            color="rebeccapurple"
        )

        # Plot outliers
        ax.scatter(
            external_values[out_mask],
            weights[out_mask],
            label="Outliers",
            marker="x",
            s=80,
            color="crimson"
        )

        # Stats computed on inliers only
        x_stats = external_values[in_mask]
        y_stats = weights[in_mask]

    else:
        ax.scatter(external_values, weights, label="Data", color="rebeccapurple")
        x_stats = external_values
        y_stats = weights

    # Pearson correlation - only compute if we have at least 2 points
    if len(x_stats) >= 2:
        r, p = pearsonr(x_stats, y_stats)
        text = f"Pearson r = {r:.3f}\np-value = {p:.3e}"

        # Regression
        if show_regression and len(x_stats) >= 2:
            slope, intercept, _, _, _ = linregress(x_stats, y_stats)
            x_line = np.linspace(x_stats.min(), x_stats.max(), 100)
            y_line = slope * x_line + intercept
            ax.plot(x_line, y_line, linestyle="--", label="Linear regression", color="mediumorchid")

            text += f"\nSlope = {slope:.3f}"
    else:
        text = "Insufficient data for correlation (need at least 2 points)"

    ax.set_xlabel("External value")
    ax.set_ylabel("Weight (%)")
    ax.set_title("Weight vs External Value")

    ax.legend()

    ax.text(
        0.05, 0.95,
        text,
        transform=ax.transAxes,
        va="top",
        bbox=dict(boxstyle="round", alpha=0.8, color="wheat")
    )

    plt.tight_layout()
    plt.show()
