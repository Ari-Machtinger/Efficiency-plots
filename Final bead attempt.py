import pandas as pd
import plotly.graph_objects as go
import numpy as np
import webbrowser
import plotly.io as pio

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

# Replace the efficiency values with the new ones provided by the user
new_efficiency_values = [
    1.0, 0.4, 0.4,  # AerosolSense Low Dose
    0.6, 0.3, 0.3,  # AerosolSense High Dose
    2.0, 1.7, 1.8,  # Apollo Low Dose
    1.5, 1.0, 1.3,  # Apollo High Dose
    41.0, 52.0, 47.3,  # Cub Low Dose
    56.9, 66.7, 46.6,  # Cub High Dose
    0, 0, 0,  # Inkfish Low Dose
    0.3, 0.5, 0.7   # Inkfish High Dose
]

# Update samplers to include Inkfish
samplers = ['AerosolSense', 'Apollo', 'Cub', 'Inkfish']

# Update plot_df with the new efficiency values
plot_df = []
index = 0
for sampler in samplers:
    for dose in ['Low Dose', 'High Dose']:
        for i in range(3):  # Each dose has three values
            if index < len(new_efficiency_values):
                plot_df.append({
                    'Sampler': sampler,
                    'Dose': dose,
                    'Efficiency': new_efficiency_values[index],
                    'Sample': f'{sampler} {dose.lower()} {i + 1}'
                })
                index += 1
            else:
                raise ValueError("Mismatch between provided efficiency values and expected data points.")

plot_df = pd.DataFrame(plot_df)
print(plot_df)

# Ensure the list is not accessed beyond its bounds
if index != len(new_efficiency_values):
    raise ValueError("Mismatch between provided efficiency values and expected data points.")

# Expand `plot_df` to match the number of efficiency values
expanded_plot_df = []
samplers = ['AerosolSense', 'Apollo', 'Cub', 'Inkfish']
doses = ['Low Dose', 'High Dose']

for sampler in samplers:
    for dose in doses:
        for i in range(3):
            expanded_plot_df.append({
                'Sampler': sampler,
                'Dose': dose,
                'Efficiency': new_efficiency_values.pop(0),
                'Sample': f'{sampler} {dose} {i + 1}'
            })

plot_df = pd.DataFrame(expanded_plot_df)

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
                marker=dict(symbol='diamond', size=16, color='orange', opacity=1),
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
    title='<b>PoD by sampler for inactivated SARS-CoV-2,<br>Salter</b>',
    title_x=0.5,
    title_font=dict(size=36),
    margin=dict(b=120),
    yaxis=dict(
        title='PoD (%)',
        title_font=dict(size=48),
        range=[0, 70],
        tickvals=np.arange(0, 80, 10),
        ticktext=[f"{i}%" for i in range(0, 80, 10)],
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
        y=-0.2,  # Slightly higher than the previous -0.25
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
        'text': '<b>PoD by sampler for inactivated SARS-CoV-2,<br>Salter</b>',
        'x': 0.5,
        'font': {'size': 36}
    },
    xaxis_title={
        'text': '',
        'font': {'size': 28}
    },
    yaxis_title={
        'text': 'PoD (%)',
        'font': {'size': 48}
    },
    legend={
        'font': {'size': 24}
    },
    xaxis={
        'tickfont': {'size': 22}  # Updated font size for sampler names
    },
    margin={
        'b': 120  # Increase bottom margin for annotation visibility
    }
)
fig.update_yaxes(title='PoD (%)', title_font={'size': 36}, range=[0, 70], showgrid=True, tickvals=np.arange(0, 80, 10), ticktext=[f"{i}%" for i in range(0, 80, 10)])
# Removed all previously added vertical lines
fig.update_layout(shapes=[])

# Adjust the existing vertical lines to ensure even spacing, consistent width, and proper placement
# Assuming the existing lines are part of the layout or added dynamically
for sampler, base in sampler_map.items():
    fig.add_shape(
        type="line",
        x0=base,  # Place the line at the center of each sampler
        x1=base,  # Ensure it is a single vertical line
        y0=0,
        y1=60,
        line=dict(color="rgba(100,100,100,0.7)", width=2)  # Consistent width
    )

# Explicitly specify the path to Google Chrome on macOS
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

