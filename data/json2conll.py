#!/usr/bin/python3

import sys
import argparse
import json
import copy

parser = argparse.ArgumentParser(description = 'Process a conll eval files to give Concept Error Rate.')
parser.add_argument('-i','--input', metavar = 'input', type = str, help = 'input file (json)', required = True)
parser.add_argument('-o','--output', metavar = 'output', type = str, help = 'output file (conll)', required = True)
#parser.add_argument('-l','--labels', type = str, help = 'table to indicate the field id of POS, entities and relations in the input file. (e.g.:default for conll2003 is 1,3,0)', required = True)

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
#print(ids)
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

def process_entities(jsondata):
    tab_entities = ["O"]*len(jsondata["tokens"])
    for entities in jsondata["pre_entities"]:
        for inc in range(entities["start"]+1,entities["end"]):
            tab_entities[inc] = "I-" + entities["type"]
        tab_entities[entities["start"]] = "B-" + entities["type"]
    return tab_entities


tab_tokens = []
tab_postag = []
tab_relations = []
tab_entities = []

org_id = 0
for line_src in fichier_src:
    datajson = json.loads(line_src.strip())
    cpt_line = 0
    for line in datajson:
        cpt_line = cpt_line + 1
        tab_entities = process_entities(line)
        tab_tokens = line["tokens"]
        if len(tab_tokens) != len(tab_entities):
            print("Length error line:", cpt_line)
            sys.exit(1)
        for inc in range(len(tab_tokens)):
            fichier_out.write(tab_tokens[inc]+" "+tab_entities[inc])
            fichier_out.write("\n")
        fichier_out.write("\n")

fichier_out.write("\n")
fichier_out.close()
fichier_src.close()
