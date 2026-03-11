from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap

INPUT_TSV = Path("/Users/mach_admin/Downloads/results_summary_qualitative_2026-03-11_15-55-06.tsv")
OUTPUT_SVG = Path("/Users/mach_admin/Downloads/Thesis committee meetings/1st meeting/Data/Efficiency plots/heatmap_positive_negative.svg")
OUTPUT_PNG = Path("/Users/mach_admin/Downloads/Thesis committee meetings/1st meeting/Data/Efficiency plots/heatmap_positive_negative.png")
OUTPUT_MATRIX_CSV = Path("/Users/mach_admin/Downloads/Thesis committee meetings/1st meeting/Data/Efficiency plots/heatmap_positive_negative_matrix.csv")


def main() -> None:
    df = pd.read_csv(INPUT_TSV, sep="\t")

    required_columns = ["Assay Target", "Start Time", "Qualitative Result"]
    missing_columns = [column for column in required_columns if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    clean = df[required_columns].copy()
    clean = clean.dropna(subset=["Assay Target", "Start Time", "Qualitative Result"])
    clean["Assay Target"] = clean["Assay Target"].astype(str).str.strip()
    clean["Qualitative Result"] = clean["Qualitative Result"].astype(str).str.strip().str.title()
    clean["Start Time"] = pd.to_datetime(clean["Start Time"], errors="coerce")
    clean = clean[clean["Start Time"].notna()]

    clean = clean[clean["Assay Target"].str.lower() != "spc"]
    clean = clean[clean["Qualitative Result"].isin(["Positive", "Negative"])]

    clean["value"] = clean["Qualitative Result"].map({"Negative": 0, "Positive": 1})

    grouped = (
        clean.groupby(["Assay Target", "Start Time"], as_index=False)["value"]
        .max()
        .copy()
    )

    if grouped.empty:
        raise ValueError("No valid Positive/Negative pathogen data found after filtering.")

    matrix = grouped.pivot(index="Assay Target", columns="Start Time", values="value")

    pathogen_order = sorted(matrix.index.tolist())
    matrix = matrix.reindex(pathogen_order)

    matrix = matrix.sort_index(axis=1)

    matrix.to_csv(OUTPUT_MATRIX_CSV)

    data = matrix.to_numpy(dtype=float)

    fig_width = max(12, 0.35 * data.shape[1] + 4)
    fig_height = max(4, 0.8 * data.shape[0] + 2)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    cmap = ListedColormap(["#f0f0f0", "#d62728"])
    masked = np.ma.masked_invalid(data)
    im = ax.imshow(masked, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    x_labels = [timestamp.strftime("%Y-%m-%d") for timestamp in matrix.columns]
    y_labels = matrix.index.tolist()

    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_xticklabels(x_labels, rotation=60, ha="right")
    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_yticklabels(y_labels)

    ax.set_xlabel("Time (Start Time)")
    ax.set_ylabel("Pathogen")
    ax.set_title("Pathogen Detection Heatmap (Positive/Negative)")

    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1])
    cbar.ax.set_yticklabels(["Negative", "Positive"])

    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            if np.isnan(data[row, col]):
                continue
            label = "P" if data[row, col] == 1 else "N"
            text_color = "white" if data[row, col] == 1 else "black"
            ax.text(col, row, label, ha="center", va="center", color=text_color, fontsize=8)

    fig.tight_layout()
    fig.savefig(OUTPUT_SVG, dpi=300)
    fig.savefig(OUTPUT_PNG, dpi=300)

    print(f"Saved SVG: {OUTPUT_SVG}")
    print(f"Saved PNG: {OUTPUT_PNG}")
    print(f"Saved matrix CSV: {OUTPUT_MATRIX_CSV}")


if __name__ == "__main__":
    main()
