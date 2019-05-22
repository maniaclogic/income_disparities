
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import plotly.tools as tls


from disparities import GDt, GDc, df


v = GDc[['continents', 'gini', 'index', 'year']].dropna().set_index('continents')
trace1 = dict(x=v['year'], y=v['gini'], text=v['index'], type='scatter', mode='markers',
              transforms=[dict(type='groupby', groups=v.index)])
v = v.reset_index().set_index('year')
trace2 = dict(x=v.index, y=v['gini'], text=v['continents'], type='box',
              transforms=[dict(type='groupby', groups=v.index)])
rom = df[df['index'] == 'Romania'][['year', '%inc_highest20','%inc_fourth20','%inc_third20','%inc_second20' ,'%inc_low20']].set_index('year')
sa = df[df['index'] == 'South Africa'][['year', '%inc_highest20',
                                    '%inc_fourth20','%inc_third20', '%inc_second20',
                                    '%inc_low20']].set_index('year')

trace3 = dict(y=[100] + list(rom.iloc[0]) + [0], x=[100, 80, 60, 50, 40, 20, 0], type='scatter')
trace0 = dict(x=[0, 100], y=[0, 100], type='scatter')
trace4 = dict(y=[100] + list(sa.iloc[0]) + [0], x=[100, 80, 60, 50, 40, 20, 0], type='scatter')

data1 = [trace4, trace0]
data2 = [trace3, trace0]

data3 = [trace1, trace2]

layout = dict(title='Gini coefficient per continent',
              hovermode='closest', xaxis=dict(ticks=str(range(1986, 2007))), showticklabels=True, dtick=1,
              tickvals=list(GDc['year']))
layout1 = dict(title= 'Lorenz curve Romania 1989', hovermode='closest', showlegend=False, xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(text='% of population')), yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text='% of income')))
layout2 = dict(title= 'Lorenz curve South Africa 1993', hovermode='closest', showlegend=False, xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(text='% of population')), yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text='% of income')))
figt = dict(data=data3, layout=layout)
figrom = dict(data=data2, layout=layout1)
figsa = dict(data=data1, layout=layout2)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H2('M E A S U R I N G - I N E Q U A L I T Y'),
        html.Img(src='/assets/stats.png'),
    ], className='banner'),

    html.Div([
        dcc.Graph(id='live-choro'),
        dcc.Interval(id='choro-update', interval=1*2000, n_intervals=0)
        ], className='eight columns'),
    html.Div([
        dcc.Dropdown(id='d_year',
                     options=[{
                         'label': i,
                         'value': i} for i in sorted(list(GDc['year'].unique())[:-1])[1:]],
                     value='2000'),
    dcc.Graph(id='gini_by_year')], className='three columns'),
    html.Div([
        dcc.Graph(id='romania', figure=figrom)], className='five columns'),
    html.Div([
        dcc.Graph(id='southafrica', figure=figsa)
    ], className='five columns'),
    html.Div([
        dcc.Graph(id='stats-world',
                  figure=figt)
    ], className='twelve columns')

], className='row')

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

COUNT = 0

@app.callback(Output('live-choro', 'figure'),
            [Input('choro-update', 'n_intervals')])
def update_choro(n):

    yearls =sorted(list(GDc['year'].unique())[:-1])[1:]
    global COUNT

    if COUNT >= len(yearls):
        COUNT = 0
        year = yearls[COUNT]
        data_ch = (go.Choropleth(locations=GDc[GDc['year'] == year]['code'],
                                 z=GDc[GDc['year'] == year]['gini'],
                                 text=GDc[GDc['year'] == year]['index'],
                                 marker=go.choropleth.Marker(
                                     line=go.choropleth.marker.Line(color='rgb(180,180,180)', width=0.5))),)

        layout_ch = dict(title='GINI index worldwide '+ str(year), showlegend=True, legend=GDc['gini'], hovermode='closest',
                         geo=go.layout.Geo(showframe=False, projection=go.layout.geo.Projection(type='equirectangular'))
                         )

        COUNT += 1
    else:
        year = yearls[COUNT]
        data_ch = (go.Choropleth(locations=GDc[GDc['year'] == year]['code'],
                                 z=GDc[GDc['year'] == year]['gini'],
                                 text=GDc[GDc['year'] == year]['index'],
                                 marker=go.choropleth.Marker(
                                     line=go.choropleth.marker.Line(color='rgb(180,180,180)', width=0.5))),)

        layout_ch = dict(title='GINI index worldwide '+ str(year), showlegend=True, legend=GDc['gini'], hovermode='closest',
                         geo=go.layout.Geo(showframe=False, projection=go.layout.geo.Projection(type='equirectangular'))
                         )

        COUNT +=  1

    return dict(data=data_ch, layout=layout_ch)


gini_years = GDt.columns[3:]



@app.callback(Output('gini_by_year', 'figure'),
            [Input('d_year', 'value')])
def bar_grap(year):
    a = GDt[[year, 'GINI index']].dropna()
    trace = dict(x=list(a[year]), y=list(a['GINI index']), type='bar', orientation='h', autocolorscale=False, colorscale='Reds', showlegend=False,
                 transforms=[dict(type='groupby', groups=a[year])])

    layout = dict(hovermode='closest')
    p_fig = dict(data=[trace], layout=layout)

    return p_fig


if __name__ == '__main__':
    app.run_server(debug=True)


