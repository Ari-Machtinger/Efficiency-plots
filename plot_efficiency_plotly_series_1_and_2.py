import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Use Series 1 data from provided CSV attachment
csv_file = 'Madison analysis for chamber study virus series.csv'
df1 = pd.read_csv(csv_file)

samplers = ['AerosolSense', 'Apollo', 'Cub']

# Fixed SettingWithCopyWarning by using .loc for assignment
def filter_df(df):
    df = df[df['Sample'].apply(lambda x: isinstance(x, str) and any(s in x for s in samplers) and 'SKC' not in x and 'blank' not in x)]
    def get_dose(sample):
        if 'low dose' in sample:
            return 'Low Dose'
        elif 'high dose' in sample:
            return 'High Dose'
        else:
            return None
    df.loc[:, 'Dose'] = df['Sample'].apply(get_dose)
    df = df[df['Dose'].notnull()]
    def get_sampler(sample):
        for s in samplers:
            if s in sample:
                return s
        return None
    df.loc[:, 'Sampler'] = df['Sample'].apply(get_sampler)
    df.loc[:, 'Efficiency'] = pd.to_numeric(df['Efficiency of capture based on APS'], errors='coerce') * 100
    return df

# Only process Series 1 data
df1 = filter_df(df1)

def build_plot_df(df, series_label):
    plot_df = []
    for sampler in samplers:
        for dose in ['Low Dose', 'High Dose']:
            group = df[(df['Sampler'] == sampler) & (df['Dose'] == dose)].head(3)
            for _, row in group.iterrows():
                plot_df.append({
                    'Sampler': sampler,
                    'Dose': dose,
                    'Efficiency': row['Efficiency'],
                    'Sample': row['Sample'],
                    'Series': series_label
                })
    return pd.DataFrame(plot_df)


# Only use series 1 data
plot_df = build_plot_df(df1, 'Series 1')

# Build x positions for each sampler/dose/series
sampler_map = {s: i for i, s in enumerate(samplers)}
plot_df['x_offset'] = 0.0
for sampler, base in sampler_map.items():
    for dose, dose_shift in zip(['Low Dose', 'High Dose'], [-0.1, 0.1]):
        x_pos = base + dose_shift
        mask = (plot_df['Sampler'] == sampler) & (plot_df['Dose'] == dose)
        plot_df.loc[mask, 'x_offset'] = x_pos

# Create plot
fig = go.Figure()
for sampler, base in sampler_map.items():
    for dose, dose_shift in zip(['Low Dose', 'High Dose'], [-0.1, 0.1]):
        x_pos = base + dose_shift
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
    marker=dict(size=12, color='blue'),
    text=plot_df['Sample'],
    name='Data Points',
    showlegend=False
))
# Save figure as PNG
fig.write_image("test png series 1 9_6.png")
# Save figure as PNG
fig.write_image("test png series 1 9_6.png")

# Build custom tick positions and labels for x axis
sampler_annotations = []
custom_ticks = []
custom_labels = []
for sampler, base in sampler_map.items():
    custom_ticks.extend([base - 0.1, base + 0.1])
    custom_labels.extend([
        '<span style="font-size:18px">Low</span>',
        '<span style="font-size:18px">High</span>'
    ])
    sampler_annotations.append({'x': base, 'text': sampler})

fig.update_layout(
    width=1100,
    height=700,
    title='<b>Capture efficiency of inactivated SARS-CoV-2 by sampler</b>',
    title_x=0.5,
    title_font=dict(size=28),
    margin=dict(b=170),
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
        tickangle=0,
        ticklabelstandoff=20
    ),
    showlegend=False
)
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
fig.write_image("efficiency_plot_series_1.svg")
fig.show()

# Save figure as an HTML file
html_file = "series_1_10_2.html"
fig.write_html(html_file)

# Open the HTML file in Google Chrome
import webbrowser
# Explicitly specify the path to Google Chrome on macOS
chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get("chrome").open(html_file)
