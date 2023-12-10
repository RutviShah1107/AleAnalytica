from flask import Flask, render_template, request, jsonify
import json
import pandas as pd
from .src.read_data import ReadData
from .src.cluster import Clustering
from .src.bar_graphs import BarGraphs
from .src.heatmap_columns import HeatmapColumns
from .src.attitude_columns_likert import AttitudeColumnsLikert

app = Flask(__name__, static_folder='static')

rdk = ReadData('./data/kantar6k.csv')
df = rdk.read_dataframe()
rda = ReadData('./data/preprocessed_data.csv')
df_analysis = rda.read_dataframe()
clust = Clustering(df_analysis, df)
        
with open('./data/cluster_names.json', 'r') as file:
    cluster_mapping = json.load(file)

cluster_names = list(cluster_mapping.values())

df['Cluster_number'] = df['Cluster']
df['Cluster'] = df['Cluster'].astype(str)
df['Cluster'] = df['Cluster'].map(cluster_mapping)

with open('./data/columns.json', 'r') as json_file:
    columns_dict = json.load(json_file)

@app.route('/')
def index():    
    return render_template('index.html')

@app.route('/demographic')
def demographic():
    return render_template('demographic.html')

@app.route('/attitudes-heatmaps')
def attitudes_heatmaps():
    return render_template('attitudes-heatmaps.html', attitudes = columns_dict['Attitudes'])


@app.route('/attitudes-likert')
def attitudes_likert():
    return render_template('attitudes-likert.html', attitudes = columns_dict['Attitudes'])

@app.route('/occasion')
def occasion():
    return render_template('occasion.html', occasion = columns_dict['Occasion Deep Dive'])

@app.route('/media')
def media():
    return render_template('media.html', media = columns_dict['Media Consumption'])


@app.route('/display/<endpoint>')
def display(endpoint):   
    if endpoint == "generateDendogram":
        p = int(request.args.get('p'))        
        clust = Clustering(df_analysis, df, p)
        df['Cluster'] = df['Cluster'].astype(str)
        df['Cluster'] = df['Cluster'].map(cluster_mapping)
        return clust.generate_graph()
    else:
        return "Bad endpoint", 400
    
@app.route('/demographic/<endpoint>')
def demographic_endpoint(endpoint):
    if endpoint == "generateDemographicGraph":
        demo_dict = {'Age': json.loads(BarGraphs(df, 'Age').generate_graph()),
                     'Gender': json.loads(BarGraphs(df, 'Gender').generate_graph()),
                     'Ethinicity': json.loads(BarGraphs(df, 'Ethinicity').generate_graph()),
                     'MaritalStatus': json.loads(BarGraphs(df, 'Marital Status').generate_graph()),
                     'EmploymentStatus': json.loads(BarGraphs(df, 'Employment Status').generate_graph()),
                     'Education': json.loads(BarGraphs(df, 'Education').generate_graph()),
                     'LivingArea': json.loads(BarGraphs(df, 'Living Area').generate_graph()),
                     'HHI': json.loads(BarGraphs(df, 'Household Income').generate_graph())}
        return json.dumps(demo_dict)
    else:
        return "Bad endpoint", 400

@app.route('/attitudes-heatmaps/<endpoint>')
def attitudes_heatmap_endpoint(endpoint):
    if endpoint == "generateAttitudeGraph":
        column = request.args.get('column')     
        hc = HeatmapColumns(df, column)
        return hc.generate_graph()
    else:
        return "Bad endpoint", 400

@app.route('/attitudes-likert/<endpoint>')
def attitudes_likert_endpoint(endpoint):
    if endpoint == "generateAttitudeGraph":
        column = request.args.get('column')  
        graph_dict = {}
        if column == 'A1' or column == 'A3':
            for i in range(1,9):
                graph_dict[i] = json.loads(AttitudeColumnsLikert(df, column, i).generate_graph_double())
        else:
            for i in range(1,9):
                graph_dict[i] = json.loads(AttitudeColumnsLikert(df, column, i).generate_graph_single())
        return json.dumps(graph_dict)
    else:
        return "Bad endpoint", 400

@app.route('/media/<endpoint>')
def media_endpoint(endpoint):
    if endpoint == "generateMediaGraph":
        column = request.args.get('column')     
        hc = HeatmapColumns(df, column)
        return hc.generate_graph()
    else:
        return "Bad endpoint", 400
    

@app.route('/occasion/<endpoint>')
def occasion_endpoint(endpoint):
    if endpoint == "generateOccasionGraph":
        column = request.args.get('column')  
        if column != "ODD1": 
            hc = HeatmapColumns(df, column)
            return hc.generate_graph()
        else:
            return BarGraphs(df, 'Most recent consumption day').generate_graph()
    else:
        return "Bad endpoint", 400