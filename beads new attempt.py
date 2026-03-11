import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Load the data
file_path = "Madison analysis for chamber study virus series - Virus test series 1.tsv"
df = pd.read_csv(file_path, sep='\t')

# Filter out SKC rows and blanks
samplers = ['AerosolSense', 'Apollo', 'Cub']
df = df[df['Sample'].apply(lambda x: any(s in x for s in samplers) and 'SKC' not in x and 'blank' not in x)]

def get_dose(sample):
    if 'low dose' in sample:
        return 'Low Dose'
    elif 'high dose' in sample:
        return 'High Dose'
    else:
        return None

def get_sampler(sample):
    for s in samplers:
        if s in sample:
            return s
    return None

df['Dose'] = df['Sample'].apply(get_dose)
df = df[df['Dose'].notnull()]
df['Sampler'] = df['Sample'].apply(get_sampler)
df['Efficiency'] = pd.to_numeric(df['Efficiency of capture based on APS'], errors='coerce') * 100

# Build plot_df using only the correct sample names and efficiency values
plot_df = []
for sampler in samplers:
    for dose in ['Low Dose', 'High Dose']:
        group = df[(df['Sampler'] == sampler) & (df['Dose'] == dose)].head(3)
        for _, row in group.iterrows():
            plot_df.append({
                'Sampler': sampler,
                'Dose': dose,
                'Efficiency': row['Efficiency'],
                'Sample': row['Sample']
            })
plot_df = pd.DataFrame(plot_df)

sampler_map = {s: i for i, s in enumerate(plot_df['Sampler'].unique())}
def offset_x(row):
    base = sampler_map[row['Sampler']]
    if row['Dose'] == 'Low Dose':
        return base - 0.2 + np.random.uniform(-0.05, 0.05)
    else:
        return base + 0.2 + np.random.uniform(-0.05, 0.05)
plot_df['x_offset'] = plot_df.apply(offset_x, axis=1)

# Build custom tick positions and labels for x axis
custom_ticks = []
custom_labels = []
sampler_annotations = []
for sampler, base in sampler_map.items():
    custom_ticks.extend([base - 0.2, base + 0.2])
    custom_labels.extend([
        f'<span style="font-size:18px">Low</span>',
        f'<span style="font-size:18px">High</span>'
    ])
    sampler_annotations.append({'x': base, 'text': sampler})

fig = go.Figure()
for sampler, base in sampler_map.items():
    for dose, x_pos in zip(['Low Dose', 'High Dose'], [base - 0.2, base + 0.2]):
        group = plot_df[(plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)]
        if not group.empty:
            min_eff = group['Efficiency'].min()
            max_eff = group['Efficiency'].max()
            mean_eff = group['Efficiency'].mean()
            # Line spanning min to max
            fig.add_trace(go.Scatter(
                x=[x_pos, x_pos],
                y=[min_eff, max_eff],
                mode='lines',
                line=dict(color='rgba(100,100,100,0.7)', width=4),
                showlegend=False
            ))
            # Marker for mean
            fig.add_trace(go.Scatter(
                x=[x_pos],
                y=[mean_eff],
                mode='markers',
                marker=dict(symbol='diamond', size=16, color='orange'),
                name='Mean',
                showlegend=False
            ))
# Add scatter points
fig.add_trace(go.Scatter(
    x=plot_df['x_offset'],
    y=plot_df['Efficiency'],
    mode='markers',
    marker=dict(size=12, color=plot_df['Dose'].map({'Low Dose': 'blue', 'High Dose': 'red'})),
    text=plot_df['Sample'],
    name='Data Points',
    showlegend=False
))
fig.update_layout(
    width=900,
    height=700,
    title='<b>Efficiency of inactivated SARS-CoV-2 by sampler</b>',
    title_x=0.5,
    title_font=dict(size=36),
    margin=dict(b=120),
    yaxis=dict(
        title='Efficiency',
        title_font=dict(size=48),
        range=[0, 60],
        tickvals=np.arange(0, 70, 10),
        ticktext=[f"{i}%" for i in range(0, 70, 10)],
        showgrid=True
    ),
    xaxis=dict(
        tickvals=custom_ticks,
        ticktext=custom_labels,
        tickfont=dict(size=1),
        title='',
        tickangle=0
    ),
    showlegend=False
)
fig.update_xaxes(
    tickvals=custom_ticks,
    ticktext=custom_labels,
    title='',
    tickfont={'size': 1},  # font size overridden by HTML
    tickangle=0
)
fig.update_layout(showlegend=False)
for ann in sampler_annotations:
    fig.add_annotation(
        x=ann['x'],
        y=-0.25,
        text=ann['text'],
        showarrow=False,
        font=dict(size=36),
        xanchor='center',
        yanchor='bottom',
        xref='x',
        yref='paper'
    )
