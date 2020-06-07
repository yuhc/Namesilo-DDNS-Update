#!/usr/bin/env python

# Author: Kudoyafka @ github
# Date 2020/01/26
# Usage: DDNS updating for namesilo

import urllib3
import xmltodict
import requests

import time
import sys
import datetime
import configparser
import xml.etree.ElementTree as ET

# Update DNS in namesilo
def update(currentIP,recordID,targetDomain,targetIP):
        # Initial DNS update request
        updateDNSRecords_request="https://www.namesilo.com/api/dnsUpdateRecord?version=1&type=xml&key=" \
        + apiKey + "&domain=" + domain \
        +"&rrid=" + recordID
        if host != "":
            updateDNSRecords_request  += "&rrhost=" + host
        updateDNSRecords_request += "&rrhost=" + host \
        +"&rrvalue=" + currentIP  \
        + "&rrttl=7207"

        # Evaluate the response
        response = requests.get(updateDNSRecords_request)
        Element = ET.fromstring(response.content)

        for reply in Element.iter('reply'):
            detail = reply.find('detail').text
            if detail != "success":
                print("Error: " + detail)
                print("Exiting ... ")
                file = open("DDNS_Update.log", "a+")
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                file.writelines(timestamp + "\n")
                file.writelines("Error: " + detail + "\n\n")
                file.close()
                sys.exit()
            else:
                file = open("DDNS_Update.log", "a+")
                ts = time.time()
                timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                file.writelines(timestamp + "\n")
                file.writelines(targetDomain + "\n")
                file.writelines(targetIP + " Updated to -> " + currentIP + "\n\n")
                file.close()

#Check if the IP is changed, then perform update
def check():
    # Initial reqeust to namesilo
    dnsListRecords_request = "https://www.namesilo.com/api/dnsListRecords?version=1&type=xml&key="\
        + apiKey +  "&domain=" + domain
    # Get response from namesilo
    response = requests.get(dnsListRecords_request)
    Element = ET.fromstring(response.content)

    # Determine if the request is success
    for reply in Element.iter('reply'):
        detail = reply.find('detail').text
        if detail != "success":
            print("Error: " + detail)
            print("Exiting ... ")
            file = open("DDNS_Update.log", "a+")
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            file.writelines(timestamp + "\n")
            file.writelines("Error: " + detail + "\n\n")
            file.close()
            sys.exit()

    # Find local IP
    for request in Element.iter('request'):
        currentIP = request.find('ip').text
        break

    # Add host to target domain if found
    if host != "":
        targetDomain = host + "." + domain
    else:
        targetDomain = domain

    # Find record ID for updating usage
    found = 0
    for resource_record in Element.iter('resource_record'):
        temp_host = resource_record.find('host').text
        if temp_host == targetDomain:
            found = 1
            targetIP = resource_record.find('value').text
            recordID = resource_record.find('record_id').text

    if found == 0:
        print("Error:" + targetDomain + "not found.")
        print("Existing ... ")
        sys.exit()


    #Update it if the public IP is changed
    if currentIP != targetIP:
        update(currentIP, recordID,targetDomain,targetIP )
    else:
	file = open("DDNS_Update.log", "a+")
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        file.writelines(timestamp + "\n")
        file.writelines("Public IP have not changed.\n\n")
        file.close()

# Read Config File
conf = configparser.ConfigParser()
conf.read('config.ini', encoding="utf-8")
domain = conf.get('DEFAULT', 'domain')
host = conf.get('DEFAULT', 'host')
apiKey = conf.get('DEFAULT', 'api_key')
check_interval = conf.getint('DEFAULT', 'check_interval')
# Begin checking
while True:
    check()
    time.sleep(check_interval)
