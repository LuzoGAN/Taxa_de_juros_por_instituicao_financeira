# Importações
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px

# Tratamento da Base
df = pd.read_excel("https://www.bcb.gov.br/conteudo/txcred/Documents/taxascredito.xls",sheet_name=2 , skiprows=4)
df3 = df.drop(['Unnamed: 5','Unnamed: 6'], axis=1)
df3 = df.drop(0)
df3.drop(['Unnamed: 5','Unnamed: 6'], axis=1, inplace=True)
df3['MODALIDADE'].fillna(method='ffill', inplace=True)
df3.replace(' ', None, inplace=True)
df3.dropna(axis=1, how='all')
remo = df3.loc[df3['POSIÇÃO'].isna()]
df_final = df3.drop(remo.index)
df_final['MODALIDADE'].fillna(method='ffill', inplace=True)


# Inicialização
app = Dash(__name__)

# Layout
#app.layout = html.Div([
#    html.Div(children='Taxa de juros por instituição financeira'),
#    dash_table.DataTable(data=df_final.to_dict('Records'),page_size=10)
#])
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Taxas de juros por instituição finaceira', className='text-primary text-center fs-3')
    ]),

    dbc.Row([
        dbc.RadioItems(options=[{'label': x, 'value':x} for x in ['TAXAS MÉDIAS','TAXAS MÉDIAS.1']],
                       value='TAXAS MÉDIAS',
                       inline=True,
                       id='radio-buttons-final')
    ]),

    dbc.Row([
        dbc.Col([dash_table.DataTable(data=df_final.to_dict('records'), page_size=12)]),

        dbc.Col([
            dcc.Graph(figure={}, id='my-fist-graph-final')
        ])
    ])
], fluid= True)

# Controles
@callback(
    Output(component_id='my-fist-graph-final', component_property='figure'),
    Input(component_id='radio-buttons-final', component_property='value')
)

def update_graph(col_chosen):
    fig = px.histogram(df_final, x='MODALIDADE', y=col_chosen, histfunc='sum')
    return fig

# Run
if __name__ == '__main__':
    app.run(debug=True)