#!/opt/bin/python2.7
#coding:utf-8
# created on 6/30/11
import argparse
import os
import re
import sys
from ConfigParser import SafeConfigParser
from shutil import move
from datetime import datetime

class FileMover(object):
    ini_path = '/var/files/'

    def set_results(self, results):
        self.results = results

    def _parse_ini(self):
        """
        Get global values and return the parser object
        """
        config_parser = SafeConfigParser()
        try:
            config_parser.read(os.path.join(FileMover.ini_path, 'filemover.ini'))
        except IOError, e:
            sys.stdout.write('Error: could not find file %s' % os.path.join(FileMover.ini_path, 'filemover.ini'))
            sys.exit(1)
        self.root_path = config_parser.get('filemover', 'rootpath')
        return config_parser

    def _get_document_type(self, namespace, filename):
        """
        Return the document type by using a regex the filename and testing against
        valid file types for the namespace
        """

        document_regex = re.compile('%s_(?P<document_type>[a-zA-Z]+)' % namespace)
        document_type = re.findall(document_regex, filename)
        if len(document_type) != 1:
            return False
        return document_type[0]

    def _get_namespace_from_filename(self, filename):
        namespace_regex = '^[a-zA-Z]+'
        text_matches = re.findall(namespace_regex, filename)
        return text_matches[0]


    def get_file_name(self):
        fn_parse = self._parse_ini()
        namespace = fn_parse.get(self.results.app, 'namespace')
        timeformat = fn_parse.get(self.results.app, 'datetime_format')

        filename =  str.format('{0}_{1}_{2}.{3}', namespace, self.results.filetype, datetime.now().strftime(timeformat), 'csv')
        sys.stdout.write(os.path.join(self.root_path, filename))

    def display_config_location(self):
        sys.stdout.write('config file: %s ' % os.path.join(FileMover.ini_path, 'filemover.ini') + '\n\n')


    def display_config(self):
        sys.stdout.write('config file: %s ' % os.path.join(FileMover.ini_path, 'filemover.ini') + '\n\n')
        config_parser = SafeConfigParser()
        try:
            config_parser.read(os.path.join(FileMover.ini_path, 'filemover.ini'))
        except IOError, e:
            sys.stdout.write('Error: could not find file %s' % os.path.join(FileMover.ini_path, 'filemover.ini'))
            sys.exit('NoConfig')
        default_items = config_parser.items('filemover')
        for item in default_items:
            sys.stdout.write(str(item) + '\n')

    def get_table_name(self, filename):
        tn_parser = self._parse_ini()
        namespace = self._get_namespace_from_filename(filename)
        document_type = self._get_document_type(namespace, filename)
        valid_types = tn_parser.get(namespace, 'file_ids')
        if document_type not in valid_types:
            error_string = '%s is not a valid document type for namespace %s' % (document_type, namespace)
            error_string+= '\n valid types are: %s' % valid_types
            sys.stdout.write(error_string)
            sys.exit(error_string)
        table_name = '%s_%s' % (namespace, document_type)
        return table_name

    def move_file(self, filepath):
        exist_path, filename = os.path.split(filepath)
        mv_parser = self._parse_ini()
        processed_path = mv_parser.get('filemover', 'processed_path')
        move_path = os.path.join(processed_path, filename)
        move(filepath, move_path)
        sys.stdout.write('Moved file to :%s\n' % move_path)
        



def main():
    parser = argparse.ArgumentParser(description='Global File Manipulation')
    parser.add_argument('--action', action="store", dest="action")
    parser.add_argument('--app', action="store", dest="app")
    parser.add_argument('--type', action="store", dest="filetype")
    parser.add_argument('--filename', action='store', dest='filepath')
    results = parser.parse_args()
    fm = FileMover()
    fm.set_results(results)

    if results.action == 'config':
        fm.display_config()

    if results.action == 'getfilename':
        fm.get_file_name()

    if results.action == 'move':
        fm.move_file(fm.results.filepath)
