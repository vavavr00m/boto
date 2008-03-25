# Copyright (c) 2006,2007 Mitch Garnaat http://garnaat.org/
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

#
# Parts of this code were copied or derived from sample code supplied by AWS.
# The following notice applies to that code.
#
#  This software code is made available "AS IS" without warranties of any
#  kind.  You may copy, display, modify and redistribute the software
#  code either by itself or as incorporated into your code; provided that
#  you do not remove any proprietary notices.  Your use of this software
#  code is at your own risk and you waive any claim against Amazon
#  Digital Services, Inc. or its affiliates with respect to your use of
#  this software code. (c) 2006 Amazon Digital Services, Inc. or its
#  affiliates.

"""
Handles basic connections to AWS
"""

import base64
import hmac
import httplib
import socket, errno
import re
import sha
import sys
import time
import urllib, urlparse
import os
import xml.sax
from boto.exception import AWSConnectionError, BotoClientError, BotoServerError
import boto.utils
from boto import config, UserAgent

PORTS_BY_SECURITY = { True: 443, False: 80 }

class AWSAuthConnection:
    def __init__(self, server, aws_access_key_id=None,
                 aws_secret_access_key=None, is_secure=True, port=None,
                 proxy=None, proxy_port=None, proxy_user=None,
                 proxy_pass=None, debug=0, https_connection_factory=None):
        self.num_retries = 5
        self.is_secure = is_secure
        self.handle_proxy(proxy, proxy_port, proxy_user, proxy_pass)
        # define exceptions from httplib that we want to catch and retry
        self.http_exceptions = (httplib.HTTPException, socket.error, socket.gaierror)
        # define values in socket exceptions we don't want to catch
        self.socket_exception_values = (errno.EINTR,)
        if https_connection_factory is not None:
            self.https_connection_factory = https_connection_factory[0]
            self.http_exceptions += https_connection_factory[1]
        else:
            self.https_connection_factory = None
        if (is_secure):
            self.protocol = 'https'
        else:
            self.protocol = 'http'
        self.server = server
        self.debug = config.getint('Boto', 'debug', debug)
        if port:
            self.port = port
        else:
            self.port = PORTS_BY_SECURITY[is_secure]
        self.server_name = '%s:%d' % (server, self.port)
        
        if aws_access_key_id:
            self.aws_access_key_id = aws_access_key_id
        elif os.environ.has_key('AWS_ACCESS_KEY_ID'):
            self.aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        elif config.has_option('Credentials', 'aws_access_key_id'):
            self.aws_access_key_id = config.get('Credentials', 'aws_access_key_id')
        
        if aws_secret_access_key:
            self.aws_secret_access_key = aws_secret_access_key
        elif os.environ.has_key('AWS_SECRET_ACCESS_KEY'):
            self.aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        elif config.has_option('Credentials', 'aws_secret_access_key'):
            self.aws_secret_access_key = config.get('Credentials', 'aws_secret_access_key')

        # cache up to 20 connections
        self._cache = boto.utils.LRUCache(20)
        self.refresh_http_connection(self.server, self.is_secure)
        self._last_rs = None

    def handle_proxy(self, proxy, proxy_port, proxy_user, proxy_pass):
        self.proxy = proxy
        self.proxy_port = proxy_port
        self.proxy_user = proxy_user
        self.proxy_pass = proxy_pass
        if os.environ.has_key('http_proxy') and not self.proxy:
            pattern = re.compile(
                '(?:http://)?' \
                '(?:(?P<user>\w+):(?P<pass>.*)@)?' \
                '(?P<host>[\w\-\.]+)' \
                '(?::(?P<port>\d+))?'
            )
            match = pattern.match(os.environ['http_proxy'])
            if match:
                self.proxy = match.group('host')
                self.proxy_port = match.group('port')
                self.proxy_user = match.group('user')
                self.proxy_pass = match.group('pass')
        else:
            if not self.proxy:
                self.proxy = config.get_value('Boto', 'proxy', None)
            if not self.proxy_port:
                self.proxy_port = config.get_value('Boto', 'proxy_port', None)
            if not self.proxy_user:
                self.proxy_user = config.get_value('Boto', 'proxy_user', None)
            if not self.proxy_pass:
                self.proxy_pass = config.get_value('Boto', 'proxy_pass', None)

        if not self.proxy_port and self.proxy:
            print "http_proxy environment variable does not specify " \
                "a port, using default"
            self.proxy_port = self.port
        self.use_proxy = (self.proxy != None)
        if self.use_proxy and self.is_secure:
            raise AWSConnectionError("Unable to provide secure connection through proxy")

    def get_http_connection(self, host, is_secure):
        if host is None:
            host = '%s:%d' % (self.server, self.port)
        cached_name = is_secure and 'https://' or 'http://'
        cached_name += host
        if cached_name in self._cache:
            return self._cache[cached_name]
        return self.refresh_http_connection(host, is_secure)

    def refresh_http_connection(self, host, is_secure):
        if self.use_proxy:
            host = '%s:%d' % (self.proxy, int(self.proxy_port))
        if host is None:
            host = '%s:%d' % (self.server, self.port)
        boto.log.info('establishing HTTP connection')
        if is_secure:
            if self.https_connection_factory:
                connection = self.https_connection_factory(host)
            else:
                connection = httplib.HTTPSConnection(host)
        else:
            connection = httplib.HTTPConnection(host)
        if self.debug > 1:
            connection.set_debuglevel(self.debug)
        cached_name = is_secure and 'https://' or 'http://'
        cached_name += host
        if cached_name in self._cache:
            boto.log.info('closing old HTTP connection')
            self._cache[cached_name].close()
        self._cache[cached_name] = connection
        # update self.connection for backwards-compatibility
        if host.split(':')[0] == self.server and is_secure == self.is_secure:
            self.connection = connection
        return connection

    def prefix_proxy_to_path(self, path, host=None):
        path = self.protocol + '://' + (host or self.server) + path
        return path

    def get_proxy_auth_header(self):
        auth = base64.encodestring(self.proxy_user+':'+self.proxy_pass)
        return {'Proxy-Authorization': 'Basic %s' % auth}

    def _mexe(self, method, path, data, headers, host=None, sender=None):
        """
        mexe - Multi-execute inside a loop, retrying multiple times to handle
               transient Internet errors by simply trying again.
               Also handles redirects.

        This code was inspired by the S3Utils classes posted to the boto-users
        Google group by Larry Bates.  Thanks!
        """
        boto.log.info('Method: %s' % method)
        boto.log.info('Path: %s' % path)
        boto.log.info('Data: %s' % data)
        boto.log.info('Headers: %s' % headers)
        boto.log.info('Host: %s' % host)
        response = None
        body = None
        e = None
        num_retries = config.getint('Boto', 'num_retries', self.num_retries)
        i = 0
        connection = self.get_http_connection(host, self.is_secure)
        while i <= num_retries:
            try:
                if callable(sender):
                    response = sender(connection, method, path, data, headers)
                else:
                    connection.request(method, path, data, headers)
                    response = connection.getresponse()
                location = response.getheader('location')
                if response.status == 500 or response.status == 503:
                    boto.log.info('received %d response, retrying in %d seconds' % (response.status, 2**i))
                    body = response.read()
                elif response.status < 300 or response.status >= 400 or \
                        not location:
                    return response
                else:
                    scheme, host, path, params, query, fragment = \
                            urlparse.urlparse(location)
                    if query:
                        path += '?' + query
                    boto.log.info('Redirecting: %s' % scheme + '://' + host + path)
                    connection = self.get_http_connection(host,
                            scheme == 'https')
                    continue
            except KeyboardInterrupt:
                sys.exit('Keyboard Interrupt')
            except self.http_exceptions, e:
                boto.log.info('encountered %s exception, reconnecting' % \
                                  e.__class__.__name__)
                connection = self.refresh_http_connection(host, self.is_secure)
            time.sleep(2**i)
            i += 1
        # If we made it here, it's because we have exhausted our retries and stil haven't
        # succeeded.  So, if we have a response object, use it to raise an exception.
        # Otherwise, raise the exception that must have already happened.
        if response:
            raise BotoServerError(response.status, response.reason, body)
        elif e:
            raise e
        else:
            raise BotoClientError('Please report this exception as a Boto Issue!')

    def make_request(self, method, path, headers=None, data='', host=None,
            auth_path=None, sender=None):
        if headers == None:
            headers = {'User-Agent' : UserAgent}
        else:
            headers = headers.copy()
        if not headers.has_key('Content-Length'):
            headers['Content-Length'] = len(data)
        if self.use_proxy:
            path = self.prefix_proxy_to_path(path, host)
            if self.proxy_user and self.proxy_pass:
                headers.update(self.get_proxy_auth_header())
        self.add_aws_auth_header(headers, method, auth_path or path)
        return self._mexe(method, path, data, headers, host, sender)

    def add_aws_auth_header(self, headers, method, path):
        if not headers.has_key('Date'):
            headers['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                            time.gmtime())

        c_string = boto.utils.canonical_string(method, path, headers)
        boto.log.info('Canonical: %s' % c_string)
        headers['Authorization'] = \
            "AWS %s:%s" % (self.aws_access_key_id,
                           boto.utils.encode(self.aws_secret_access_key,
                                             c_string))

class AWSQueryConnection(AWSAuthConnection):

    APIVersion = ''
    SignatureVersion = '1'

    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None,
                 is_secure=True, port=None, proxy=None, proxy_port=None,
                 host=None, debug=0, https_connection_factory=None):
        AWSAuthConnection.__init__(self, host,
                                   aws_access_key_id, aws_secret_access_key,
                                   is_secure, port, proxy, proxy_port, debug,
                                   https_connection_factory)

    def make_request(self, action, params=None, path=None, verb='GET'):
        headers = {'User-Agent' : UserAgent}
        if path == None:
            path = '/'
        if params == None:
            params = {}
        h = hmac.new(key=self.aws_secret_access_key, digestmod=sha)
        params['Action'] = action
        params['Version'] = self.APIVersion
        params['AWSAccessKeyId'] = self.aws_access_key_id
        params['SignatureVersion'] = self.SignatureVersion
        params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        keys = params.keys()
        keys.sort(cmp = lambda x, y: cmp(x.lower(), y.lower()))
        qs = ''
        for key in keys:
            h.update(key)
            h.update(str(params[key]))
            qs += key + '=' + urllib.quote(unicode(params[key]).encode('utf-8')) + '&'
        signature = base64.b64encode(h.digest())
        qs = path + '?' + qs + 'Signature=' + urllib.quote(signature)
        
        if self.use_proxy:
            qs = self.prefix_proxy_to_path(qs)

        return self._mexe(verb, qs, None, headers)

    def build_list_params(self, params, items, label):
        for i in range(1, len(items)+1):
            params['%s.%d' % (label, i)] = items[i-1]
