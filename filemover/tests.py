#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
import os
import subprocess
from core import FileMover
from ConfigParser import SafeConfigParser

class TestSimpleAPICalls(unittest.TestCase):


#    def test_getpath_command(self):
#        root_path = os.path.abspath(os.path.dirname(__file__))
#        proc = subprocess.Popen(['filemover', '--action getfilename', '--app testapp', '--type invoice'], stdout=subprocess.PIPE)
#        stdout_value = proc.communicate()[0]
#        print '\tstdout', repr(stdout_value), '\n'

    def test_doctype_from_filename(self):
        test_filename = 'testapp_testfile_20110701_134840.csv'
        fm = FileMover()
        document_type = fm._get_document_type('testapp', test_filename)
        self.assertEqual('testfile', document_type)

    def test_tablename_from_filename(self):
        test_filename = 'testapp_testfile_20110701_134840.csv'
        fm = FileMover()
        table_name = fm.get_table_name(test_filename)
        self.assertEqual('testapp_testfile', table_name)

    def test_namespace_from_filename(self):
        test_filename = 'testapp_testfile_20110701_134840.csv'
        fm = FileMover()
        namespace = fm._get_namespace_from_filename(test_filename)
        self.assertEqual('testapp', namespace)

    def test_move_file(self):
        test_filename = 'testapp_testfile_20110701_134840.csv'

        fm = FileMover()
        config_parser = fm._parse_ini()
        move_path = config_parser.get('filemover', 'processed_path')
        orig_path = config_parser.get('filemover', 'rootpath')
        with open(os.path.join(orig_path, test_filename), 'w') as file_to_move:
            file_to_move.write('12345')

        fm.move_file(os.path.join(orig_path, test_filename))
        self.assertTrue(os.path.exists('%s/%s' % ((move_path, test_filename))))
        os.remove(os.path.join(move_path, test_filename))

if __name__ == '__main__':
    unittest.main()
