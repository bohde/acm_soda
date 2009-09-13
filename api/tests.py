"""
Unit tests for API
"""

import unittest
import hashlib

import acm_soda.api.utils as utils
import acm_soda.api.views as views
import django.utils.simplejson as json

from django.test import TestCase
from django.test.client import Client

from acm_soda.api.models import Client as SodaClient
from acm_soda.api.models import Inventory as Inventory


class TestApiSecurity(unittest.TestCase):
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
        self.assertEquals(utils.gen_signature(d, s), hashlib.sha256('1=23=4' + s).hexdigest())

    def testCheckSignature(self):
        s = "secret"
        d = {'1':'2', '3':'4', 'signature':hashlib.sha256('1=23=4' + s).hexdigest()}
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
    urls = 'api.test_urls'
    def setUp(self):
        self.secret = 'test'
        self.client_name = 'test'
        self.url = '/test'
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

    def goodPathThrough(self):
        data = json.dumps(self.data)
        response = self.client.post(self.url,data,content_type="application/json")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response.content, 'test')


class TestModels(TestCase):
    fixtures = ['test_fixture.json']

    def testInventoryModel(self):
        response = Inventory.getEntireInventory()
        self.assertEquals(len(response), 2)
        for r in response:
            for x in ['soda', 'quantity']:
                self.assertTrue(r.has_key(x))

    def testInventoryModelForSoda(self):
        response = Inventory.getInventoryForSoda("coke")
        self.assertEquals(len(response), 1)
        for r in response:
            for x in ['soda', 'quantity']:
                self.assertTrue(r.has_key(x))

class TestApiViews(TestCase):
    fixtures = ['test_fixture.json']
    urls = 'api.test_urls'

    def setUp(self):
        self.secret = 'twitter'
        self.client_name = 'twitter'
        self.data = {'client_name':self.client_name}
        self.data['signature'] = utils.gen_signature(self.data, self.secret)

    def buying(self):
        self.user = ''

class TestInventoryViews(TestApiViews):
    def setUp(self):
        TestApiViews.setUp(self)
        self.url = '/inventory'

    def testInventoryUrl(self):
        data = json.dumps(self.data)
        response = self.client.post(self.url,data,content_type="application/json")
        self.assertEquals(response.status_code, 200)
        j = json.loads(response.content)
        self.assertEquals(len(j), 2)
        for r in j:
            for x in ['soda', 'quantity']:
                self.assertTrue(r.has_key(x))

    def testInventoryUrlForSpecificSodas(self):
        data = json.dumps(self.data)
        for soda in ["mtn", "coke"]:
            response = self.client.post(self.url + "/" + soda ,data,content_type="application/json")
            self.assertEquals(response.status_code, 200)
            j = json.loads(response.content)
            self.assertEquals(len(j), 1)
            for r in j:
                for x in ['soda', 'quantity']:
                    self.assertTrue(r.has_key(x))

class TestSlotViews(TestApiViews):
    def setUp(self):
        TestApiViews.setUp(self)
        self.url = '/slot'

    def testSlot(self):
        data = json.dumps(self.data)
        for slot in [1,2]:
            response = self.client.post(self.url + "/" + str(slot), data, content_type="application/json")
            self.assertEquals(response.status_code, 200)
            j = json.loads(response.content)
            self.assertEquals(len(j), 1)
            for r in j:
                for x in ['soda', 'quantity']:
                    self.assertTrue(r.has_key(x))

    # def testSlotBuy(self):
    #     data = json.dumps(self.data)
    #     for slot, res in [1,200
