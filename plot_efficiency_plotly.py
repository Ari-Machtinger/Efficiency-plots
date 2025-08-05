import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
file_path = "Madison analysis for chamber study virus series - Virus test series 1.tsv"
df = pd.read_csv(file_path, sep='\t')

# Filter out SKC rows and blanks
samplers = ['AerosolSense', 'Apollo', 'Cub']
df = df[df['Sample'].apply(lambda x: any(s in x for s in samplers) and 'SKC' not in x and 'blank' not in x)]

# Extract dose type
def get_dose(sample):
    if 'low dose' in sample:
        return 'Low Dose'
    elif 'high dose' in sample:
        return 'High Dose'
    else:
        return None

df['Dose'] = df['Sample'].apply(get_dose)
df = df[df['Dose'].notnull()]

# Extract sampler name
def get_sampler(sample):
    for s in samplers:
        if s in sample:
            return s
    return None

df['Sampler'] = df['Sample'].apply(get_sampler)

# Efficiency column (multiply by 100)
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

# Use Plotly Express for grouped boxplot with overlaid data points
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
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

# Create boxplot traces
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
    title='<b>Virus test series 1</b>',
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
import numpy as np

# Update layout for title and axis fonts
fig.update_layout(
    title={
        'text': '<b>Virus test series 1</b>',
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
# Print out every plot point with sample name and efficiency
print("Plot points used for each boxplot:")
for sampler in samplers:
    for dose in ['Low Dose', 'High Dose']:
        group = df[(df['Sampler'] == sampler) & (df['Dose'] == dose)].head(3)
        print(f"\n{sampler} - {dose}:")
        for _, row in group.iterrows():
            efficiency_val = row['Efficiency']
            try:
                efficiency_val_float = float(efficiency_val)
                print(f"  {row['Sample']}: {efficiency_val_float:.2f}%")
            except Exception:
                print(f"  {row['Sample']}: {efficiency_val}%")

# Format y-axis: 0-100, ticks every 10, show as percent labels
fig.update_yaxes(title='Efficiency', title_font={'size': 36}, range=[0, 60], showgrid=True, tickvals=np.arange(0, 70, 10), ticktext=[f"{i}%" for i in range(0, 70, 10)])
fig.show()
