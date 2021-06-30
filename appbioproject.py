import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

import networkx as nx

network_data_frame = pd.read_csv('9606.protein.links.v11.0.txt.gz', sep=' ', dtype = str, header = 0)
network_data_frame.loc[:,'protein1'] = [re.sub("9606.", "", x) for x in network_data_frame.loc[:,"protein1"]]
network_data_frame.loc[:,'protein2'] = [re.sub("9606.", "", x) for x in network_data_frame.loc[:,"protein2"]]

#make the whole network
network = nx.from_pandas_edgelist(network_data_frame, source = 'protein1', target = 'protein2')

#subset only the interactions
network_subsetted_df = network_data_frame[network_data_frame['combined_score'].astype(int) >= 500]

#create network object with only significant weighted interactions
network_subsetted = nx.from_pandas_edgelist(network_subsetted_df, source = 'protein1', target = 'protein2')

highdegree = [n for n,d in network_subsetted.degree if d > 100]
lowdegree = [n for n,d in network_subsetted.degree if d <= 100]

#load dataset with pfam ids
pfams = pd.read_csv('proteins_w_domains.txt', sep='\t').dropna()

#make degree label column
hd_df = pfams.loc[pfams.loc[:,'Protein stable ID'].isin(highdegree),:]
ld_df = pfams.loc[pfams.loc[:,'Protein stable ID'].isin(lowdegree),:]

hd_df.loc[:,'Degree'] = 'High'
ld_df.loc[:,'Degree'] = 'Low'

final = pd.concat([hd_df,ld_df], axis=0)

plot = final.groupby(['Degree', 'Pfam ID'])['Protein stable ID'].count().to_frame(name = "Protein stable IDs").reset_index()

sns.barplot(x = "Degree", y = "Protein stable IDs", data = plot)
plt.savefig('barplot_appbio.png', dpi=300, bbox_inches='tight')
