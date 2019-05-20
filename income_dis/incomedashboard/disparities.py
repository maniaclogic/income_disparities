import pandas as pd


high10 = pd.read_excel('dependencies/Indicator_Income share held by highest 10%.xlsx', index_col=0)
high20 = pd.read_excel('dependencies/Indicator_Income share held by highest 20%.xlsx', index_col=0)
sec20 = pd.read_excel('dependencies/Indicator_Income share held by second 20%.xlsx', index_col=0)
thi20 = pd.read_excel('dependencies/Indicator_Income share held by third 20%.xlsx', index_col=0)
four20 = pd.read_excel('dependencies/Indicator_Income share held by fourth 20%.xlsx', index_col=0)
low20 = pd.read_excel('dependencies/indicator SI_DST_FRST_20.xls.xlsx', index_col=0)
low10 = pd.read_excel('dependencies/Indicator_Income share held by lowest 10%.xlsx', index_col=0)


num_bill = pd.read_excel('dependencies/Indicator_number of billionaires.xlsx', index_col=0)
rel_num_bill = pd.read_excel('dependencies/Indicator_Number of billionaires per 1 million inhabitants.xlsx', index_col=0)
avg_age_bill = pd.read_excel('dependencies/Indicator_Average age.xlsx', index_col=0)

gini = pd.read_excel('dependencies/indicator SI_POV_GINI.xls.xlsx', index_col=0)

shigh20 = high20.stack()
ssec20 = sec20.stack()
sthi20 = thi20.stack()
sfour20 = four20.stack()
slow20 = low20.stack()

d = {'%inc_highest20': shigh20, '%inc_second20': ssec20, '%inc_third20': sthi20, '%inc_fourth20': sfour20, '%inc_low20': slow20}
df_inc = pd.DataFrame(data=d).reset_index()
df_inc = df_inc.rename(columns={'Income share held by highest 20%': 'country', 'level_1': 'year'}).set_index('country')
df_inc[['%inc_highest20', '%inc_second20', '%inc_third20', '%inc_fourth20', '%inc_low20']] = round(df_inc[['%inc_highest20', '%inc_second20', '%inc_third20', '%inc_fourth20', '%inc_low20']])

snum = num_bill.stack()
srel = rel_num_bill.stack()
savg = avg_age_bill.stack()

d = {'count billionaires': snum, 'number of billionaires per 1 million': srel, 'average age billionaires': savg}
df2 = pd.DataFrame(data=d).reset_index()
df2 = df2.rename(columns={'Total number of billionaires': 'country', 'level_1': 'year'}).set_index('country')
df2 = df2[df2['count billionaires'] != 0]
df2['average age billionaires'] = [int(i) for i in df2['average age billionaires']]

GD = gini.transpose().dropna(1, how='all')

d = {'Argentina': 'South America', 'Australia': 'Australia', 'Austria': 'Europe', 'Belgium': 'Europe', 'Brazil': 'South America', 'Canada': 'North America', 'Chile': 'South America', 'China': 'Asia', 'Colombia': 'South America', 'Cyprus': 'Asia', 'Czech Rep.': 'Europe', 'Denmark': 'Europe', 'Egypt': 'Africa', 'France': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe', 'Hong Kong, China': 'Asia', 'Iceland': 'Europe', 'India': 'Asia', 'Indonesia': 'Asia', 'Ireland': 'Europe', 'Israel': 'Asia', 'Italy': 'Europe', 'Japan': 'Asia', 'Kazakhstan': 'Asia', 'Korea Rep.': 'Asia', 'Kuwait': 'Asia', 'Lebanon': 'Asia', 'Liechtenstein': 'Europe', 'Malaysia': 'Asia', 'Mexico': 'North America', 'Monaco': 'Europe', 'Netherlands': 'Europe', 'New Zealand': 'Australia', 'Norway': 'Europe', 'Oman': 'Asia', 'Philippines': 'Asia', 'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe', 'Russia':'Europe', 'Saudi Arabia': 'Asia', 'Serbia': 'Europe', 'Singapore': 'Asia', 'South Africa': 'Africa', 'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe', 'Taiwan': 'Asia', 'Thailand': 'Asia', 'Turkey': 'Asia', 'Ukraine': 'Europe', 'United Arab Emirates': 'Asia', 'United Kindom': 'Europe', 'United States': 'North America', 'Venezuela': 'South America'}
a = {'Argentina': 'ARG', 'Australia':'AUS', 'Austria':'AUT', 'Belgium':'BEL', 'Brazil':'BRA', 'Canada':'CAN', 'Chile':'CHL', 'China':'CHN', 'Colombia':'COL', 'Cyprus':'CYP', 'Czech Republic':'CZE', 'Denmark':'DNK', 'Egypt':'EGY', 'France':'FRA', 'Germany':'DEU', 'Greece':'GRC', 'Hong Kong, China':'CHN', 'Iceland':'ISL', 'India':'IND', 'Indonesia':'IDN', 'Ireland':'IRL', 'Israel':'ISR', 'Italy':'ITA', 'Japan':'JPN', 'Kazakhstan':'KAZ', 'Korea Rep.':'KOR','Kuwait':'KWT', 'Lebanon':'LBN', 'Liechtenstein':'LIE', 'Malaysia':'MYS', 'Mexico':'MEX', 'Monaco':'MCO', 'Netherlands':'NLD', 'New Zealand':'NZL', 'Norway':'NOR', 'Oman':'OMN', 'Phillippines':'PHL', 'Poland':'POL', 'Portugal':'PRT', 'Romania':'ROU', 'Russia':'RUS', 'Saudi Arabia':'SAU', 'Serbia':'SRB', 'Singapore':'SGP', 'South Africa':'ZAF', 'Spain':'ESP', 'Sweden':'SWE', 'Switzerland': 'CHE', 'Taiwan':'TWN', 'Thailand':'THA', 'Turkey':'TUR', 'Ukrain':'UKR', 'UnitedArab Emirates':'ARE', 'United Kingdom':'GBR', 'United States':'USA', 'Venezuela':'VEN'}
d = pd.DataFrame(data=d, index=range(len(d))).transpose()[0]
a = pd.DataFrame(data=a, index=range(len(a))).transpose()[0]
df = pd.DataFrame(d)
a = pd.DataFrame(a)
df.columns = ['continents']
a.columns=['code']
df_inc = df_inc.merge(df, left_index=True, right_index=True).dropna()
df_inc = df_inc.merge(a,left_index=True, right_index=True)
GDc = pd.DataFrame(data={'gini':GD.stack()}).reset_index()
GDc = GDc.rename(columns={'GINI index': 'country', 'level_0': 'year'})
GDc.set_index(['country'], inplace=True)
GDc = GDc.merge(a, left_index=True, right_index=True).reset_index()
GDc.set_index(['index'], inplace=True)
GDc = GDc.merge(df, left_index=True, right_index=True).reset_index()

GD_list = list(GD.transpose().index)
GDt = GD.transpose().reset_index()
