
import json
import requests


class restException(Exception):
    def __init__(self, message, response=None):
        self.message = message
        self.response = response
        
    def __str__(self):
        try:
            response = "%s\n\tResponse Headers: %s\n\tBody: %s" % (self.message, self.response, self.response.body)
        except:
            response = "%s\n\tResponse: %s" % (self.message, self.response)
        return response


class requestsClient(object):
    '''
    @staticmethod
    def formatJson(data):
        return json.dumps(data, sort_keys=True, indent=4, separaters=(',', ': '))

    @staticmethod
    def printJson(data):
        print(formatJson(data))

    @staticmethod
    def isJson(val):
        if 'json' in val:
            return True
        for jtype in {'application/json', 'javascript'}:
            if val in jtype:
                return True
        return False      
    '''
	#
	# Initialize Session object
	#
	
    def __init__(self):
        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(max_retries=3))
        self.session.mount('https://', HTTPAdapter(max_retries=3))
        self.set_base_url()
        self.set_default_headers()
        
    def set_base_url(self, appliance=""):
        self.base_url = 'https://' + appliance
        return self.base_url
    
    def get_base_url(self):
        return self.base_url

    def set_default_headers(self):
        self.session.headers = {'accept': 'application/json',
                                'accept-language': 'en_US',
                                'content-type': 'application/json'}
							   

    def set_active_session(self, sessionId):
        '''Add the sessionID to the sessions default headers.'''
        self.session.headers.update({'auth': sessionId})
        
    def get_session(self):
        '''Returns the current sessionID used in default headers.'''
        if 'auth' in self.session.headers:
            return self.session.headers['auth']
        return False
        
    def clear_session(self):
        '''Removes the sessionID from the default headers.'''
        self.session.headers.update({'auth': None})

	#	
	# Login/Logout actions
	#
	
    def login(self, appliance, username, password):
        self.set_base_url(appliance)
        uri = '/rest/login-sessions'
        data = {'userName': username, 'password': password}
        (url, headers, data) = self.build_request(uri, data)
        try:
            response = self.post(url, data=data, headers=headers)
        except Exception:
            print "Something bad happened..."
        if 'sessionID' in response.body:
            self.set_sessionId(response.body['sessionId'])
        else:
            print "didn't get a sessionID returned"
            raise
        return response

    def logout(self):
        """Assure we have a current session and issue a logout request."""
        if self.get_sessionId():
            url = self.get_base_url() + '/rest/login-sessions'
            try:
                response = self.delete(url)
            except Exception, e:
                print "caught exception while trying to logout: ", e
            '''Remove the sessionID from the default headers'''
            self.clear_sessionId()
            return response

    #
    # HTTP verbs - shorthand functions
    #    
    def get(self, uri, **kwargs):
        (url, headers, data) = self.build_request(uri, **kwargs)
        response = self.session.get(url, data=data, headers=headers, **kwargs)
        self.printStuff(response)
        return response
    
    def put(self, url, **kwargs):
        return self.session.put(url, **kwargs) 
    
    def update(self, url, **kwargs):
        return self.session.update(url, **kwargs) 
    
    def post(self, uri, **kwargs):
        (url, headers, data) = self.build_request(uri, **kwargs)
        response = self.session.post(url, data=data, headers=headers, **kwargs)
        self.printStuff(response)
        return response
    
    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs) 
    
    def build_request(self, uri, data=None, headers={}, **kwargs):
        url = self.get_base_url() + uri
        if 'headers' in kwargs:
            headers = self.additional_headers(headers)
        if data:
            #if isJson(data):
            #    data = formatJson(data)
            # Add the length of the request body in the header 
            data = formatJson(data)
            headers['content-length'] = "%s" % (len(data))
        print("\nRequest header(s): %s\n%s" % formatJson(self.session.headers()), formatJson(headers))
        return (url, headers, data)

    def printStuff(self, request):
        print("\nRequest header(s): %s" % formatJson(self.session.request.headers))
        print("\nRequest body %s" % formatJson(request.data))
        print("\nResponse header %s" % formatJson(request.headers))
        print("\nResponse body %s" % formatJson(self.session.response))
