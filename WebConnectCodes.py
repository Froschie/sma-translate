#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import argparse
import sys

# Command Line Arguments
parser=argparse.ArgumentParser(
    description='''Script for Translating SMA WebConnect Codes to selectable language.''')
parser.add_argument('--sma_ip', type=str, required=True, default="", help='IP of the SMA Device.')
parser.add_argument('--sma_pw', type=str, required=True, default="", help='Password of the SMA Device.')
parser.add_argument('--nossl', type=bool, required=False, default=False, help='Connection without via SSL?')
parser.add_argument('--csv', type=bool, required=False, default=False, help='Output on terminal or write CSV file?')
parser.add_argument('--lang', type=str, required=False, default="de", choices=["en", "de", "cs", "el", "es", "fr", "it", "ja", "ko", "nl", "pl", "pt", "th"], help='Language selection.')
parser.add_argument('--live', type=str, required=False, default="yes", choices=["yes", "no"], help='Adding Live Data from SMA Inverter?')
parser.add_argument('--onlylive', type=str, required=False, default="no", choices=["yes", "no"], help='Show only live data?')
args=parser.parse_args()

# Language to file mapping.
languages = {"en": "en-US.json", "de": "de-DE.json", "cs": "cs-CS.json", "el": "el-EL.json", "es": "es-ES.json", "fr": "fr-FR.json", "it": "it-IT.json", "ja": "ja-JP.json", "ko": "ko-KR.json", "nl": "nl-NL.json", "pl": "pl-PL.json", "pt": "pt-PT.json", "th": "th-TH.json"}
lang_file = languages[args.lang]

# SSL or unencrypted communication
if args.nossl:
    base_url = "http://" + args.sma_ip
else:
    base_url = "https://" + args.sma_ip

# Download of Language File
url = base_url + "/data/l10n/" + lang_file
response = requests.request("GET", url, verify=False)
descriptions = response.json()

# Download if Object / Code List
url = base_url + "/data/ObjectMetadata_Istl.json"
response = requests.request("GET", url, verify=False)
objects = response.json()

# Tab Print Function
sma_array = []
headers = []
def tab_print(data, headers, summary=False):
    tab_len = []
    for item in headers:
        tab_len.append(len(item))
    for values in data:
        for i, item in enumerate(values):
            if i < len(tab_len):
                if len(str(item)) > tab_len[i]:
                    tab_len[i] = len(str(item))
    header_line = ""
    for i, item in enumerate(headers):
        if tab_len[i] > 0:
            header_line = header_line + '{:{width}}'.format(item, width=tab_len[i]) + "  "
    print(header_line)
    delimiter_line = ""
    for i, lenght in enumerate(tab_len):
        if tab_len[i] > 0:
            delimiter_line = delimiter_line + "".ljust(int(lenght), '-') + "  "
    print(delimiter_line)
    for i, values in enumerate(data):
        line = ""
        for j, item in enumerate(values):
            if j < len(tab_len):
                if type(item) == int:
                    line = line + str(item).rjust(tab_len[j], ' ') + "  "
                else:
                    line = line + str(item).ljust(tab_len[j], ' ') + "  "
        if i == len(data)-1 and summary == True:
            print(delimiter_line)
        print(line)

# Function for Translating single IDs
def translate(id):
    global descriptions
    if type(id) == list:
        text = ""
        for no in id:
            text = text + " " + translate(no)
        return text.strip()
    if str(id) in descriptions:
        return descriptions[str(id)]
    else:
        return "-----"

# Function for either printing or CSV writing information
temp_output = []
temp_csv = ""
def pr_output(text, nl=True):
    global args
    global file_data
    global temp_output
    global temp_csv
    if args.csv:
        if nl:
            if text != "":
                file_data += temp_csv + "\"" + text + "\"\n"
                temp_csv = ""
            else:
                file_data += temp_csv + "\n"
                temp_csv = ""
        else:
            temp_csv += "\"" + text + "\";"
    else:
        if len(text) > 45:
            text = text[:42] + "..."
        if nl:
            temp_output.append(text)
            sma_array.append(temp_output)
            temp_output = []
        else:
            temp_output.append(text)
    return None

# Listing all Headlines
object_list_all = []
if not args.csv:
    object_list_all.append("TagId")
else:
    for item in objects:
        for i in objects[item]:
            if i not in object_list_all:
                object_list_all.append(i)

