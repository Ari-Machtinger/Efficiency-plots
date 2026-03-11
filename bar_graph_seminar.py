from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

INPUT_TSV = Path("/Users/mach_admin/Downloads/Untitled spreadsheet - Sheet1.tsv")
OUTPUT_SVG = Path("/Users/mach_admin/Downloads/Thesis committee meetings/1st meeting/Data/Efficiency plots/bar_graph_seminar.svg")
OUTPUT_PNG = Path("/Users/mach_admin/Downloads/Thesis committee meetings/1st meeting/Data/Efficiency plots/bar_graph_seminar.png")

REPLICATE_COLUMNS = [
    "Air sample replicate 1",
    "Air sample replicate 2",
    "Air sample replicate 3",
]
AVERAGE_COLUMN = "Average"


def pct_to_float(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
        .replace("", np.nan)
        .astype(float)
    )


def main() -> None:
    plt.rcParams.update(
        {
            "font.size": 20,
            "axes.titlesize": 28,
            "axes.labelsize": 24,
            "xtick.labelsize": 20,
            "ytick.labelsize": 20,
            "legend.fontsize": 20,
            "svg.fonttype": "none",
        }
    )

    df = pd.read_csv(INPUT_TSV, sep="\t")

    sampler_column = df.columns[0]
    df = df.rename(columns={sampler_column: "Sampler"})

    for column in REPLICATE_COLUMNS + [AVERAGE_COLUMN]:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")
        df[column] = pct_to_float(df[column])

    df = df.dropna(subset=["Sampler", AVERAGE_COLUMN]).copy()

    # Error bars as standard deviation across replicate measurements.
    df["error_sd"] = df[REPLICATE_COLUMNS].std(axis=1, ddof=1)

    x = np.arange(len(df))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(
        x,
        df[AVERAGE_COLUMN],
        yerr=df["error_sd"],
        color="#4C78A8",
        edgecolor="black",
        capsize=6,
        linewidth=1,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(df["Sampler"])
    ax.set_xlabel("Sampler", labelpad=28)
    ax.set_ylabel("Detection %")
    ax.set_title("Inactivated SARS-CoV-2 (%)\ndetected by each sampler", pad=20)
    ax.set_ylim(0, 30)

    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig(OUTPUT_SVG, dpi=300)
    fig.savefig(OUTPUT_PNG, dpi=300)

    print(f"Saved SVG: {OUTPUT_SVG}")
    print(f"Saved PNG: {OUTPUT_PNG}")


if __name__ == "__main__":
    main()
