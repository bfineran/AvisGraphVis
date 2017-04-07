
# coding: utf-8

# In[64]:

import pandas as pd
import numpy as np
from random import randint
import datetime
import math
import json


data = pd.read_csv('PricingData_top_2_markets.csv')
data = data[data['market_group'] == 'LAX']
data = data.sample(1000)
# print (data.head(5))


# In[58]:

def get_lor(row):
    LORgroup = row['lor_group']
    duration = LORgroup.split(':')[1].split('-')
    start = int(duration[0])
    if len(duration) > 1:
        end = int(duration[1])
    else:
        end = start
    return randint(start, end)

data['lor'] = data.apply(lambda row: get_lor(row), axis=1)


# In[59]:

def create_dropoff_date(row):
    start_date = row['pickup_date']
    date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    lor = row['lor']
    new_date = date + datetime.timedelta(days=lor)
    return new_date

def clean_pickup_date(row):
    start_date = row['pickup_date']
    date = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    new_date = date + datetime.timedelta(days=0)
    return new_date

data['dropoff_date'] = data.apply(lambda row: create_dropoff_date(row), axis=1)
data['pickup_date'] = data.apply(lambda row: clean_pickup_date(row), axis=1)
data = data.sort_values('pickup_date')
# data


# In[60]:


def is_edge_avis(row):
    if math.isnan(row['avis_price']):
        return False
    h = math.isnan(row['hertz_price'])
    n = math.isnan(row['national_price'])
    if h and n:
        return True
    if n:
        return row['avis_price'] < row['hertz_price']
    elif h:
        return row['avis_price'] < row['national_price']
    else:
        return row['avis_price'] < row['hertz_price'] and row['avis_price'] < row['national_price']

def is_edge_budget(row):
    if math.isnan(row['budget_price']):
        return False
    h = math.isnan(row['alamo_price'])
    n = math.isnan(row['enterprise_price'])
    if h and n:
        return True
    if n:
        return row['budget_price'] < row['alamo_price']
    elif h:
        return row['budget_price'] < row['enterprise_price']
    else:
        return row['budget_price'] < row['alamo_price'] and row['budget_price'] < row['enterprise_price']
                  
def is_edge_payless(row):
    if math.isnan(row['payless_price']):
        return False
    h = math.isnan(row['dollar_price'])
    n = math.isnan(row['thrifty_price'])
    if h and n:
        return True
    if n:
        return row['payless_price'] < row['dollar_price']
    elif h:
        return row['payless_price'] < row['thrifty_price']
    else:
        return row['payless_price'] < row['dollar_price'] and row['payless_price'] < row['thrifty_price']
                  
data['edge_avis'] = data.apply(lambda row: is_edge_avis(row), axis=1)
data['edge_budget'] = data.apply(lambda row: is_edge_budget(row), axis=1)
data['edge_payless'] = data.apply(lambda row: is_edge_payless(row), axis=1)
# data


# In[61]:

data2 = data[['pickup_date','dropoff_date','edge_avis', 'edge_budget', 'edge_payless']]
data2

output_avis = []
def generate_output_avis(row):
    obj = {}
    obj['id'] = str(row['pickup_date'])
    obj['name'] = ''
    obj['data'] = {'color':str(row['edge_avis'])}
    obj['children'] = [{'id':str(row['dropoff_date']), 'name': "", 'data': {}, 'children': []}]
    output_avis.append(obj)
data2.apply(lambda row: generate_output_avis(row), axis=1)
output_budget = []
def generate_output_budget(row):
    obj = {}
    obj['id'] = str(row['pickup_date'])
    obj['name'] = ''
    obj['data'] = {'color':str(row['edge_budget'])}
    obj['children'] = [{'id':str(row['dropoff_date']), 'name': "", 'data': {}, 'children': []}]
    output_budget.append(obj)
data2.apply(lambda row: generate_output_budget(row), axis=1)

output_payless = []
def generate_output_payless(row):
    obj = {}
    obj['id'] = str(row['pickup_date'])
    obj['name'] = ''
    obj['data'] = {'color':str(row['edge_payless'])}
    obj['children'] = [{'id':str(row['dropoff_date']), 'name': "", 'data': {}, 'children': []}]
    output_payless.append(obj)


data2.apply(lambda row: generate_output_payless(row), axis=1)

output = {'avis':output_avis, 'budget':output_budget, 'payless':output_payless}



def generate_graph(output):
    graph = {}
    graph_centralities = {}
    tot_in = 0
    tot_out = 0
    for obj in output:
        fr = obj['id']
        to = obj['children'][0]['id']
        if fr not in graph:
            graph[fr] = {'in':set(), 'out': set()}
        if to not in graph:
            graph[to] = {'in':set(), 'out': set()}
        graph[fr]['out'].add(to)
        graph[to]['in'].add(fr)
        tot_in += 1
        tot_out += 1
    for v in graph:
        if v not in graph_centralities:
            graph_centralities[v] = {'in_centrality':0, 'out_centrality':0}
        graph_centralities[v]['in_centrality'] = len(graph[v]['in']) / tot_in
        graph_centralities[v]['out_centrality'] = len(graph[v]['out']) / tot_out
    sorted_vertices = sorted(graph_centralities, key=lambda v: -1 * graph_centralities[v]['out_centrality'])
    for v in sorted_vertices:
        print('Vertex: ' + v + '\t' + str(graph_centralities[v]))
    # print(graph_centralities)

generate_graph(output_avis)
# with open('graph_data.json', 'w') as fp:
 #    json.dump(output, fp)
# print(output)


# In[ ]:



