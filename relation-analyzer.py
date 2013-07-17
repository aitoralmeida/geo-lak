# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 12:53:42 2013

@author: aitor
"""

import csv
import networkx as nx
from networkx.readwrite import gexf
import urllib2
import json
from networkx.readwrite import json_graph

papers = {}

def slug_me(s):
    result = s.replace(' ', '-')
    result = result.replace('.', '')
    return result

def unslug_me(s):
    result = s.replace('-', ' ')
    return result

def un_urify(s):
    return s.split('/')[-1]

def prettify_organization(s):
    return s.replace('-', ' ')

#deprecated
def create_coauthorship():
    with open('./data/coauthorship.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            if not row[1] in papers.keys():
                papers[row[1]] = []
            papers[row[1]].append(slug_me(row[0]))
    
    
    
    relations = []
    
    for paper in papers:
        authors = papers[paper]
        for i in range(0, len(authors)):
            for j in range(i, len(authors)):
                if authors[i] != authors[j]:
                    relations.append([authors[i], authors[j]])
                    
    print relations
    
    with open('./data/coauthorship-edgelist.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        for relation in relations:
            writer.writerow(relation)  
            
def create_nodes():
    G = nx.Graph()
    with open('./data/peopleClean.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            person = slug_me(row[1])
            G.add_node(person)
            G.node[person]["name"] = row[1]
            G.node[person]["location"] = un_urify(row[2])
            G.node[person]["affiliation"] = un_urify(row[3])
            G.node[person]['clique-size'] = -1
    return G
    
def create_edges(G):
    papers = {}
    with open('./data/authorshipClean.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            paper_id = row[3]
            author = slug_me(row[2])
            if not paper_id in papers.keys():
                papers[paper_id] = []
            papers[paper_id].append(author)
            
        
    for paper in papers:
        authors = papers[paper]
        for i in range(0, len(authors)):
            for j in range(i, len(authors)):
                if authors[i] != authors[j]:
                    G.add_edge(authors[i], authors[j])
                    
    return G
    
def analyze_graph(G):
    betweenness = nx.betweenness_centrality(G)
    eigenvector = nx.eigenvector_centrality_numpy(G)
    closeness = nx.closeness_centrality(G)
    pagerank = nx.pagerank(G)
    degrees = G.degree()

    for name in G.nodes():
        G.node[name]['betweenness'] = betweenness[name]
        G.node[name]['eigenvector'] = eigenvector[name]
        G.node[name]['closeness'] = closeness[name]
        G.node[name]['pagerank'] = pagerank[name]
        G.node[name]['degree'] = degrees[name]
        
    components = nx.connected_component_subgraphs(G)
    i = 0    
    for cc in components:            
        #Set the connected component for each group
        for node in cc:
            G.node[node]['component'] = i
        i += 1
        
        cent_betweenness = nx.betweenness_centrality(cc)              
        cent_eigenvector = nx.eigenvector_centrality_numpy(cc)
        cent_closeness = nx.closeness_centrality(cc)
        
        for name in cc.nodes():
            G.node[name]['cc-betweenness'] = cent_betweenness[name]
            G.node[name]['cc-eigenvector'] = cent_eigenvector[name]
            G.node[name]['cc-closeness'] = cent_closeness[name]
    
    #Assign each person to his bigger clique    
    cliques = list(nx.find_cliques(G))
    j = 0
    for clique in cliques:
        clique_size = len(clique)
        for member in clique:
            if G.node[member]['clique-size'] < clique_size:
                G.node[member]['clique-size'] = clique_size
                G.node[member]['clique'] = j
        j +=1
    
    
    return G
    
def get_coords(organization, country):
    start = 'http://nominatim.openstreetmap.org/search?q='
    end = '&format=json&polygon=1&addressdetails=1'
    organization = organization.replace('-', '+')
    country = country.replace('_', '+')
    url_add = start + organization + ',+' + country + end
    print url_add
    req = urllib2.Request(url_add)
    response = urllib2.urlopen(req)
    result = response.read()     
    if result == '[]':
        url_add = start + country + end
        req = urllib2.Request(url_add)
        response = urllib2.urlopen(req)
        result = response.read()  
    data = json.loads(result)
    res = []
    if len(data) < 1:
        res = []
    else:
        res = [data[0]['lat'], data[0]['lon']]
    return res
    
def get_geo_data(G):
    i = 0
    for node in G.nodes():
        print 'Node %i: %s' %(i, node)
        i += 1
        organization = G.node[node]['affiliation']
        country = G.node[node]['location']
        coords = get_coords(organization, country)
        if len(coords) == 2:
            G.node[node]['lat'] = coords[0]
            G.node[node]['lon'] = coords[1]
    return G


def load_graph(filepath):
    return gexf.read_gexf(filepath)
    
def export_json(G):
    data = json_graph.node_link_data(G)
    json.dump(data, open('./data/lak-coauthor.json', 'w'))
    
        
def save_graph(G):
    gexf.write_gexf(G, './data/lak-coauthor.gexf')
            

if __name__ == '__main__':
    G = create_nodes()
    G = create_edges(G)
    G = analyze_graph(G)
    G = get_geo_data(G)    
    save_graph(G)
    print 'fin'


    


            
            
    
#req = urllib2.Request('http://nominatim.openstreetmap.org/search?q=university+of+leeds,+uk&format=json&polygon=1&addressdetails=1')
#response = urllib2.urlopen(req)
#the_page = response.read()            
#            

        
    