import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["font.family"] = "Arial"

SAMPLERS = ["AerosolSense", "Apollo", "Cub"]
DOSE_ORDER = ["Low", "High"]
DOSE_POINT_COLOR = {"Low": "#1f3cff", "High": "#ff1a1a"}

GRAPHS = [
    {
        "title": "RoD by sampler for inactivated\nSARS-CoV-2, Salter",
        "output_svg": "RoD by sampler for inactivated SARS-CoV-2, Salter.svg",
        "output_csv": "RoD by sampler for inactivated SARS-CoV-2, Salter.csv",
        "records": [
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 1, "rod_percent": 10.7, "average_percent": 8.1},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 2, "rod_percent":  4.8, "average_percent": 8.1},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 3, "rod_percent":  8.9, "average_percent": 8.1},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 1, "rod_percent": 10.4, "average_percent": 5.9},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 2, "rod_percent":  1.3, "average_percent": 5.9},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 3, "rod_percent": np.nan, "average_percent": 5.9},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 1, "rod_percent":  0.3, "average_percent": 0.4},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 2, "rod_percent":  0.7, "average_percent": 0.4},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 3, "rod_percent":  0.1, "average_percent": 0.4},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 1, "rod_percent":  0.4, "average_percent": 0.4},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 2, "rod_percent":  0.5, "average_percent": 0.4},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 3, "rod_percent":  0.2, "average_percent": 0.4},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 1, "rod_percent": 12.0, "average_percent": 11.4},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 2, "rod_percent":  7.7, "average_percent": 11.4},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 3, "rod_percent": 14.5, "average_percent": 11.4},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 1, "rod_percent": 55.3, "average_percent": 29.7},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 2, "rod_percent": 30.0, "average_percent": 29.7},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 3, "rod_percent":  3.7, "average_percent": 29.7},
        ],
    },
    {
        "title": "RoD by sampler for inactivated\nSARS-CoV-2, MiniHEART Lo-Flo",
        "output_svg": "RoD by sampler for inactivated SARS-CoV-2, MiniHEART Lo-Flo.svg",
        "output_csv": "RoD by sampler for inactivated SARS-CoV-2, MiniHEART Lo-Flo.csv",
        "records": [
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 1, "rod_percent":  2.7, "average_percent": 4.7},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 2, "rod_percent":  4.1, "average_percent": 4.7},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 3, "rod_percent":  7.2, "average_percent": 4.7},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 1, "rod_percent":  3.1, "average_percent": 3.4},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 2, "rod_percent":  2.9, "average_percent": 3.4},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 3, "rod_percent":  4.3, "average_percent": 3.4},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 1, "rod_percent":  2.4, "average_percent": 4.9},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 2, "rod_percent":  1.6, "average_percent": 4.9},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 3, "rod_percent": 10.7, "average_percent": 4.9},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 1, "rod_percent":  1.2, "average_percent": 1.1},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 2, "rod_percent":  0.5, "average_percent": 1.1},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 3, "rod_percent":  1.7, "average_percent": 1.1},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 1, "rod_percent": 19.6, "average_percent": 21.3},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 2, "rod_percent": 24.3, "average_percent": 21.3},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 3, "rod_percent": 19.9, "average_percent": 21.3},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 1, "rod_percent": 11.9, "average_percent": 10.6},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 2, "rod_percent":  6.3, "average_percent": 10.6},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 3, "rod_percent": 13.5, "average_percent": 10.6},
        ],
    },
    {
        "title": "RoD by sampler for\n0.5 µm PSL beads",
        "output_svg": "RoD by sampler for 0.5 µm PSL beads.svg",
        "output_csv": "RoD by sampler for 0.5 µm PSL beads.csv",
        "records": [
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 1, "rod_percent":  1.0, "average_percent": 0.6},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 2, "rod_percent":  0.4, "average_percent": 0.6},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 3, "rod_percent":  0.4, "average_percent": 0.6},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 1, "rod_percent":  0.6, "average_percent": 0.4},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 2, "rod_percent":  0.3, "average_percent": 0.4},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 3, "rod_percent":  0.3, "average_percent": 0.4},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 1, "rod_percent":  1.0, "average_percent": 0.9},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 2, "rod_percent":  0.9, "average_percent": 0.9},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 3, "rod_percent":  0.9, "average_percent": 0.9},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 1, "rod_percent":  0.8, "average_percent": 0.7},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 2, "rod_percent":  0.5, "average_percent": 0.7},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 3, "rod_percent":  0.7, "average_percent": 0.7},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 1, "rod_percent": 41.0, "average_percent": 46.8},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 2, "rod_percent": 52.0, "average_percent": 46.8},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 3, "rod_percent": 47.3, "average_percent": 46.8},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 1, "rod_percent": 56.9, "average_percent": 56.7},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 2, "rod_percent": 66.7, "average_percent": 56.7},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 3, "rod_percent": 46.6, "average_percent": 56.7},
        ],
    },
    {
        "title": "RoD by sampler for\n1 µm PSL beads",
        "output_svg": "RoD by sampler for 1 µm PSL beads.svg",
        "output_csv": "RoD by sampler for 1 µm PSL beads.csv",
        "records": [
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 1, "rod_percent":  2.4, "average_percent": 1.9},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 2, "rod_percent":  0.8, "average_percent": 1.9},
            {"Sampler": "AerosolSense", "Dose": "Low",  "replicate": 3, "rod_percent":  2.6, "average_percent": 1.9},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 1, "rod_percent":  6.6, "average_percent": 4.3},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 2, "rod_percent":  2.1, "average_percent": 4.3},
            {"Sampler": "AerosolSense", "Dose": "High", "replicate": 3, "rod_percent":  4.1, "average_percent": 4.3},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 1, "rod_percent":  0.9, "average_percent": 1.0},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 2, "rod_percent":  1.2, "average_percent": 1.0},
            {"Sampler": "Apollo",       "Dose": "Low",  "replicate": 3, "rod_percent":  0.9, "average_percent": 1.0},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 1, "rod_percent":  0.5, "average_percent": 0.6},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 2, "rod_percent":  0.6, "average_percent": 0.6},
            {"Sampler": "Apollo",       "Dose": "High", "replicate": 3, "rod_percent":  0.6, "average_percent": 0.6},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 1, "rod_percent": 49.2, "average_percent": 47.6},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 2, "rod_percent": 44.7, "average_percent": 47.6},
            {"Sampler": "Cub",          "Dose": "Low",  "replicate": 3, "rod_percent": 48.9, "average_percent": 47.6},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 1, "rod_percent": 53.7, "average_percent": 47.8},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 2, "rod_percent": 45.9, "average_percent": 47.8},
            {"Sampler": "Cub",          "Dose": "High", "replicate": 3, "rod_percent": 43.8, "average_percent": 47.8},
        ],
    },
]


