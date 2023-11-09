from dash import dcc, html, Dash, Input, Output, dash_table
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#DATA READING

#Cryptos
ETH_data = pd.read_csv("./data/Crypto/ETH.csv", parse_dates=['Date'], date_format = "%Y-%m-%d")
SOL_data = pd.read_csv("./data/Crypto/SOL.csv", parse_dates=['Date'], date_format="%Y-%m-%d")
DOGE_data= pd.read_csv("./data/Crypto/DOGE.csv", parse_dates=['Date'], date_format="%Y-%m-%d")
LTC_data = pd.read_csv("./data/Crypto/LTC.csv", parse_dates=['Date'], date_format = "%Y-%m-%d")
XMR_data = pd.read_csv("./data/Crypto/XMR.csv", parse_dates=['Date'], date_format="%Y-%m-%d")
BTC_data = pd.read_csv("./data/Crypto/BTC.csv", parse_dates=['Date'], date_format="%Y-%m-%d")
XRP_data = pd.read_csv("./data/Crypto/XRP.csv", parse_dates=['Date'], date_format="%Y-%m-%d")

app = Dash(__name__, title='Portfolio Analysis')



CRYPTO = {
    "ETH"  : "ETHEREUM",
    "SOL"  : "SOLANA",
    "DOGE" : "DOGE COIN",
    'BTC' : 'BITCOIN',
    'LTC' : 'LITECOIN',
    'XRP' : 'RIPPLE',
    'XMR' : 'MONERO'
     }
CRYPTO_LIST = tuple(CRYPTO.keys())

def last_close(x):
    data = globals()[f'{x}_data']
    return data["Close"].iloc[-1]

crypto_dict = {
    "Tickers" : CRYPTO_LIST,
    "Company" : list(CRYPTO.values()),
    "Quantity" : [25, 250, 350000, 1, 250, 900, 45],
    "Price" : [last_close(crypto) for crypto in CRYPTO],
    "Value" : None,
    "Action": ["Buy", "Sell", "Hold", "Buy", "Sell", "Hold", 'Sell'],
}
crypto_summary_data = pd.DataFrame(crypto_dict)
crypto_summary_data['Value'] = crypto_summary_data['Quantity'].mul(crypto_summary_data['Price'])
crypto_summary_data_records = crypto_summary_data.to_dict('records')


@app.callback(
    Output('graph', 'figure'),
    Input("datatable", 'active_cell'),
)

def display_candlestick(active_cell):
    if active_cell['row'] == 0 :
        df = ETH_data.copy()
        name = 'ETHEREUM'
    elif active_cell['row'] == 1 :
        df = SOL_data.copy()
        name = 'SOLANA'
    elif active_cell['row'] == 2 :
        df = DOGE_data.copy()
        name = 'DOGE COIN'
    if active_cell['row'] == 3:
        df = BTC_data.copy()
        name = 'BITCOIN'
    elif active_cell['row'] == 4 :
        df = LTC_data.copy()
        name = 'LITECOIN'
    elif active_cell['row'] == 5 :
        df = XRP_data.copy()
        name = 'RIPPLE'
    elif active_cell['row'] == 6 :
        df = XMR_data.copy()
        name = 'MONERO'

        
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y")

    fig = go.Figure(
        go.Candlestick(
        x=df["Date"],
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
            )
        )
    fig.update_layout(
        title_text=f'Price Data of {name}',
        template="plotly",
        autosize=True,
        ) 
    return fig

def piechart():
    data = crypto_summary_data
    portfolio_total = data["Value"].sum()

    fig = px.pie(
        data,
        values="Value",
        names="Tickers",
        hole=0.4,
        title=f"Your total portfolio value is ₹{portfolio_total:,.0f}",

    )
    fig.layout.autosize = True
    return fig

Table = dash_table.DataTable(
            data=crypto_summary_data_records,
            columns=[{'id': c, 'name': c, 'editable': (c=='Quantity')} for c in crypto_summary_data.columns],
            sort_action='native',
            style_cell={'backgroundColor' : 'white', 'textAlign' : 'center'},
            style_header={'backgroundColor' : 'grey', 'fontWeight': 'bold', 'textAlign': 'center'},
            style_data_conditional=[
                {
                    'if': {
                        'filter_query': '{Action} = Sell',
                        'column_id': 'Action'
                    },
                    'color': 'tomato',
                    'fontWeight': 'bold'
                },
                {
                    'if': {
                        'filter_query': '{Action} = Buy',
                        'column_id': 'Action'
                    },
                    'color': 'green',
                    'fontWeight': 'bold'
                }
            ],
            style_as_list_view=True,
            id='datatable',
            active_cell={'row': 0, 'column': 0},

        )

app.layout = html.Div([

    html.Div([
        html.Div(['PORTFOIO ANALYZER'],className='top-left'),
        html.Div([
            dcc.Link("Market", href="#"),
            dcc.Link("Portfolio", href="#"),
            dcc.Link("Settings", href="#"),
            dcc.Link("Accounts", href="#"),], className='navbar'),
    ],
    className='top'),
    html.Div([html.Div([
        html.Div([
            html.Div([dcc.Graph(id='graph')], className='chart'),
            html.Div([dcc.Graph(figure=piechart())], className='pie-chart')
    ], className='graph-container'),
    html.Div(Table , className='table')
    ], className='container')
    
    
    
])
])



if __name__ == "__main__":
    app.run_server(debug=False)
