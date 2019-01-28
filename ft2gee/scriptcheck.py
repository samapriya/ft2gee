#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import pendulum
import os
import fileinput
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path = os.path.dirname(os.path.realpath(__file__))


# Function to access ftables in scripts and export to tables in EE
def fscript(local, geepath):
    [head, tail] = os.path.split(local)
    open(os.path.join(head, tail + '_FT'), 'w')
    with open(local) as f:
        print('\n' + 'Attempting to export GEE Script with path edits at: ' + str(os.path.join(head, tail + '_FT')))
        for line in f:
            if "ee.FeatureCollection('ft:" in line:
                try:
                    current = str(pendulum.today()).split('T')[0]
                    with open(os.path.join(head, tail + '_FT'), 'a') as \
                        jsfile:
                        jsfile.write('Last edited at: ' + str(current))
                        jsfile.write('\n')
                    id = line.split('ft:')[1].split("'")[0]
                    name = line.split('var')[1].split('=')[0]
                    name = str(re.sub('[^A-Za-z0-9]+', '', name))
                    filepath = geepath + '/'+str(re.sub('[^A-Za-z0-9]+', ''
                            , name))
                    combined = str(id) + '&' + str(name) + '&' \
                        + str(filepath)
                    orig = 'ft:' + str(id)
                    final = filepath
                    for line in fileinput.input(local):
                        line = line.replace(orig, final)
                        with open(os.path.join(head, tail + '_FT'), 'a'
                                  ) as jsfile:
                            jsfile.write(line)
                except Exception, e:
                    print e


# fscript(local=r'C:\Users\samapriya\Cloud Shadow',geepath='users/samapriya/vec/')
