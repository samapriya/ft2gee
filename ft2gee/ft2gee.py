__copyright__ = """

    Copyright 2019 Samapriya Roy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

#! /usr/bin/env python

import argparse,os,ee,sys,platform
os.chdir(os.path.dirname(os.path.realpath(__file__)))
from gdrive2tab import dr2ee
from ee_ftables_tables import fexp
from scriptcheck import fscript
lpath=os.path.dirname(os.path.realpath(__file__))
sys.path.append(lpath)


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])

def quota():
    quota=ee.data.getAssetRootQuota(ee.data.getAssetRoots()[0]['id'])
    print('')
    print("Total Quota: "+str(humansize(quota['asset_size']['limit'])))
    print("Used Quota: "+str(humansize(quota['asset_size']['usage'])))

def quota_from_parser(args):
    quota()

def dr2ee_from_parser(args):
    dr2ee(geepath=args.gee,credpath=args.credentials)

def fexp_from_parser(args):
    fexp(local=args.local,geepath=args.gee)

def fscript_from_parser(args):
    fscript(local=args.local,geepath=args.gee)

spacing="                               "
def main(args=None):
    parser = argparse.ArgumentParser(description='Fusion table to EE tables CLI')
    subparsers = parser.add_subparsers()

    parser_quota = subparsers.add_parser('quota', help='Print Earth Engine total quota and used quota')
    parser_quota.set_defaults(func=quota_from_parser)

    parser_dr2ee = subparsers.add_parser('drive2gee', help='Exports Google Drive Fusion tables to Earth Engine tables')
    required_named = parser_dr2ee.add_argument_group('Required named arguments.')
    required_named.add_argument('--gee', help='Path to Google Earth Engine asset folder for tables to be exported', required=True)
    optional_named = parser_dr2ee.add_argument_group('Optional named arguments')
    optional_named.add_argument('--credentials', help='Credentials file downloaded for gdrive',default=None)
    parser_dr2ee.set_defaults(func=dr2ee_from_parser)

    parser_fexp = subparsers.add_parser('gee2tab', help='Exports Earth Engine referenced fusion tables to Earth Engine tables')
    required_named = parser_fexp.add_argument_group('Required named arguments.')
    required_named.add_argument('--local', help='Local path to folder with Google Earth Engine Scripts', required=True)
    required_named.add_argument('--gee', help='Path to Google Earth Engine asset folder for tables to be exported', required=True)
    parser_fexp.set_defaults(func=fexp_from_parser)

    parser_fscript = subparsers.add_parser('scriptcheck', help='Replaces referenced fusion tables in Earth Engine scripts to EE tables')
    required_named = parser_fscript.add_argument_group('Required named arguments.')
    required_named.add_argument('--local', help='Local path to a Google Earth Engine Script to check', required=True)
    required_named.add_argument('--gee', help='Earth Engine folder where EE tables were exported', required=True)
    parser_fscript.set_defaults(func=fscript_from_parser)

    args = parser.parse_args()

    #ee.Initialize()
    args.func(args)

if __name__ == '__main__':
    main()