def build_values(records):
    df = pd.DataFrame(records)
    df["Dose"] = pd.Categorical(df["Dose"], categories=DOSE_ORDER, ordered=True)
    return df


def jitter_for_group(group):
    present = group[group["rod_percent"].notna()].copy()
    if present.empty:
        return {}
    if len(present) == 1:
        return {int(present.index[0]): 0.0}
    if len(present) == 2:
        sorted_idx = present.sort_values("rod_percent").index.tolist()
        return {int(sorted_idx[0]): -0.08, int(sorted_idx[1]): 0.08}

    sorted_present = present.sort_values("rod_percent")
    sorted_idx = sorted_present.index.tolist()
    sorted_values = sorted_present["rod_percent"].to_numpy(dtype=float)
    min_spacing = float(np.min(np.diff(sorted_values)))

    average_val = float(sorted_present["average_percent"].iloc[0])
    close_to_average = bool(np.any(np.abs(sorted_values - average_val) < 0.8))

    if min_spacing < 1.0 or close_to_average:
        offsets = [-0.11, -0.03, 0.11]
    else:
        offsets = [-0.09, -0.02, 0.09]

    return {int(idx): offsets[i] for i, idx in enumerate(sorted_idx)}


def make_graph(title, output_svg, output_csv, records):
    values_df = build_values(records)

    sampler_to_base = {sampler: index for index, sampler in enumerate(SAMPLERS)}
    dose_offset = {"Low": -0.22, "High": 0.22}

    values_df["x_center"] = values_df.apply(
        lambda row: sampler_to_base[row["Sampler"]] + dose_offset[str(row["Dose"])], axis=1
    )

    values_df["x_jitter"] = 0.0
    for (_, _), group in values_df.groupby(["Sampler", "Dose"], sort=False, observed=False):
        jitter_map = jitter_for_group(group)
        for idx, jitter_value in jitter_map.items():
            values_df.loc[idx, "x_jitter"] = jitter_value

    values_df["x_position"] = values_df["x_center"] + values_df["x_jitter"]

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_facecolor("#cfd8e3")
    fig.patch.set_facecolor("white")
    ax.set_axisbelow(True)

    ax.grid(axis="y", color="white", linewidth=1.2, alpha=0.6, zorder=0)
    ax.grid(axis="x", visible=False)

    for (sampler, dose), group in values_df.groupby(["Sampler", "Dose"], sort=False, observed=False):
        present = group[group["rod_percent"].notna()]
        center_x = float(group["x_center"].iloc[0])
        average_val = float(group["average_percent"].iloc[0])

        min_val = float(present["rod_percent"].min())
        max_val = float(present["rod_percent"].max())

        ax.vlines(center_x, min_val, max_val, colors="#7f7f7f", linewidth=3, zorder=2)
        ax.scatter(center_x, average_val, marker="D", s=140, color="#ff00ff", zorder=4)

        for _, row in present.iterrows():
            point_color = DOSE_POINT_COLOR[str(row["Dose"])]
            ax.scatter(row["x_position"], row["rod_percent"], s=80, color=point_color, zorder=5)

    tick_positions = []
    tick_labels = []
    for sampler in SAMPLERS:
        base = sampler_to_base[sampler]
        tick_positions.extend([base + dose_offset["Low"], base + dose_offset["High"]])
        tick_labels.extend(["Low", "High"])

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, fontsize=20, color="#334a6b")

    for sampler in SAMPLERS:
        base = sampler_to_base[sampler]
        ax.text(
            base,
            -0.12,
            sampler,
            transform=ax.get_xaxis_transform(),
            ha="center",
            va="top",
            fontsize=28,
            color="#334a6b",
        )

    ax.set_ylim(0, 70)
    ax.set_yticks(np.arange(0, 71, 10))
    ax.set_yticklabels([f"{v}%" for v in range(0, 71, 10)], fontsize=12, color="#334a6b")

    ax.set_ylabel("RoD (%)", fontsize=34, color="#223a5e")
    ax.set_title(title, fontsize=28, weight="bold", color="#223a5e")

    for spine in ["top", "right", "left", "bottom"]:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.tick_params(axis="y", length=0)

    fig.tight_layout()
    fig.savefig(output_svg, format="svg", dpi=300)
    plt.close(fig)

    export_df = values_df[["Sampler", "Dose", "replicate", "rod_percent", "average_percent", "x_position"]].copy()
    export_df["point_color"] = export_df["Dose"].astype(str).map(DOSE_POINT_COLOR)
    export_df["included_in_plot"] = export_df["rod_percent"].notna()
    export_df.to_csv(output_csv, index=False)

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(f"\n--- {title.replace(chr(10), ' ')} ---")
        print("Exact values used:")
        print(export_df.to_string(index=False))

    print(f"SVG written: {output_svg}")
    print(f"Values written: {output_csv}")


def main():
    for graph in GRAPHS:
        make_graph(
            title=graph["title"],
            output_svg=graph["output_svg"],
            output_csv=graph["output_csv"],
            records=graph["records"],
        )


if __name__ == "__main__":
    main()
