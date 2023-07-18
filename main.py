# Importações
from dash import Dash, html, dash_table
import pandas as pd

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
app.layout = html.Div([
    html.Div(children='Taxa de juros por instituição financeira'),
    dash_table.DataTable(data=df_final.to_dict('Records'),page_size=10)
])

# Run
if __name__ == '__main__':
    app.run(debug=True)