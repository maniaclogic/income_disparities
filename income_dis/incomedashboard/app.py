import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.tools as tls
import pandas as pd
from plotly.graph_objs._box import Box
from plotly.graph_objs._scatter import Scatter
import numpy as np

from disparities import df_inc, GDc

data_ch = (go.Choropleth(locations=GDc[GDc['year'] == '2000']['index'],
                         z=GDc[GDc['year'] == '2000']['gini'],
                         text=GDc['index'],
                         marker=go.choropleth.Marker(
                             line=go.choropleth.marker.Line(color='rgb(180,180,180)', width=0.5))),)

v = GDc[['continents', 'gini', 'index', 'year']].dropna().set_index('continents')
trace1 = dict(x=v['year'], y=v['gini'], text=v['index'], type='scatter', mode='markers',
              transforms=[dict(type='groupby', groups=v.index)])
v = v.reset_index().set_index('year')
trace2 = dict(x=v.index, y=v['gini'], text=v['continents'], type='box',
              transforms=[dict(type='groupby', groups=v.index)])
v.reset_index(inplace=True)
trace3 = dict(x=sorted(list(v['year'].unique())), y=GDc.groupby(['year'])['gini'].median(), type='line')


def box_contin(x):
    res = [go.Bar(x=GDc[GDc['continents'] == x]['year'],
                  y=GDc[GDc['continents'] == x]['gini'],
                  text=GDc[GDc['continents'] == x]['index'])]
    return res


data3 = [trace1, trace2]

layout = dict(title='Gini coefficient per continent',
              hovermode='closest', xaxis=dict(ticks=str(range(1986, 2007))), showticklabels=True, dtick=1,
              tickvals=list(GDc['year']))

layout_ch = dict(title='GINI index worldwide in 2000', showlegend=True, legend=GDc['gini'], hovermode='closest',
                 geo=go.layout.Geo(showframe=False, projection=go.layout.geo.Projection(type='equirectangular')))


def lay_contin(x):
    layout1 = dict(title='Gini coefficient ' + str(x))
    return layout1


fig = dict(data=data_ch, layout=layout_ch)

figt = dict(data=data3, layout=layout)

fig1 = dict(data=box_contin('South America'), layout=lay_contin('South America'))
fig2 = dict(data=box_contin('Australia'), layout=lay_contin('Australia'))
fig3 = dict(data=box_contin('Europe'), layout=lay_contin('Europe'))
fig4 = dict(data=box_contin('North America'), layout=lay_contin('North America'))
fig5 = dict(data=box_contin('Asia'), layout=lay_contin('Asia'))
fig6 = dict(data=box_contin('Africa'), layout=lay_contin('Africa'))

app = dash.Dash()

app.layout = html.Div([
    html.Div([
        html.H2('E Q U A L I T Y '),
        html.Img(src='/assets/stats.png'),
    ], className='banner'),

    html.Div([
        dcc.Graph(id='gini',
                  figure=figt)]),
    html.Div([
        dcc.Graph(id='ch_world',
                  figure=fig)
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='South-gini',
                      figure=fig1)], className='six columns'),
        html.Div([
            dcc.Graph(id='Australia-gini',
                      figure=fig2)], className='six columns'),
        html.Div([
            dcc.Graph(id='Europe-gini',
                      figure=fig3)], className='five columns'),
        html.Div([
            dcc.Graph(id='North-gini',
                      figure=fig4)], className='five columns'),
        html.Div([
            dcc.Graph(id='Asia-gini',
                      figure=fig5)], className='five columns'),
        html.Div([
            dcc.Graph(id='Africa-gini',
                      figure=fig6)], className='five columns'),
    ], className='row')
])

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)
