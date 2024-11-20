import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import plotly.graph_objs as go


from disparities import GDt, GDc, df


v = GDc.dropna().set_index('continents')
trace1 = dict(x=v['year'], y=v['gini'], text=v.index, type='scatter', mode='markers',
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
layout1 = dict(title= 'Lorenz curve Romania 1989', hovermode='closest', showlegend=False, xaxis=dict(title='% of population'), yaxis=dict(title='% of income'))
layout2 = dict(title= 'Lorenz curve South Africa 1993', hovermode='closest', showlegend=False, xaxis=dict(title='% of population'), yaxis=dict(title='% of income'))
figt = dict(data=data3, layout=layout)
figrom = dict(data=data2, layout=layout1)
figsa = dict(data=data1, layout=layout2)

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.Div([
        html.H3('M E A S U R I N G - I N E Q U A L I T Y'),
        html.Img(src='/assets/stats.png'),
    ], className='banner'),

    html.Div([
    dcc.Markdown('''
    ***
    ## Measuring inequality
    Is it possible? Well, kind of.
    We can utilize the statistic measurement called Gini index or Gini coefficient, which aspires to do just that.
    It measures the distribution of income or wealth across different percentiles in a population, usually countries.

    >A Gini index of 0 represents perfect equality,

    >a Gini index of 100 represents perfect inequality.

    Here is a map colored with the Gini indices around the world where data was available.
    If you want to have a closer look at different years, you may utilize the dropdown next to it.
    '''.replace('  ', ''),
        className='container',
        style={'maxWidth': '650px'}
)
    ], className='five columns offset-by-one column'),
    html.Div([
        dcc.Markdown('''
        ***
        ***
        Here we have Gini indices of the income distributions. The difference between the wealth and income Gini indices is not insignificant.
        A wealth index can be over 100 (or 1 if measured in coefficient) since it is possible to have a high income
        but 0 or negative net worth.

        It is also important to note that data availability is an issue since we can only compute the Gini coefficient
        if we have GDPs reported by countries, as well as the distribution among the population.
        Furthermore the Gini index only focuses on one criteria. It does not consider
        other markers that are important measures of equality: race, religion, gender, and social status for example.

        >Note:
        A largely retired population tends to result in a higher Gini coefficient
        since they contribute to the population count but don't generate income.
        '''.replace('  ', ''),
                    className='container',
                     style={'maxWidth': '650px'})
    ], className='five columns'),

    html.Div([
        dcc.Graph(id='live-choro'),
        dcc.Interval(id='choro-update', interval=1*2000, n_intervals=0)
        ], className='seven columns'),
    html.Div([
        dcc.Dropdown(id='d_year',
                     options=[{
                         'label': i,
                         'value': i} for i in sorted(list(GDc['year'].unique())[:-1])[1:]],
                     value='2000'),
    dcc.Graph(id='gini_by_year')], className='three columns'),
    html.Div([
        dcc.Graph(id='romania', figure=figrom),
        dcc.Graph(id='southafrica', figure=figsa)
    ], className='six columns offset-by-one column'),
    html.Div([
        dcc.Markdown('''
        ## Lorenz Curve
        The Gini coefficient is calculated by plotting the percentage of income that is held by
        quantiles of the population against perfect equality and calculating the ratio of area
        of the triangle to that under the Lorenz curve.

        If you that was too abstract for you, lets break it down.

        If you look at either Graph to the left of this text, you see an orange line.
        This is what perfect equality would look like. Each 20 percent of the population control 20 percent of the income.
        The blue line shows what is actually the case.
        >The gini coefficient can be thought of as the difference between equality and actuality.

        Now imagine our orange line building a triangle with the xaxis and the end of the graph.
        The blue line goes through it. Dividing the triangle into two areas.
        Area A will be between the orange line and the blue line, Area B will be between the blue line and the
        xaxis/end of graph.
        Using trigonometry we can determine the value of Area A and Area B. Now we Subtract Area B from Area A and we get
        a value between 0 and 1 (of course ignoring wealth coefficients). This is the Gini coefficient for that country
        in that year. The Gini Index is nothing other than the Gini coeffcient * 100, therefore normalizing the values to percentages.

        '''.replace('  ', ''), className='container',
                                style={'maxWidth':'650px'}
                                )
    ],className='three columns'),
    html.Div([

    ]),
    html.Div([
        dcc.Graph(id='stats-world',
                  figure=figt),
        dcc.Markdown('''
        ### Boxplots

        Boxplots allow for a statistical visualization of data to quickly analyze its spread, variance and determine outliers. Overlayed with a swarm plot which represents the data as points, it enables us to quickly distinguish important data points from each other.

        For example, one can quickly isolate the min and max values in the analyzed dataset corresponding to Romania in 1989 and South Africa in 2006 respectively from the green and brown dots; the former corresponds to European nations while the later depicts Africa.
        These two extremes were, therefore, chosen for our Lorenz curves. The rectangular slabs represent the data as boxplots (trace1 in the legend) while the points correspond to swarm plots of our data points (trace 0 in the legend). The median for every year is represented as a horizontal line within the box plots.

        The height of the boxes in the boxplot are indicative of the middle two quartiles of the data in each year, meaning that most of the data points fall within this range. The extending lines, also called whiskers, are indicative of the extremities of the data points;
        we see an interesting narrowing in the spread of data in recent years. Furthermore, the median for each year since 1993 consistently has a value of under 50, suggesting that the world as a whole is relatively equal in terms of its income distribution.
        Within each continent though, the European countries differ from each other the least as can be seen as the proximity of the green dots to each other. Considering that there are a large number of data points from European countries in more recent years,
        it is easily inferred that these data points equalize the distribution of income among low and high earners.

        Apart from the median and the spread of the data, the precise location of data points grouped by continent can be isolated through the quartiles they fall into (represented by the horizontal lines at multiple of twentyfive). South American countries consistently
        have higher Gini indices than European countries. African countries have higher values as well, with the exception of Egypt, which consistently returns values in and around 30.
        Asian, Australian and North American countries fall approximately between the second and the third quartile of the data.
        '''.replace('  ', ''),
                     className='container',
                     style={'maxWidth':'2400px'})
    ], className='twelve columns'),


    html.Div([
    dcc.Markdown('''
    ***
    ###### Build in Dash with data from Gapminder
    This application was written in Python with the Dash framework.

    Gapminder is an independent Swedish foundation with no political,
    religious or economic affiliations. Gapminder is a fact tank, not a think tank.
    It fights misconceptions about global development.
    And also produces free teaching resources and provides free cleaned data,
    aspiring to make the world understandable based on reliable statistics.
    Gapminder promotes a fact-based worldview everyone can understand.

    [&rarr; Check out Dash &larr;](https://plot.ly/)  &nbsp; [&rarr; Check out Gapminder &larr;](https://www.gapminder.org) &nbsp; [&rarr; Source Code &larr;](https://github.com/maniaclogic/income_disparities/blob/master/income_dis/incomedashboard/app.py)
    ***
    '''.replace('  ', ''),
        className='container',
        style={'maxWidth': '800px', 'place-items': 'center'}
)], className='ten columns')

], className='row')

COUNT = 0

@app.callback(Output('live-choro', 'figure'),
            [Input('choro-update', 'n_intervals')])
def update_choro(n):

    yearls =sorted(list(GDc['year'].unique()))
    global COUNT

    if COUNT >= len(yearls):
        COUNT=0
        year = yearls[COUNT]
        data_ch = (go.Choropleth(locations=GDc[GDc['year'] == year]['code'],
                                 z=GDc[GDc['year'] == year]['gini'],
                                 text=GDc[GDc['year'] == year].index,
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
                                 text=GDc[GDc['year'] == year].index,
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
