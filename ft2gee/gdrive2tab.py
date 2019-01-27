#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
from oauth2client.tools import argparser
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools
import ee
import os
import re
import sys
import shutil
from pathlib import Path
basepath = os.path.dirname(os.path.realpath(__file__))

# If modifying these scopes, delete the file token.json.

SCOPES = 'https://www.googleapis.com/auth/drive.readonly'


def exportnow(collection, filename, filepath):
    ee.Initialize()
    filename = re.sub('[^A-Za-z0-9]+', '', filename)
    coll = ee.FeatureCollection('ft:' + collection)
    try:
        task = ee.batch.Export.table.toAsset(collection=coll,
                description=filename, assetId=filepath)
        task.start()
        print('Exporting: ' + str(collection) + ' to ' + str(filepath))
    except Exception, e:
        pass

def dr2ee(geepath,credpath):
    if credpath is not None and os.path.isfile(os.path.join(basepath,'credentials.json')):
        os.unlink(basepath,'credentials.json')
        shutil.copy(credpath,basepath)
    else:
        shutil.copy(credpath,basepath)
    store = oauth_file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store,argparser.parse_args([]))
    service = build('drive', 'v3', http=creds.authorize(Http()))

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=1000, fields="nextPageToken, files(id, name,mimeType)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            if item['mimeType']=='application/vnd.google-apps.fusiontable':# Remove this line to remove the filter
                #print(u'{0} ({1})'.format(item['name'], item['id'],item['mimeType']))
                exportnow(collection=item['id'],filename=item['name'],filepath=geepath+str(re.sub('[^A-Za-z0-9]+', '', item['name'])))

# dr2ee(geepath='users/samapriya/vec/',credpath=r'C:\Users\samapriya\Box Sync\IUB\Pycodes\Applications and Tools\Drive\drive_tests\credentials.json')