fig.update_layout(
    title={
        'text': '<b>Efficiency of inactivated SARS-CoV-2 by sampler</b>',
        'x': 0.5,
        'font': {'size': 36}
    },
    xaxis_title={
        'text': '',
        'font': {'size': 28}
    },
    yaxis_title={
        'text': 'Efficiency',
        'font': {'size': 48}
    },
    legend={
        'font': {'size': 24}
    },
    xaxis={
        'tickfont': {'size': 28}
    },
    margin={
        'b': 120  # Increase bottom margin for annotation visibility
    }
)
fig.update_yaxes(title='Efficiency', title_font={'size': 36}, range=[0, 60], showgrid=True, tickvals=np.arange(0, 70, 10), ticktext=[f"{i}%" for i in range(0, 70, 10)])
fig.write_html("efficiency_plot_series_1.html")
fig.show()
print("Plot saved as efficiency_plot_series_1.html")

# Redefine the data points for the new graph
data = {
    "Sampler": [
        "Cub", "Cub", "Cub", "Cub", "Cub", "Cub",
        "AerosolSense", "AerosolSense", "AerosolSense", "AerosolSense", "AerosolSense", "AerosolSense",
        "Apollo", "Apollo", "Apollo", "Apollo", "Apollo", "Apollo",
        "Inkfish", "Inkfish", "Inkfish", "Inkfish", "Inkfish", "Inkfish"
    ],
    "Dose": [
        "Low", "Low", "Low", "High", "High", "High",
        "Low", "Low", "Low", "High", "High", "High",
        "Low", "Low", "Low", "High", "High", "High",
        "Low", "Low", "Low", "High", "High", "High"
    ],
    "Replicate": [
        1, 2, 3, 1, 2, 3,
        1, 2, 3, 1, 2, 3,
        1, 2, 3, 1, 2, 3,
        1, 2, 3, 1, 2, 3
    ],
    "Efficiency": [
        49.20, 44.70, 48.90, 53.70, 45.90, 43.80,
        2.40, 0.80, 2.60, 6.60, 2.10, 4.10,
        1.70, 2.30, 1.80, 1.10, 1.20, 1.20,
        2.00, 1.70, 1.10, 2.10, 1.10, 0.80
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Create the graph
fig = go.Figure()

# Add scatter points for each sampler and dose
for sampler in df["Sampler"].unique():
    for dose in ["Low", "High"]:
        subset = df[(df["Sampler"] == sampler) & (df["Dose"] == dose)]
        fig.add_trace(go.Scatter(
            x=[dose] * len(subset),
            y=subset["Efficiency"],
            mode="markers",
            name=f"{sampler} {dose}",
            marker=dict(size=8, color="blue")
        ))

# Update layout to match previous graph style
fig.update_layout(
    title=dict(text="Efficiency by Sampler", font=dict(size=20, color="black")),
    xaxis=dict(
        title="Dose",
        tickangle=-45,
        title_font=dict(size=16, color="black"),
        tickfont=dict(size=14, color="black")
    ),
    yaxis=dict(
        title="Efficiency (%)",
        tickformat="%",
        title_font=dict(size=16, color="black"),
        tickfont=dict(size=14, color="black")
    ),
    font=dict(size=14, color="black"),
    plot_bgcolor="white",
    margin=dict(l=80, r=80, t=80, b=80)
)

# Show the graph
fig.show()
