from __future__ import annotations

from typing import List

from http.enums import HttpMethod, HttpVersion
from http.header import HttpHeader, HEADER_CONTENT_LENGTH
from http.response import HttpResponseBadRequest, HttpResponseNotImplemented, HttpResponseHttpVersionNotSupported
from settings import HTTP_ENCODING


class HttpRequest:
    """
    HTTP Request class. Contains information regarding the requested method, path, HTTP version, headers
    and body (if present).
    Constructing the class will throw HttpResponseError with further information on why the request is not
    valid.
    """
    __method = None
    __path = None
    __http_version = None
    __headers = {}
    __body = None

    def __init__(self, raw_bytes: bytes):
        """
        Given an array of bytes, tries to parse the request.
        :param raw_bytes:
        """
        if not raw_bytes:
            raise HttpResponseBadRequest(content="No data found to be parsed")

        raw_data = raw_bytes.decode(HTTP_ENCODING)
        lines = raw_data.split("\r\n")
        if len(lines) == 0:
            raise HttpResponseBadRequest(content="No data found")

        # First we parse the request-line
        self.__init_parse_requestline(lines)
        # Then we parse the header lines (which follow right after the request-line)
        c_headers = self.__init_parse_headers(lines[1:])
        # And finally, we parse the body (or we make sure that such body is not present)
        self.__init_parse_body(lines[(1 + c_headers + 1):])

    def __init_parse_requestline(self, lines):
        """
        Given an array of lines, get the first one and parse it with the request-line format
        :param lines: list of lines in the request
        :return: None
        """
        first_line_data = lines[0].split(" ")
        if len(first_line_data) != 3:
            # If we split the first line by the space, and does not have 3 elements, request is malformed
            raise HttpResponseBadRequest(content="Invalid request-line")
        method, path, http_version = first_line_data

        for avail_method in HttpMethod:
            # Method is case sensitive, so no .upper()
            if str(avail_method) == method:
                method = avail_method
                break
        if isinstance(method, str):
            # If we are not able to get the HttpMethod object from it, it is because we do not support
            # the request method
            raise HttpResponseNotImplemented(content="Method {} is not available".format(method))
        self.__method = method

        # Path is fine, leave as is
        self.__path = path

        # Now, try to parse the HTTP version
        http = http_version.split("/")
        if len(http) != 2:
            # It has to have two parts: HTTP SLASH VERSION
            raise HttpResponseBadRequest(content="Could not parse HTTP version")
        version = http[1].split(".")
        if len(version) != 2:
            # Make sure the VERSION part has a major and minor version
            raise HttpResponseBadRequest(content="Invalid HTTP version number")
        try:
            # And check that these values are numbers and not negative
            p1 = int(version[0])
            p2 = int(version[1])
            if p1 < 0 or p2 < 0:
                raise ValueError()
        except ValueError:
            raise HttpResponseBadRequest(content="Could not parse HTTP version number")

        for avail_version in HttpVersion:
            # HTTP version is case-sensitive, so we cannot either apply .upper()
            if str(avail_version) == http_version:
                http_version = avail_version
                break
        if isinstance(http_version, str):
            # If http_version is still a string, we do not support such version
            raise HttpResponseHttpVersionNotSupported(content="HTTP version {} is not available".format(http_version))
        self.__http_version = http_version

    def __init_parse_headers(self, lines):
        """
        Given a list of lines after removing the request-lines, parses lines which are headers.
        :param lines: list of lines to be checked
        :return: number of parsed headers
        """
        count = 0
        found_crlf = False
        for line in lines:
            # If line is "blank", it is because it CRLF, so end of headers
            if line == '':
                found_crlf = True
                break
            # Try to parse header with format ': SPACE'
            header = line.split(": ")
            if len(header) != 2:
                # Malformed header
                raise HttpResponseBadRequest(content="Header '{}' is not a valid header format".format(line))
            self.__headers[header[0].lower()] = HttpHeader(header[0], header[1])
            count += 1

        if not found_crlf:
            # We finished parsing headers, but make sure we found the CRLF regarding the last header
            # (the CRLF that ends the request will be checked in the next function)
            raise HttpResponseBadRequest(content="Could not find CRLF after headers parsing")
        return count

    def __init_parse_body(self, lines):
        """
        Function that given the remaining lines of the request, will check for the body if needed.
        :param lines: "body" part
        :return:
        """
        if not self.has_header(HEADER_CONTENT_LENGTH):
            # If no Content-Length header is present, it means that we can NOT receive any body. Thus, the remaining
            # lines has to be an empty one (the CRLF that ends the request)
            if len(lines) != 1 or lines[0] != '':
                raise HttpResponseBadRequest(content="Expecting no request body, but found")
            return

        # If Content-Length is present, we check if the length of the remaining data matches the specified
        # Content-Length value
        body = "\r\n".join(lines)
        actual_length = len(body)
        try:
            val = self.get_header(HEADER_CONTENT_LENGTH)
            if val is None:
                raise ValueError
            # If the value of the header is not an integer, then it is malformed
            expected_length = int(val.value)
        except ValueError:
            raise HttpResponseBadRequest(content="Could not parse Content-Length")

        if expected_length != actual_length:
            print(expected_length, actual_length)
            raise HttpResponseBadRequest(content="Request body differs from the specified Content-Length value")
        # And save the body data
        self.__body = body

    def get_method(self) -> HttpMethod:
        return self.__method

    def get_path(self) -> str:
        return self.__path

    def get_http_version(self) -> HttpVersion:
        return self.__http_version

    def get_headers(self) -> List[HttpHeader]:
        return list(self.__headers.values())

    def get_body(self) -> str | None:
        return self.__body

    def has_header(self, name):
        return name.lower() in self.__headers

    __contains__ = has_header

    def get_header(self, name: str) -> HttpHeader | None:
        if not self.has_header(name):
            return None
        return self.__headers[name.lower()]

    __getitem__ = get_header
