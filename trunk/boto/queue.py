# Copyright (c) 2006 Mitch Garnaat http://garnaat.org/
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

"""
Represents an SQS Queue
"""

import xml.sax
import urlparse
from boto.exception import SQSError
from boto.handler import XmlHandler
from boto.message import Message

class Queue:
    
    def __init__(self, connection=None, url=None, message_class=Message):
        self.connection = connection
        self.url = url
        self.message_class = message_class

    # This allows the XMLHandler to set the attributes as they are named
    # in the XML response but have the capitalized names converted to
    # more conventional looking python variables names automatically
    def __setattr__(self, key, value):
        if key == 'url' or key == 'QueueUrl':
            self.__dict__['url'] = value
            if value:
                self.__dict__['id'] = urlparse.urlparse(value)[2]
        else:
            self.__dict__[key] = value

    # get the visibility timeout for the queue
    def get_timeout(self):
        path = '%s' % self.id
        response = self.connection.make_request('GET', path)
        body = response.read()
        if response.status >= 300:
            raise SQSError(response.status, response.reason, body)
        handler = XmlHandler(self, {})
        xml.sax.parseString(body, handler)
        self.connection._last_rs = handler.rs
        return handler.rs.VisibilityTimeout

    # convenience method that returns a single message or None if queue is empty
    def read(self, visibility_timeout=None):
        rs = self.get_messages(1, visibility_timeout)
        self.connection._last_rs = rs
        if len(rs) == 1:
            return rs[0]
        else:
            return None

    # add a single message to the queue
    def write(self, message):
        path = '%s/back' % self.id
        message.queue = self
        response = self.connection.make_request('PUT', path, None,
                                                message.get_body())
        body = response.read()
        if response.status >= 300:
            raise SQSError(response.status, response.reason, body)
        handler = XmlHandler(message, {})
        xml.sax.parseString(body, handler)
        message.id = handler.rs.MessageId
        return handler.rs

    # get a variable number of messages, returns a list of messages
    def get_messages(self, num_messages=1, visibility_timeout=None):
        path = '%s/front?NumberOfMessages=%d' % (self.id, num_messages)
        if visibility_timeout:
            path = '%s&VisibilityTimeout=%d' % (path, visibility_timeout)
        response = self.connection.make_request('GET', path)
        body = response.read()
        if response.status >= 300:
            raise SQSError(response.status, response.reason, body)
        handler = XmlHandler(self, {'Message' : self.message_class})
        xml.sax.parseString(body, handler)
        return handler.rs

    def delete_message(self, message):
        path = '%s/%s' % (message.queue.id, message.id)
        response = self.connection.make_request('DELETE', path)
        body = response.read()
        if response.status >= 300:
            raise SQSError(response.status, response.reason, body)
        handler = XmlHandler(self, {})
        xml.sax.parseString(body, handler)
        return handler.rs

    def clear(self):
        """Utility function to remove all messages from a queue"""
        num_messages = 0
        message = self.read()
        while message:
            num_messages += 1
            self.delete_message(message)
            message = self.read()
        return num_messages

    def count(self, page_size=25):
        """Utility function to count the number of messages in a queue"""
        n = 0
        l = self.get_messages(page_size, 10)
        while l:
            for m in l:
                n += 1
            l = self.get_messages(page_size, 10)
        return n
    
