import requests
from requests.auth import AuthBase

class FusionAuth(AuthBase):
    """Attaches auth header """
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.sessionId = None
        
    def __call__(self, request):
        """ modify and return the request """
        if self.sessionId:
            request.headers['auth'] = self.sessionId

session = requests.Session()
session.headers.update({'Accept': 'application/json, */*',
           'Accept-language': 'en_US',
           'Content-Type': 'application/json'})
session.verify = False

url = "https://16.114.190.161/rest/version"
response = session.get(url)
print "\nHeaders we sent: %s" % response.request.headers
print "\nHeaders returned: %s" % response.headers
print "\nResponse Text: %s" % response.text

url = "https://16.114.190.161/rest/version"
response = session.get(url)
print "\nHeaders we sent: %s" % response.request.headers
print "\nHeaders returned: %s" % response.headers
print "\nResponse Text: %s" % response.text
print response

url = "https://16.114.190.161/rest/appliance/eula/status"
response = session.get(url)
print "\nHeaders we sent: %s" % response.request.headers
print "\nHeaders returned: %s" % response.headers
print "\nResponse Text: %s" % response.text
print response
