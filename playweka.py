#!/usr/bin/env python
'''
playweka.py
Copyright (C) 2015 Thomas Valadez (@tvldz)
License: MIT
Requires: googleplay-api (https://github.com/egirault/googleplay-api)

This script searches the Google Play Store with a given query,
enumerates all of the "ANDROID." permissions for each app, and 
creates an ARFF file for Weka machine learning applications. It
also prints out an index, correlating each application with the 
integer the app is represented by within the file output.

Usage:
python playweka.py <search term>
'''

import os
import sys
from googleplay import GooglePlayAPI
from config import *
import string
import traceback
from helpers import sizeof_fmt, print_header_line, print_result_line
from sets import Set

def main():
    search_term = sys.argv[1]
    '''
    apps will be a list of dicts describing each returned app:
    {'app_name':<app name>,'app_id':<app id>,'app_creator':<creator>,'app_permissions':[list]}
    '''
    apps = []
    nb_res = 100 # apps to retrieve. API allows for max of 100.
    offset = 0 
    api = GooglePlayAPI(ANDROID_ID)
    api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
    try:
        message = api.search(search_term, nb_res, offset)
    except:
        print "Error: something went wrong. Google may be throttling or rejecting the request."
        sys.exit(1)

    doc = message.doc[0]
    for c in doc.child:
        permissions = []
        details = api.details(c.docid)
        for line in details.docV2.details.appDetails.permission:
            permissions.append(line)
        apps.append({'app_name':c.title,'app_id':c.docid,'app_creator':c.creator,'app_permissions':permissions})

    '''
    We are interested in the set of all possible permissions that start with 'ANDROID.'
    '''
    permissions = Set([])
    for app in apps:
        for permission in app["app_permissions"]:
            if  permission.upper()[0:8] == "ANDROID.":
                permissions.add(permission.upper())

    '''
    Create ARFF output for Weka
    '''
    dataset = open(search_term + ".arff",'w')
    dataset.write("@relation Appdata\n")
    dataset.write("@attribute index NUMERIC\n")
    dataset.write("@attribute app_name STRING\n")
    for att in permissions:
        dataset.write("@attribute "+ att + " {0,1}\n")
    dataset.write("@data\n")
    i = 0 # index for cross-referencing
    for app in apps:
        print("{} {}").format(str(i), str(app)) # index
        perm_str = str(i) + ',' + app['app_id'] + ','
        app_perm_upper = []
        for app_permission in app['app_permissions']:
            app_perm_upper.append(app_permission.upper())
        for permission in permissions:
            if permission in app_perm_upper:
                perm_str = perm_str + '1,'
            else:
                perm_str = perm_str + '0,'
        dataset.write(perm_str[:-1])
        dataset.write("\n")
        i += 1

if __name__ == '__main__':
    sys.exit(main())
