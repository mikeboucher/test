#!/usr/local/bin/python

import logging
import requests
import time
from requests.adapters import HTTPAdapter
import pprint
import re


class RestRequestsSession(object):

    def __init__(self):
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.session.headers = {'Accept': 'application/json, */*',
                                'Accept-language': 'en_US',
                                'Content-Type': 'application/json'}
        self.session.verify = False
        self.urlRoot = None
        
    def set_apiVersion(self, apiVersion=None):
        '''Set or clear the X-Api-Version in the header.'''
        if 'X-Api-Version' in self.session.headers and not apiVersion:  # Remove it?
            del self.session.headers['X-Api-Version']
        else:  # Insert or Update
            self.session.headers.update({'X-Api-Version': apiVersion})  

    def set_sessionId(self, sessionId=None):
        '''Set or clear the auth string in the headers'''
        if 'auth' in self.session.headers and not sessionId:  # Remove it?
            del self.session.headers['auth']
        else:  # Insert or Update
            self.session.headers.update({'auth': sessionId})
            
    def set_urlRoot(self, urlRoot):
        self.urlRoot = urlRoot
        
    def get_urlRoot(self):
        return self.urlRoot
         
    def print_headers(self):
        print self.session.headers

    ###########################################################################

    def get(self, uri, **kwargs):
        try:
            #url = self.get_urlRoot() + uri
            url = uri
            print '\nURL\tGET %s\nHeader %s\n' % (url)
            #response = self.session.get(url, **kwargs)
            response = self.session.get(url)
            #response = re.json()
            print '\nStatus %d\nRequest Headers %s\nRequest Body %s\nResponse Headers %s' % (
             response.status_code, 
             response.request.headers,
             response.request.body,
             response.headers)
        except Exception as e:
            msg = "Exception occurred while attempting to GET: %s" % (uri)
            raise Exception(msg, e)
        return response        


z = RestRequestsSession()
z.get('http://httpbin.org/get')
