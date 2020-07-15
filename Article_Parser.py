#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 18:22:34 2020

@author: xander
"""

import datetime, networkx as nx, os, xmltodict
os.path.join(os.path.dirname(__file__))

'''
with open ('Pubmed_Data_Download.sh','w') as file:
    file.write('#!/bin/bash' + '\n')
    file.write('#PBS -k o' + '\n')
    file.write('#PBS -l nodes=1:ppn=16,walltime=4:00:00,vmem=50gb' + '\n')
    file.write('#PBS -M ' + '\n')
    file.write('#PBS -m e' + '\n')
    file.write('#PBS -Pubmed_Data_Download' + '\n')
    file.write('#PBS -j oe' + '\n')
    file.write('\ncd /N/dc2/projects/MAMMALEXP/Deep_Learn/PubMed/' + '\n')
    for i in range (1015):
        index = str(0)*(4 - len(str(i + 1))) + str(i + 1)
        file.write('wget ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed20n' + index + '.xml.gz' + '\n')
        file.write('gunzip pubmed20n*.gz')
    file.close()
'''

os.chdir('/home/xander/Deep_Learn')
file_List = os.listdir('./')
month_Lengths = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
art_Data = {}
for i in file_List:
    with open(i, encoding = 'utf-8') as file:
        file_Dict = xmltodict.parse(file.read())
        file.close()
    for j in file_Dict.keys():
        for k in file_Dict[j].keys():
            for l in range(len(file_Dict[j][k])):
                art_Id = ''
                pub_Date = ''
                auth_Dept = ''
                auth_School = ''
                art_Abst = ''
                art_Refs = []
                for m in file_Dict[j][k][l].keys():
                    if ('History' in file_Dict[j][k][l][m].keys()):
                        if ('PubMedPubDate' in file_Dict[j][k][l][m]['History'].keys()):
                            if (type(file_Dict[j][k][l][m]['History']['PubMedPubDate']) == list):
                                if ('Year' in file_Dict[j][k][l][m]['History']['PubMedPubDate'][0].keys()):
                                    pub_Year = int(file_Dict[j][k][l][m]['History']['PubMedPubDate'][0]['Year'])
                                    if ('Month'in file_Dict[j][k][l][m]['History']['PubMedPubDate'][0].keys()):
                                        pub_Month = int(file_Dict[j][k][l][m]['History']['PubMedPubDate'][0]['Month'])
                                        if ('Day' in file_Dict[j][k][l][m]['History']['PubMedPubDate'][0].keys()):
                                            pub_Day = int(file_Dict[j][k][l][m]['History']['PubMedPubDate'][0]['Day'])
                                            if (pub_Day > month_Lengths[pub_Month]):
                                                pub_Day = month_Lengths[pub_Month]
                                        else:
                                            pub_Day = 1
                                        pub_Date = datetime.date(pub_Year, pub_Month, pub_Day)
                            elif (type(file_Dict[j][k][l][m]['History']['PubMedPubDate']) == type(file_Dict)):
                                if ('Year' in file_Dict[j][k][l][m]['History']['PubMedPubDate'].keys()):
                                    pub_Year = int(file_Dict[j][k][l][m]['History']['PubMedPubDate']['Year'])
                                    if ('Month'in file_Dict[j][k][l][m]['History']['PubMedPubDate'].keys()):
                                        pub_Month = int(file_Dict[j][k][l][m]['History']['PubMedPubDate']['Month'])
                                        if ('Day' in file_Dict[j][k][l][m]['History']['PubMedPubDate'].keys()):
                                            pub_Day = int(file_Dict[j][k][l][m]['History']['PubMedPubDate']['Day'])
                                            if (int(pub_Day) > month_Lengths[pub_Month]):
                                                pub_Day = month_Lengths[pub_Month]
                                        else:
                                            pub_Day = 1
                                        pub_Date = datetime.date(pub_Year, pub_Month, pub_Day)
                    if ('Article' in file_Dict[j][k][l][m].keys()):
                        if ('Abstract' in file_Dict[j][k][l][m]['Article'].keys()):
                            if ('AbstractText' in file_Dict[j][k][l][m]['Article']['Abstract'].keys()):
                                if (type(file_Dict[j][k][l][m]['Article']['Abstract']['AbstractText']) == str):
                                    art_Abst = file_Dict[j][k][l][m]['Article']['Abstract']['AbstractText']
                                elif (type(file_Dict[j][k][l][m]['Article']['Abstract']['AbstractText']) == list):
                                    for n in file_Dict[j][k][l][m]['Article']['Abstract']['AbstractText']:
                                        if (type(n) == type(file_Dict)):
                                            if ('#text' in n.keys()):
                                                art_Abst += n['#text']
                                elif (type(file_Dict[j][k][l][m]['Article']['Abstract']['AbstractText']) == type(file_Dict)):
                                    if ('#text' in file_Dict[j][k][l][m]['Article']['Abstract']['AbstractText'].keys()):
                                        art_Abst = file_Dict[j][k][l][m]['Article']['Abstract']['AbstractText']['#text']
                        if ('AuthorList' in file_Dict[j][k][l][m]['Article'].keys()):
                            if ('Author' in file_Dict[j][k][l][m]['Article']['AuthorList']):
                                if (type(file_Dict[j][k][l][m]['Article']['AuthorList']['Author']) == list):
                                    if (type(file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0]) == type(file_Dict)):
                                        if ('AffiliationInfo' in file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0].keys()):
                                            if (type(file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0]['AffiliationInfo']) == type(file_Dict)):
                                                if ('Affiliation' in file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0]['AffiliationInfo'].keys()):
                                                    auth_Info = file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0]['AffiliationInfo']['Affiliation']
                                                    if (type(auth_Info) == list):
                                                        auth_Info = auth_Info[0]
                                                    if (type(auth_Info) == str):
                                                        auth_Info = auth_Info.split(',')
                                                        if (len(auth_Info) > 1):
                                                            auth_Dept = auth_Info[0]
                                                            auth_School = auth_Info[1]
                                                        else:
                                                            auth_School = auth_Info[0]
                                            elif (type(file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0]['AffiliationInfo']) == list):
                                                if ('Affiliation' in file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0]['AffiliationInfo'][0].keys()):
                                                    auth_Info = file_Dict[j][k][l][m]['Article']['AuthorList']['Author'][0]['AffiliationInfo'][0]['Affiliation']
                                                    if (type(auth_Info) == list):
                                                        auth_Info = auth_Info[0]
                                                    if (type(auth_Info) == str):
                                                        auth_Info = auth_Info.split(',')
                                                        if (len(auth_Info) > 1):
                                                            auth_Dept = auth_Info[0]
                                                            auth_School = auth_Info[1]
                                                        else:
                                                            auth_School = auth_Info[0] 
                    if ('ArticleIdList' in file_Dict[j][k][l][m].keys()):
                        if (type(file_Dict[j][k][l][m]['ArticleIdList']['ArticleId']) == list):
                            art_Id = file_Dict[j][k][l][m]['ArticleIdList']['ArticleId'][0]['#text']
                        else:
                            art_Id = file_Dict[j][k][l][m]['ArticleIdList']['ArticleId']['#text']
                    if ('ReferenceList' in file_Dict[j][k][l][m].keys()):
                        if (type(file_Dict[j][k][l][m]['ReferenceList']) == list):
                            for n in range(len(file_Dict[j][k][l][m]['ReferenceList'])):
                                if ('ArticleIdList' in file_Dict[j][k][l][m]['ReferenceList'][n].keys()):
                                    art_Refs.append(file_Dict[j][k][l][m]['ReferenceList'][n]['ArticleIdList']['ArticleId']['#text'])
                                elif ('Reference' in file_Dict[j][k][l][m]['ReferenceList'][n].keys()):
                                    art_Refs.append(file_Dict[j][k][l][m]['ReferenceList'][n]['Reference']['ArticleIdList']['ArticleId']['#text'])
                        else:
                            if (type(file_Dict[j][k][l][m]['ReferenceList']['Reference']) == list):
                                for n in range(len(file_Dict[j][k][l][m]['ReferenceList']['Reference'])):
                                    art_Refs.append(file_Dict[j][k][l][m]['ReferenceList']['Reference'][n]['ArticleIdList']['ArticleId']['#text'])
                            else:
                                art_Refs.append(file_Dict[j][k][l][m]['ReferenceList']['Reference']['ArticleIdList']['ArticleId']['#text'])
                art_Data[art_Id] = [pub_Date,art_Abst,art_Refs,auth_Dept,auth_School]

art_Net = nx.DiGraph()
max_Time = datetime.timedelta(days = 180)
for i in art_Data.keys():
    art_Refs = art_Data[i][2]
    for j in art_Refs:
        if (j in art_Data.keys()):
            if (art_Data[i][0] != '') and (art_Data[j][0] != ''):
                if ((art_Data[i][0] - art_Data[j][0]) < max_Time):
                    art_Net.add_edge(i, j)

art_Nodes = art_Net.nodes()
for i in art_Nodes:
    art_Data[i].append(art_Net.in_degree(i))

for i in list(art_Data.keys()):
    if (len(art_Data[i]) < 6):
        art_Data.pop(i, None)

with open ('Article_Data.txt', 'w') as file:
    file.write('Article ID' + '\t' + 'Article Abstract' + '\t' + 'Author Department' + '\t' + 'Author School' + '\t' + 'Impact Factor' + '\n')
    for i in art_Data.keys():
        art_Data[i][1] = art_Data[i][1].encode('ascii', 'ignore').decode('ascii')
        art_Data[i][3] = art_Data[i][3].encode('ascii', 'ignore').decode('ascii')
        art_Data[i][4] = art_Data[i][4].encode('ascii', 'ignore').decode('ascii')
        file.write(str(i) + '\t' + art_Data[i][1] + '\t' + art_Data[i][3] + '\t' + art_Data[i][4] + '\t' + str(art_Data[i][5]) + '\n')
    file.close()
