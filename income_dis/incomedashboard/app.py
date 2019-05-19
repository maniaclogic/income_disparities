import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

from disparities import df_inc, GDc


data = [go.Box(x = GDc[GDc['continents']==i]['year'],
                   y = GDc[GDc['continents']==i]['gini'],
                   text = GDc[GDc['continents']==i]['index'],
                   name=i) for i in GDc.continents.unique()]
def box_contin(x):
    res = [go.Bar(x=GDc[GDc['continents']==x]['year'],
                    y=GDc[GDc['continents']==x]['gini'],
                    text=GDc[GDc['continents']==x]['index'])]
    return res


layout = dict(title='Gini coefficient per continent',
              hovermode='closest')
def lay_contin(x):
    layout1 = dict(title='Gini coefficient ' + str(x))
    return layout1

fig = dict(data=data, layout=layout)
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
        dcc.Graph(id='continent-gini',
                  figure=fig),
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
])

app.css.append_css({
    'external_url':'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server(debug=True)