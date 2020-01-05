import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy

import pickle

########### Define your variables
beers=['Chesapeake Stout', 'Snake Dog IPA', 'Imperial Porter', 'Double Dog IPA']
ibu_values=[35, 60, 85, 75]
abv_values=[5.4, 7.1, 9.2, 4.3]
color1='lightblue'
color2='darkgreen'
mytitle='Beer Comparison'
tabtitle='beer!'
myheading='Flying Dog Beers'
label1='IBU'
label2='ABV'
githublink='https://github.com/austinlasseter/flying-dog-beers'
sourceurl='https://www.flyingdog.com/beers/'
data = 'response'

########### Set up the chart

data = pickle.load(open('response/precalc_spec_acistest.pkl', 'rb'))

binedges = data['ebins']
displayspec = numpy.append(1e-40, data[30])

trace1 = go.Scatter(x=binedges, y=displayspec,
            line=dict(
                shape = 'hv',
                color = '#9467bd'
            ),
            mode='lines',
            name='Plot')
#bitterness = go.Bar(
#    x=beers,
#    y=ibu_values,
#    name=label1,
#    marker={'color':color1}
#)
#alcohol = go.Bar(
#    x=beers,
#    y=abv_values,
#    name=label2,
#    marker={'color':color2}
#)

#beer_data = [bitterness, alcohol]
#beer_layout = go.Layout(
#    barmode='group',
#    title = 
 
xaxis='keV'
xaxis_type='Linear'
yaxis_type='Linear'
    
ret = {
     'data': [trace1],
    'layout': go.Layout(
            xaxis={'title': xaxis, 'type': 'linear' if xaxis_type == 'Linear' else 'log'},
            yaxis={
                'title': 'Emissivity*Aeff (ph cm^5 s^-1 bin^-1)',
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
                },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            #legend={'x': 0, 'y': 1},
            hovermode='closest',
            uirevision = True,
            showlegend=False,
        )
    }
    


beer_fig = go.Figure(data=ret['data'], layout=ret['layout'])


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='flyingdog',
        figure=beer_fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A('Data Source', href=sourceurl),
    ]
)

if __name__ == '__main__':
    app.run_server()