# Display the graph as HTML in Google Chrome
html_file = "inkfish_virus_salter.html"
fig.write_html(html_file)
webbrowser.get("chrome").open(html_file)

# Adjusted annotations for better visibility
for sampler, base in sampler_map.items():
    for dose, x_pos in zip(['Low Dose', 'High Dose'], [base - 0.2, base + 0.2]):
        group = plot_df[(plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)]
        if not group.empty:
            for _, row in group.iterrows():
                fig.add_annotation(
                    x=row['x_offset'],
                    y=row['Efficiency'] + 1,  # Slightly offset above the point
                    text=f"{row['Efficiency']:.1f}%",  # Display efficiency value
                    showarrow=False,
                    font=dict(size=14),  # Increased font size for better readability
                    xanchor='center',
                    yanchor='bottom'
                )

# Adjusted average value annotations for better visibility
for sampler, base in sampler_map.items():
    for dose, x_pos in zip(['Low Dose', 'High Dose'], [base - 0.2, base + 0.2]):
        group = plot_df[(plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)]
        if not group.empty:
            mean_eff = group['Efficiency'].mean()
            fig.add_annotation(
                x=x_pos,
                y=mean_eff + 1,  # Slightly offset above the average marker
                text=f"{mean_eff:.1f}%",  # Display average value
                showarrow=False,
                font=dict(size=14, color='orange'),  # Increased font size for better readability
                xanchor='center',
                yanchor='bottom'
            )
# Ensure values for all data points and averages are displayed clearly
for sampler, base in sampler_map.items():
    for dose, x_pos in zip(['Low Dose', 'High Dose'], [base - 0.2, base + 0.2]):
        group = plot_df[(plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)]
        if not group.empty:
            for _, row in group.iterrows():
                fig.add_annotation(
                    x=row['x_offset'],
                    y=row['Efficiency'],
                    text=f"{row['Efficiency']:.1f}%",  # Display efficiency value
                    showarrow=False,
                    font=dict(size=14),  # Ensure readability
                    xanchor='left',
                    yanchor='middle'
                )

# Ensure annotations are properly added and visible
for sampler, base in sampler_map.items():
    for dose, x_pos in zip(['Low Dose', 'High Dose'], [base - 0.2, base + 0.2]):
        group = plot_df[(plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)]
        if not group.empty:
            for _, row in group.iterrows():
                fig.add_annotation(
                    x=row['x_offset'] + 0.15,  # Offset further to the right of the data point
                    y=row['Efficiency'],
                    text=f"{row['Efficiency']:.1f}%",  # Display efficiency value
                    showarrow=False,
                    font=dict(size=14, color='black'),  # Font size 14, black text
                    xanchor='left',
                    yanchor='middle'
                )

# Add annotations for average values
for sampler, base in sampler_map.items():
    for dose, x_pos in zip(['Low Dose', 'High Dose'], [base - 0.2, base + 0.2]):
        group = plot_df[(plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)]
        if not group.empty:
            mean_eff = group['Efficiency'].mean()
            fig.add_annotation(
                x=x_pos + 0.15,  # Offset further to the right of the average marker
                y=mean_eff,
                text=f"{mean_eff:.1f}%",  # Display average value
                showarrow=False,
                font=dict(size=14, color='black'),  # Font size 14, black text
                xanchor='left',
                yanchor='middle'
            )

# Add visible text annotations for each data point in the blank space
for sampler, base in sampler_map.items():
    for dose, x_pos in zip(['Low Dose', 'High Dose'], [base - 0.2, base + 0.2]):
        group = plot_df[(plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)]
        if not group.empty:
            for _, row in group.iterrows():
                fig.add_annotation(
                    x=row['x_offset'] + 0.15,  # Offset to the right of the data point
                    y=row['Efficiency'],
                    text=f"{row['Efficiency']:.1f}%",  # Display PoD value as text
                    showarrow=False,
                    font=dict(size=14, color='black'),  # Font size 14, black text
                    xanchor='left',
                    yanchor='middle'
                )
# Removed Inkfish sampler from the list of samplers
samplers = ['AerosolSense', 'Apollo', 'Cub', 'Inkfish']

# Exclude the Inkfish sampler
plot_df = plot_df[plot_df['Sampler'] != 'Inkfish']

# Save the graph as an SVG file with the new name
fig.write_image("Inkfish beads 0.5.svg")
