from __future__ import annotations

from typing import Any

from http.enums import HttpResponseCode
from http.header import HttpHeader
from settings import HTTP_ENCODING


class HttpResponseBase:
    __status = None
    __headers = {}

    def __init__(self,
                 status: HttpResponseCode = HttpResponseCode.OK):
        self.__status = status

    def get_status_code(self):
        return self.__status

    def serialize_headers(self):
        return '\r\n'.join("{}: {}".format(key, value) for key, value in self.__headers.values()) + '\r\n'

    def __bytes__(self):
        return self.serialize_headers().encode(HTTP_ENCODING)

    def has_header(self, name):
        return name.lower() in self.__headers

    __contains__ = has_header

    def add_header(self, header: HttpHeader):
        self.__headers[header.name.lower()] = header

    __setitem__ = add_header

    def get_header(self, name: str) -> Any | None:
        if not self.has_header(name):
            return None
        return self.__headers[name.lower()]

    __getitem__ = get_header

    def del_header(self, name: str):
        if not self.has_header(name):
            return
        self.__headers.pop(name.lower())

    __delitem__ = del_header


class HttpResponse(HttpResponseBase):
    __content = None

    def __init__(self, content: str = "", *args, **kwargs):
        super(HttpResponse, self).__init__(*args, **kwargs)
        self.__content = content

    def serialize(self):
        return self.serialize_headers() + '\r\n' + self.__content

    def __bytes__(self):
        return self.serialize().encode(HTTP_ENCODING)


class HttpResponseError(HttpResponse, RuntimeError):
    def __init__(self, *args, **kwargs):
        if 'status' not in kwargs:
            args += 1
            kwargs['status'] = HttpResponseCode.INTERNAL_SERVER_ERROR
        super(HttpResponseError, self).__init__(*args, **kwargs)


class HttpResponseBadRequest(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseBadRequest, self).__init__(status=HttpResponseCode.BAD_REQUEST, *args, **kwargs)


class HttpResponseMethodNotAllowed(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseMethodNotAllowed, self).__init__(status=HttpResponseCode.METHOD_NOT_ALLOWED, *args, **kwargs)


class HttpResponseNotImplemented(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseNotImplemented, self).__init__(status=HttpResponseCode.NOT_IMPLEMENTED, *args, **kwargs)


class HttpResponseHttpVersionNotSupported(HttpResponseError):
    def __init__(self, *args, **kwargs):
        super(HttpResponseHttpVersionNotSupported, self).__init__(status=HttpResponseCode.HTTP_VERSION_NOT_SUPPORTED,
                                                                  *args, **kwargs)
