"""
Unit tests for API
"""

import unittest
import hashlib

import acm_soda.api.utils as views

class TestApiFunctions(unittest.TestCase):
    def testConcat(self):
        """
        concat should take a list of tuples, representing (key,value)s and return a string key1=value1key2=value2...
        """
        t = [('1', '2'), ('3', '4')]
        self.assertEquals(views.concat(t[:-1]), '1=2')
        self.assertEquals(views.concat(t), '1=23=4')
        self.assertEquals(views.concat(t[::-1]), '1=23=4')

    def testDictConcat(self):
        """
        dict_concat should pass a dict into concat as a
        """
        d = {'1':'2', '3':'4'}
        self.assertEquals(views.dict_concat(d), '1=23=4')
        d['signature'] = 'foo'
        self.assertEquals(views.dict_concat(d), '1=23=4')

    def testGenSignature(self):
        d = {'1':'2', '3':'4'}
        s = "secret"
        self.assertEquals(views.gen_signature(d, s), hashlib.md5('1=23=4' + s).hexdigest())

    def testCheckSignature(self):
        s = "secret"
        d = {'1':'2', '3':'4', 'signature':hashlib.md5('1=23=4' + s).hexdigest()}
        self.assertTrue(views.check_signature(d, s))