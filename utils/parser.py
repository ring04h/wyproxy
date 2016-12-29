# encoding: utf-8

from __future__ import absolute_import

import json
import mimetypes
from config import media_types, static_files, static_ext, save_content

def save_cnf(args):
    """save wyproxy client options"""
    try:
        fd = open('.proxy.cnf', 'w')
        json.dump(args.__dict__, fd)
    finally:
        fd.close()

def read_cnf():
    """read wyproxy client options conf"""
    try:
        fd = open('.proxy.cnf', 'r')
        return json.load(fd)
    finally:
        fd.close()

class ResponseParser(object):
    """docstring for ResponseParser"""

    def __init__(self, f):
        super(ResponseParser, self).__init__()
        self.flow = f
        self.content_type = self.get_content_type()
        self.extension = self.get_extension()
        self.ispass = self.capture_pass()

    def parser_data(self):
        """parser the capture response & request"""

        result = {}
        result['content_type'] = self.content_type
        result['url'] = self.get_url()
        result['path'] = self.get_path()
        result['extension'] = self.get_extension()
        result['host'] = self.get_host()
        result['port'] = self.get_port()
        result['scheme'] = self.get_scheme()
        result['method'] = self.get_method()
        result['status_code'] = self.get_status_code()
        result['date_start'] = self.flow.response.timestamp_start
        result['date_end'] = self.flow.response.timestamp_end
        result['content_length'] = self.get_content_length()
        result['static_resource'] = self.ispass
        result['header'] = self.get_header()
        result['request_header'] = self.get_request_header()
        
        # request resource is media file & static file, so pass
        if self.ispass:
            result['content'] = None
            result['request_content'] = None
            return result

        result['content'] = self.get_content() if save_content else ''
        result['request_content'] = self.get_request_content() if save_content else ''
        return result

    def get_content_type(self):

        if not self.flow.response.headers.get('Content-Type'):
            return ''
        return self.flow.response.headers.get('Content-Type').split(';')[:1][0]

    def get_content_length(self):
        if self.flow.response.headers.get('Content-Length'):
            return int(self.flow.response.headers.get('Content-Length'))
        else:
            return 0

    def capture_pass(self):
        """if content_type is media_types or static_files, then pass captrue"""

        if self.extension in static_ext:
            return True

        # can't catch the content_type
        if not self.content_type:
            return False

        if self.content_type in static_files:
            return True

        http_mime_type = self.content_type.split('/')[:1]
        if http_mime_type:
            return True if http_mime_type[0] in media_types else False
        else:
            return False

    def get_header(self):
        return self.parser_header(self.flow.response.headers)

    def get_content(self):
        return self.flow.response.content

    def get_request_header(self):
        return self.parser_header(self.flow.request.headers)

    def get_request_content(self):
        return self.flow.request.content

    def get_url(self):
        return self.flow.request.url

    def get_path(self):
        return '/{}'.format('/'.join(self.flow.request.path_components))

    def get_extension(self):
        if not self.flow.request.path_components:
            return ''
        else:
            end_path = self.flow.request.path_components[-1:][0]
            split_ext = end_path.split('.')
            if not split_ext or len(split_ext) == 1:
                return ''
            else:
                return split_ext[-1:][0][:32]

    def get_scheme(self):
        return self.flow.request.scheme

    def get_method(self):
        return self.flow.request.method

    def get_port(self):
        return self.flow.request.port

    def get_host(self):
        return self.flow.request.host

    def get_status_code(self):
        return self.flow.response.status_code

    @staticmethod
    def parser_header(header):
        headers = {}
        for key, value in header.iteritems():
            headers[key] = value
        return headers
