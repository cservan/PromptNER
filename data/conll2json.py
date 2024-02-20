#!/usr/bin/python3

import sys
import argparse
import json
import copy

parser = argparse.ArgumentParser(description = 'Process a conll eval files to give Concept Error Rate.')
parser.add_argument('--input', metavar = 'input', type = str, help = 'input file', required = True)
parser.add_argument('--output', metavar = 'output', type = str, help = 'output file', required = True)
parser.add_argument('--labels', type = str, help = 'table to indicate the fiel id of POS, entities and relations in the input file. (e.g.:default for conll2003 is 1,3,0)', required = True)

args = parser.parse_args()

#fichier_tgt = open(args.tgt, "r")
fichier_src = open(args.input, "r")
fichier_out = open(args.output, "w")

line_concat_pos_print = ""
line_concat_hyp_print = ""
line_concat_pos = ""
line_concat_src = ""
taghypprev = ""
postagprev = ""
tagroot = ""
tagrootprev = ""
cptCER = 0
sumCER = 0.0
tagtoclose = False
line_id = 0
ids = [int(x) for x in list(args.labels.split(","))]
print(ids)
whole_data_to_write = []


def process_entities(tab):
    prev_ent = ""
    datas = {"start":0,"end":0,"type":""}
    to_return = []
    for inc in range(len(tab)):
        if tab[inc][0] == "B" or tab[inc][0] == "O" :
            if datas["type"] != "":
                datas["end"] = inc
                to_return.append(copy.deepcopy(datas))
                datas = {"start":0,"end":0,"type":""}
            if tab[inc][0] == "B" :
                datas["type"] = tab[inc][2:]
                datas["start"] = inc
    if datas["type"] != "":
        datas["end"] = len(tab)
        to_return.append(copy.deepcopy(datas))
    return to_return



tab_tokens = []
tab_postag = []
tab_relations = []
tab_entities = []

org_id = 0
for line_src in fichier_src:
    line_src_tab = line_src.strip().split(" ")
    #print (line_src_tab)
    concatref = True
    concathyp = True
    tagtoclose = False
    if len(line_src_tab) > 1:
        word = line_src_tab[0].strip()
        if word ==  "-DOCSTART-":
            org_id = org_id + 1
        else:
            if ids[0] != 0:
                postag = line_src_tab[ids[0]].strip()
                #line_concat_pos = line_concat_pos+postag+" "
                tab_postag.append(postag)
            if ids[1] != 0:
                entity = line_src_tab[ids[1]].strip()
                #line_concat_pos = line_concat_pos+postag+" "
                tab_entities.append(entity)
            if ids[2] != 0:
                relation = line_src_tab[ids[2]].strip()
                #line_concat_pos = line_concat_pos+postag+" "
                tab_relations.append(relation)
            #line_concat_src = line_concat_src+word+" "
            tab_tokens.append(word)
    else:
        line_id = line_id+1
        taghypprev = ""
        postagprev = ""
        data_to_write = {}
        #tab_tokens = line_concat_src.strip().split(" ")
        #tab_postag = line_concat_pos.strip().split(" ")
        #tab_relations = line_concat_relations.strip().split(" ")
        #tab_entities = line_concat_entities.strip().split(" ")
        if len(tab_tokens) > 0:
            if len(tab_tokens[0]) > 0:
                data_to_write["org_id"] = str(org_id)
                data_to_write["tokens"] = tab_tokens
                data_to_write["pos"] = tab_postag
                data_to_write["relations"] = tab_relations
                data_to_write["entities"] = process_entities(tab_entities)
                whole_data_to_write.append(copy.deepcopy(data_to_write))
        #line_concat_pos = ""
        #line_concat_src = ""
        tab_tokens = []
        tab_postag = []
        tab_relations = []
        tab_entities = []

fichier_out.write(json.dumps(whole_data_to_write,ensure_ascii = False))
fichier_out.write("\n")
fichier_out.close()
fichier_src.close()
