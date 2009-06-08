"""
Unit tests for API
"""

import unittest
import hashlib

import acm_soda.api.utils as utils
import django.utils.simplejson as json

from django.test import TestCase
from django.test.client import Client

from acm_soda.api.models import Client as SodaClient


class TestApiFunctions(unittest.TestCase):
    def testConcat(self):
        """
        concat should take a list of tuples, representing (key,value)s and return a string key1=value1key2=value2...
        """
        t = [('1', '2'), ('3', '4')]
        self.assertEquals(utils.concat(t[:-1]), '1=2')
        self.assertEquals(utils.concat(t), '1=23=4')
        self.assertEquals(utils.concat(t[::-1]), '1=23=4')

    def testDictConcat(self):
        """
        dict_concat should pass a dict into concat as a
        """
        d = {'1':'2', '3':'4'}
        self.assertEquals(utils.dict_concat(d), '1=23=4')
        d['signature'] = 'foo'
        self.assertEquals(utils.dict_concat(d), '1=23=4')

    def testGenSignature(self):
        d = {'1':'2', '3':'4'}
        s = "secret"
        self.assertEquals(utils.gen_signature(d, s), hashlib.md5('1=23=4' + s).hexdigest())

    def testCheckSignature(self):
        s = "secret"
        d = {'1':'2', '3':'4', 'signature':hashlib.md5('1=23=4' + s).hexdigest()}
        self.assertTrue(utils.check_signature(d, s))


def testContent(self, error_ret):
    data = json.dumps(self.data)
    response = self.client.post(self.url,data,content_type="application/json")
    self.assertEquals(response.status_code, 400)
    self.assertEquals(response.content, error_ret)

def testContentRequiresWrapper(missing, error_ret):
    def wrapper(self):
        del self.data[missing]
        testContent(self, error_ret)
    return wrapper

class TestApiWrappers(TestCase):
    def setUp(self):
        self.secret = 'test'
        self.client_name = 'test'
        self.url = '/api/inventory'
        self.data = {'method':'inventory.list', 'client_name':self.client_name}
        self.data['signature'] = utils.gen_signature(self.data, self.secret)
        SodaClient.objects.create(name=self.client_name, auth_key=self.secret)

    def testGetFailsAndReturnsAllowHeaderWithPost(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 405)
        self.assertEquals(response['ALLOW'], 'POST')

    def testPostDoesNotReturnStatus405(self):
        response = self.client.post(self.url)
        self.assertNotEquals(response.status_code, 405)

    def testContentTypeFailsIfNotJson(self):
        response = self.client.post(self.url,"",content_type="text/xml")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, 'Request must have the content-type "application/json"')


    """
    Checks to make sure that if the request doesn't have one of the parameters, it will just return an error
    """
    testContentRequiresClient = testContentRequiresWrapper('client_name', 'Request JSON must include an "client_name" element.')
    testContentRequiresSignature = testContentRequiresWrapper('signature', 'Request JSON must include an "signature" element.')

    def checkNonExistentClientFails(self):
        self.data['client_name'] = 'bob'
        testContent(self, 'Access for that "client_name" is denied.')

    def checkClientExistsButSignatureWrong(self):
        current_signature = self.data['signature']
        self.data['signature'] = ''
        self.assertNotEquals(current_signature, '')
        testContent(self, 'Access for that "client_name" is denied.')

