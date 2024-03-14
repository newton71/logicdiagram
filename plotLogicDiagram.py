# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 13:01:29 2024

@author: rkpal
"""

import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

def plotLogic(summary_dict):
# plotting logic diagram with 3 layers: Resources -> Activity -> Output.
# Input: 2 sets of links in JSON format
# Output: Image of 3-partite graph

    p = summary_dict

    nodes_R = []
    nodes_A = []
    nodes_O = []

    # add nodes
    for i in range(len(p["Link1"])):
        nodes_R.append(p["Link1"][i]["Resource"])
        nodes_A.append(p["Link1"][i]["Activity"])
    
    for i in range(len(p["Link2"])):
        nodes_O.append(p["Link2"][i]["Output"])
    
    nodes_R = list(set(nodes_R))
    nodes_A = list(set(nodes_A))
    nodes_O = list(set(nodes_O))
    
    g = nx.Graph()    
    g.add_nodes_from(nodes_R, layer = 0)
    g.add_nodes_from(nodes_A, layer = 1)
    g.add_nodes_from(nodes_O, layer = 2)
    
    
    edges = []
    for i in range(len(p["Link1"])):
        item = []
        item.append(p["Link1"][i]['Resource'])
        item.append(p["Link1"][i]['Activity'])
        edges.append(tuple(item))
        
    for i in range(len(p["Link2"])):
        item = []
        item.append(p["Link2"][i]['Activity'])
        item.append(p["Link2"][i]['Output'])
        edges.append(tuple(item))
    
    g.add_edges_from(edges)
    
        
    mapping = {}
    for old_label in g.nodes():
        new_label = insert_char_after_every_n_words(old_label, '\n', 3)
        mapping[old_label] = new_label
        
    g = nx.relabel_nodes(g, mapping, copy=True)
    
    pos = nx.multipartite_layout(g, subset_key="layer")
    plt.figure(figsize=(10,8))
    nx.draw(g, pos, with_labels=True, node_size = 400, node_color="lightblue", font_weight="normal", font_size = 8.5, clip_on = False)
    #plt.show()

    # Save the figure to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    # Close the figure to prevent it from being displayed in the notebook/output
    plt.close()
    buffer.seek(0)
    return buffer




def insert_char_after_every_n_words(line, char, nword):
# program to split a long line into multiple lines for printing    
   
    # Split the line into words
    words = line.split()
    
    # Initialize an empty list to hold modified groups of words
    modified_line = []
    
    # Loop through the words in steps of 3
    for i in range(0, len(words), nword):
        # Extract the group of 3 words
        word_group = words[i:i+nword]
        
        # Join the group of words and append the character
        # Only add the character if it's not the last group or if the last group has 3 words
        if i + nword < len(words) or len(word_group) == nword:
            modified_line.append(' '.join(word_group) + char)
        else:
            modified_line.append(' '.join(word_group))
    
    # Join all the modified groups back into a single string
    return ' '.join(modified_line)    