from http.enums import HttpMethod, HttpVersion
from http.response import HttpResponseBadRequest, HttpResponseMethodNotAllowed, HttpResponseNotImplemented, \
    HttpResponseHttpVersionNotSupported
from settings import HTTP_ENCODING


class HttpRequest:
    def __init__(self, raw_bytes: bytes):
        if not raw_bytes:
            raise HttpResponseBadRequest()

        raw_data = raw_bytes.decode(HTTP_ENCODING)
        lines = raw_data.split("\r\n")
        if len(lines) == 0:
            raise HttpResponseBadRequest()

        first_line_data = lines[0].split(" ")
        if len(first_line_data) != 3:
            raise HttpResponseBadRequest()
        method, path, http_version = first_line_data

        for avail_method in HttpMethod:
            if str(avail_method) == method.upper():
                method = avail_method
                break
        if isinstance(method, str):
            raise HttpResponseNotImplemented()

        for avail_version in HttpVersion:
            if str(avail_version) == http_version.upper():
                http_version = avail_version
                break
        if isinstance(http_version, str):
            raise HttpResponseHttpVersionNotSupported()
