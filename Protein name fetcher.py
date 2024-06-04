#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:02:21 2024

@author: aliamiryousefi
"""

#change the ready and writing directory

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load your CSV file
df = pd.read_csv('path_to_your_file/SMN.csv')

# Add columns for each of the databases
databases = ['GeneCards', 'UniProt', 'NCBI_Gene', 'HGNC', 'Human_Protein_Atlas']
for db in databases:
    df[db] = ""

def get_synonyms(marker):
    synonyms = {db: "" for db in databases}

    # GeneCards
    gc_url = f"https://www.genecards.org/cgi-bin/carddisp.pl?gene={marker}"
    gc_response = requests.get(gc_url)
    if gc_response.status_code == 200:
        gc_soup = BeautifulSoup(gc_response.content, 'html.parser')
        synonyms_section = gc_soup.find('section', {'class': 'synonyms'})
        if synonyms_section:
            synonyms['GeneCards'] = " / ".join([syn.text for syn in synonyms_section.find_all('span')])
    
    # UniProt
    up_url = f"https://www.uniprot.org/uniprot/?query={marker}&sort=score"
    up_response = requests.get(up_url)
    if up_response.status_code == 200:
        up_soup = BeautifulSoup(up_response.content, 'html.parser')
        up_results = up_soup.find('div', {'id': 'results'})
        if up_results:
            synonyms['UniProt'] = " / ".join([res.text for res in up_results.find_all('a', {'class': 'entry-overview'})])

    # NCBI Gene
    ncbi_url = f"https://www.ncbi.nlm.nih.gov/gene/?term={marker}"
    ncbi_response = requests.get(ncbi_url)
    if ncbi_response.status_code == 200:
        ncbi_soup = BeautifulSoup(ncbi_response.content, 'html.parser')
        ncbi_synonyms = ncbi_soup.find('dd', {'class': 'noline'})
        if ncbi_synonyms:
            synonyms['NCBI_Gene'] = ncbi_synonyms.text.strip()
    
    # HGNC
    hgnc_url = f"https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/{marker}"
    hgnc_response = requests.get(hgnc_url)
    if hgnc_response.status_code == 200:
        hgnc_soup = BeautifulSoup(hgnc_response.content, 'html.parser')
        hgnc_synonyms = hgnc_soup.find('div', {'class': 'panel-body'})
        if hgnc_synonyms:
            synonyms['HGNC'] = " / ".join([syn.text for syn in hgnc_synonyms.find_all('li')])

    # Human Protein Atlas
    hpa_url = f"https://www.proteinatlas.org/search/{marker}"
    hpa_response = requests.get(hpa_url)
    if hpa_response.status_code == 200:
        hpa_soup = BeautifulSoup(hpa_response.content, 'html.parser')
        hpa_synonyms = hpa_soup.find('div', {'class': 'content'})
        if hpa_synonyms:
            synonyms['Human_Protein_Atlas'] = " / ".join([syn.text for syn in hpa_synonyms.find_all('span', {'class': 'label'})])

    return synonyms

# Fetch synonyms for each marker
total_markers = len(df)
for index, row in df.iterrows():
    marker = row['Standardized Marker Name']
    synonyms = get_synonyms(marker)
    for db in databases:
        df.at[index, db] = synonyms[db]
    # Display progress
    if (index + 1) % 10 == 0 or index + 1 == total_markers:
        print(f"Progress: {((index + 1) / total_markers) * 100:.2f}%")

# Save the updated DataFrame
df.to_csv('path_to_save/Updated_Markers_Synonyms.csv', index=False)