# Defining which items should be translated via Language File
object_list_translate = ['TagId', 'TagIdEvtMsg', 'Unit', 'TagHier']

# Generating CSV Headline and Metadata
file_data = "sep=;\n"
headers.append("ID")
file_data += "\"ID\""
for x in object_list_all:
    headers.append(x)
    file_data += ";\"" + x + "\""
if args.live == "yes":
    headers.append("Query Value")
    file_data += ";\"Query Value\""
    headers.append("Query Result")
    file_data += ";\"Query Result\""
file_data += "\n"

# Querying SMA Inverter Live Data
live_data = {}
if args.live == "yes":
    # Login to SMA Inverter
    url = base_url + "/dyn/login.json"
    payload = "{\"right\":\"usr\",\"pass\":\"" + args.sma_pw + "\"}"
    response = requests.request("POST", url, data = payload, verify=False)
    if "result" in response.json():
        if "sid" in response.json()['result']:
            sid = response.json()['result']['sid']

    # Preparing list of all codes to be queried
    keys = ""
    for item in objects:
        if keys == "":
            keys = "\"" + item + "\""
        else:
            keys = keys + ",\"" + item + "\""

    # Query live data from SMA Inverter
    url = base_url + "/dyn/getValues.json?sid=" + sid
    payload = "{\"destDev\":[],\"keys\":[" + keys + "]})"
    response = requests.request("POST", url, data = payload, verify=False)
    if "result" in response.json():
        for id in response.json()['result']:
            sma_id = id
        try:
            live_data = response.json()['result'][id]
        except:
            live_data = {}

    # Logout from SMA Inverter
    url = base_url + "/dyn/logout.json?sid=" + sid
    payload = "{}"
    response = requests.request("POST", url, data = payload, verify=False)

for item in objects:
    # Translation of Codes
    pr_output(item, nl=False)
    # Adding translated fields
    for x in object_list_all:
        if x in objects[item]:
            if x in object_list_translate:
                pr_output(str(translate(objects[item][x])), nl=False)
            else:
                pr_output(str(objects[item][x]), nl=False)
        else:
            pr_output("", nl=False)
    # Adding Live Data from SMA Inverter
    if args.live == "yes":
        query_value = ""
        query_result = ""
        if str(item) in live_data:
            if len(live_data[str(item)]) == 1:
                for no in live_data[str(item)]:
                    if len(live_data[str(item)][str(no)]) == 1:
                        if "val" in live_data[str(item)][str(no)][0]:
                            if live_data[str(item)][str(no)][0]['val'] == None or type(live_data[str(item)][str(no)][0]['val']) == int:
                                query_value = str(live_data[str(item)][str(no)][0]['val'])
                                query_result = str(live_data[str(item)][str(no)])
                            else:
                                if type(live_data[str(item)][str(no)][0]['val']) == str:
                                    query_value = str(live_data[str(item)][str(no)][0]['val'])
                                    query_result = str(live_data[str(item)][str(no)])
                                else:
                                    if len(live_data[str(item)][str(no)][0]['val']) == 1:
                                        if "tag" in live_data[str(item)][str(no)][0]['val'][0]:
                                            query_value = translate(live_data[str(item)][str(no)][0]['val'][0]['tag'])
                                            query_result = str(live_data[str(item)][str(no)])
                                        else:
                                            query_value = str(live_data[str(item)][str(no)][0]['val'])
                                            query_result = str(live_data[str(item)][str(no)])
                                    else:
                                        query_result = str(live_data[str(item)][str(no)])
                        else:
                            query_result = str(live_data[str(item)][str(no)])
                    else:
                        query_result = str(live_data[str(item)][str(no)])
            else:
                query_result = str(live_data[str(item)])
        pr_output(query_value, nl=False)
        if len(query_result) > 30 and not args.csv:
            query_result = query_result[:27] + "..."
        pr_output(query_result, nl=False)
    if args.onlylive == "yes":
        if query_result == "":
            temp_output = []
            temp_csv = ""
        else:
            pr_output("")
    else:
        pr_output("")

# Check if CSV Mode is active
if args.csv:
    # Write CSV file
    f = open("WebConnectCodes.csv", "w", encoding='utf8')
    f.write(file_data)
    f.close()
else:
    # Print Text in case CSV Mode is not used
    tab_print(sma_array, headers, False)
