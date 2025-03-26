import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("finalnona.csv", encoding='ISO-8859-1')
df['monthdate'] = pd.to_datetime(df['monthdate'])
df['Revenue'] = df['OrderQuantity'] * df['ProductPrice']

# Grouped data
grouped_df = df.groupby(['monthdate', 'CategoryName'], as_index=False).agg({
    'OrderQuantity': 'sum',
    'Revenue': 'sum'
})

# App initialization
app = dash.Dash(__name__)
app.title = "Paiman Portfolio Dashboard"

app.layout = html.Div([
    html.H1("Paiman Sales Dashboard", style={'textAlign': 'center'}),

    html.Label("Select Product Category:"),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat} for cat in df['CategoryName'].unique()],
        value=df['CategoryName'].unique()[0]
    ),

    html.Div([
        dcc.Graph(id='sales-trend', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='revenue-trend', style={'display': 'inline-block', 'width': '48%'})
    ]),

    html.Div([
        dcc.Graph(id='top-products', style={'display': 'inline-block', 'width': '48%'}),
        dcc.Graph(id='region-sales', style={'display': 'inline-block', 'width': '48%'})
    ])
])

# Callbacks
@app.callback(
    Output('sales-trend', 'figure'),
    Output('revenue-trend', 'figure'),
    Output('top-products', 'figure'),
    Output('region-sales', 'figure'),
    Input('category-dropdown', 'value')
)
def update_charts(selected_category):
    filtered_group = grouped_df[grouped_df['CategoryName'] == selected_category]
    filtered_data = df[df['CategoryName'] == selected_category]

    fig1 = px.line(filtered_group, x='monthdate', y='OrderQuantity', title='Sales Trend')
    fig2 = px.line(filtered_group, x='monthdate', y='Revenue', title='Revenue Over Time')

    top_products = filtered_data['ProductName'].value_counts().nlargest(10).reset_index()
    fig3 = px.bar(top_products, x='index', y='ProductName', title='Top 10 Products', labels={'index': 'Product Name', 'ProductName': 'Count'})

    fig4 = px.bar(filtered_data, x='Region', y='OrderQuantity', title='Sales by Region', color='Region')

    return fig1, fig2, fig3, fig4

if __name__ == '__main__':
    app.run(debug=True)
