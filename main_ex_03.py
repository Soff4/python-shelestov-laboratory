import plotly.graph_objs as go
import numpy as np
import dash
from dash import dcc
from dash import html
from plotly.subplots import make_subplots

# Функція для генерації даних
def generate_data():
    x = np.linspace(0, 2*np.pi, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    return x, y1, y2

def custom_filter(data, filter_type='none'):
    if filter_type == 'none':
        return data
    elif filter_type == 'low_pass':
        # Реалізуйте ваш фільтр, наприклад, низькочастотний фільтр
        filtered_data = np.convolve(data, np.ones(10)/10, mode='same')
        return filtered_data
    elif filter_type == 'high_pass':
        # Реалізуйте ваш фільтр, наприклад, високочастотний фільтр
        filtered_data = data - np.convolve(data, np.ones(10)/10, mode='same')
        return filtered_data
    else:
        return data

x, y1, y2 = generate_data()

# Створення графіку
fig = make_subplots(rows=2, cols=1, subplot_titles=['Low-pass filter Graph', 'High-pass filter Graph'])

trace1 = go.Scatter(x=x, y=y1, mode='lines', name='Low-pass filter Graph')
fig.add_trace(trace1, row=1, col=1)

trace2 = go.Scatter(x=x, y=y2, mode='lines', name='High-pass filter Graph')
fig.add_trace(trace2, row=2, col=1)

# Створення layout для Dash
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Data visualization and filtering'),

    dcc.Dropdown(
        id='filter-dropdown',
        options=[
            {'label': 'No filter', 'value': 'none'},
            {'label': 'Low-pass filter', 'value': 'low_pass'},
            {'label': 'High-pass filter', 'value': 'high_pass'}
        ],
        value='none',
        style={'width': '35%'}
    ),

    dcc.Graph(
        id='graph',
        figure=fig,
        style={'height': '70vh', 'width': '60vw'}
    )
])

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('filter-dropdown', 'value')]
)
def update_graph(selected_filter):
    filtered_y1 = custom_filter(y1, selected_filter)
    filtered_y2 = custom_filter(y2, selected_filter)

    fig.data[0].y = filtered_y1
    fig.data[1].y = filtered_y2

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)