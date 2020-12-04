import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff

# function to remove equal sign
def remove_sign(string):
  for i in string:
    if "=" in string:
        string=string[1:]
    return string

# function to calculate the female male ratio
def convertGender (x):
    a, b= x.split(':')
    c = int(a)/int(b)
    return c

# function to remove the percentage sign
def remove_pct(string):
  for i in string:
    if "%" in string:
        string=string[:-1]
    return string

df = pd.read_csv('/home/caroline09/projects/Reporting/top50_2016.csv')

df2=df.copy().dropna()

df2['world_rank']=df2['world_rank'].apply(remove_sign)
df2.international_students = [str(each).replace('%','') for each in df2.international_students]
df2.international_students = pd.to_numeric(df2.international_students, errors='coerce')
df2.international_students = [int(each) for each in df2.international_students]
df2['num_students']=df2['num_students'].apply(lambda x :x.replace(',', ''))
df2['female_male_ratio']=df2['female_male_ratio'].apply(convertGender)
df2['female_male_ratio']=round(df2['female_male_ratio'],2)

cols=['world_rank','international','income','total_score','num_students']

for col in df2.columns:
    if col in cols:
        df2[col]=pd.to_numeric(df2[col], errors='coerce')


# Create the scatter plot
fig1 = px.scatter(df2, x="world_rank", y="research",
                 hover_name="university_name",
                 title="Research vs Rank for the top 50 universities")


# Create a bar plot for the top five universities
dftop5=df2.iloc[:5,:]
trace1 = {
  'x': dftop5.university_name,
  'y': dftop5.citations,
  'name': 'citations',
  'type': 'bar'
}
trace2 = {
  'x': dftop5.university_name,
  'y': dftop5.teaching,
  'name': 'teaching',
  'type': 'bar'
}
data = [trace1, trace2]
layout = {
  'xaxis': {'title': 'Top 5 of best universities'},
  'barmode': 'relative',
  'title': 'Citations and teaching of the top 5 universities in 2016'
}
fig2 = go.Figure(data = data, layout = layout)


# Create a bubble chart

num_students_size  = df2.num_students/1000
international_color = [float(each) for each in df2.international]

hover_text = []


for index, row in df2.iterrows():
    hover_text.append(('Country: {country}<br>'+
                      'University: {university_name}<br>'+
                       'Number of students:{number_students}').format(country=row['country'],
                                                              university_name=row['university_name'],
                                                              number_students=row['num_students']))
    
df2['text'] = hover_text

fig3 = go.Figure(data=[go.Scatter(
    x=df2.world_rank,
    y=df2.teaching,
    mode='markers',
    text=df2['text'],
    marker=dict(
        color=international_color,
        size=num_students_size,
        showscale=True,
        colorbar={'title':'Score <br> international (%)'}
        )
)])

fig3.update_layout(
    title='Teaching v. World Rank',
    xaxis=dict(
        title='World Rank',
        gridcolor='white',
        gridwidth=2,
    ),
    yaxis=dict(
        title='Teaching Criteria(%)',
        gridcolor='white',
        gridwidth=2,
    ),
    paper_bgcolor='rgb(243, 243, 243)',
    plot_bgcolor='rgb(243, 243, 243)',
)

# Principal components analysis
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
features = df2[['world_rank','teaching','international','research','income','total_score','num_students','student_staff_ratio','international_students','female_male_ratio']]
std_scale = preprocessing.StandardScaler().fit(features)
X_scaled = std_scale.transform(features)
n_components = 4
pca = PCA(n_components=n_components)
pca.fit(X_scaled)

total_var = pca.explained_variance_ratio_.sum() * 100

labels = {
    str(i): f"PC {i+1} ({var:.1f}%)"
    for i, var in enumerate(pca.explained_variance_ratio_ * 100)
}



# Display pca matrix
pca2 = PCA()
pca2.fit(X_scaled)
fig4 = px.scatter_matrix(
    X_scaled,
    labels=labels,
    dimensions=range(n_components),
    height=800,
    title=f'Total Explained Variance: {total_var:.2f}%',
)
fig4.update_traces(diagonal_visible=False)

exp_var_cumul = np.cumsum(pca2.explained_variance_ratio_)

# Display explained variance graph
fig5 = px.area(
    x=range(1, exp_var_cumul.shape[0] + 1),
    y=exp_var_cumul,
    labels={"x": "# Components", "y": "Explained Variance"}
)


# Visualize Loadings
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

fig6 = px.scatter(X_scaled, x=0, y=1)

for i, feature in enumerate(features):
    fig6.add_shape(
        type='line',
        x0=0, y0=0,
        x1=loadings[i, 0],
        y1=loadings[i, 1]
    )
    fig6.add_annotation(
        x=loadings[i, 0],
        y=loadings[i, 1],
        ax=0, ay=0,
        xanchor="center",
        yanchor="bottom",
        text=feature,
    )

# Visualize heatmap
df_corr=np.array(features.corr())
df_corr=np.around(df_corr, decimals=2)

fig7 = ff.create_annotated_heatmap(df_corr)