import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

tips = px.data.tips()
col_options = [dict(label=x, value=x) for x in tips.columns]
dimensions = ["x", "y", "color"]

app = dash.Dash(
    __name__, external_stylesheets=["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css", "style.css"]
)

server = app.server

dropdown_menu = [
                    html.P([(d.replace('_', ' ') + ":").title(), dcc.Dropdown(id=d, options=col_options)]) 
                    for d in dimensions
                ]
dropdown_menu.insert(0, html.H6("Select columns to show in plot:"))
app.layout = html.Div(
    [
        html.H1("Demo: Plotly Express with Dash", style={'textAlign': 'center'}),
        html.Hr(className='hrStyle'),
        html.Div(
            dropdown_menu,
            style={"width": "25%", "float": "left", "marginTop": "4rem"},
        ),
        dcc.Graph(
            id="graph", 
            style={"width": "75%", "display": "inline-block"},
            config={
                'displayModeBar': True
            }
        )
    ],
    className='container'
)

@app.callback(Output("graph", "figure"), [Input(d, "value") for d in dimensions])
def make_figure(x, y, color):
    return px.scatter(
        tips,
        x=x,
        y=y,
        color=color,
        height=700,
        size='size',
        template='plotly_white',
        title={
            'text': 'Tips Data Scatter Plot',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
    )

if __name__ == "__main__":
    app.run_server()