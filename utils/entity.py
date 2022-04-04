from __future__ import annotations

import datetime
import locale

from http.enums import HttpVersion, HttpMethod
from http.header import HttpHeader, HEADER_DATE, HEADER_CONTENT_LENGTH
from http.request import HttpRequest
from http.response import HttpResponse


def generate_header_date(response: HttpResponse):
    """
    Given a response, appends the Date header.
    :param response: response object where the Date header will be added
    """
    # https://stackoverflow.com/a/225106
    locale.setlocale(locale.LC_TIME, 'en_US')
    header = HttpHeader(name=HEADER_DATE, value=datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    response[HEADER_DATE] = header


def generate_header_content_length(response: HttpResponse):
    """
    Given a response, appends the Content-Length header if needed
    :param response: response where the Content-Length header will be added
    """
    if response.get_content() is None:
        # If no content, we ignore this header
        return
    # Otherwise, get the size of the contents and append it as header
    header = HttpHeader(name=HEADER_CONTENT_LENGTH, value=str(len(response.get_content())))
    response[HEADER_CONTENT_LENGTH] = header


def generate_auto_headers(request: HttpRequest, response: HttpResponse):
    """
    Given a request and a response, add to the response object the "automatic" headers.
    :param request: original request from the client
    :param response: response object to be modified
    """
    # Server header is used in all methods
    # TODO: Server
    if request.get_method() == HttpMethod.GET:
        # We need Date, Content-Length and Content-Type
        generate_header_date(response)
        generate_header_content_length(response)
        # TODO: Content-Type
    elif request.get_method() == HttpMethod.PUT:
        # We need Content-Location
        # TODO: Content-Location
        pass
    elif request.get_method() == HttpMethod.DELETE:
        # We need Date
        generate_header_date(response)
    elif request.get_method() == HttpMethod.NTW22INFO:
        # We need Date, Content-Length and Content-Type
        generate_header_date(response)
        generate_header_content_length(response)
        # TODO: Content-Type


def generate_output(request: HttpRequest | None, response: HttpResponse) -> str:
    """
    Given a request object and a response, generates the corresponding HTTP responding as a string.
    :param request: original request from the client
    :param response: prepared response from the server
    :return: valid HTTP response string
    """
    if request:
        # If we receive a valid request, then try to generate the needed headers automatically
        generate_auto_headers(request, response)
    # Generate the response-line and append the response serialization (headers and body) afterwards
    return "{} {}\r\n{}".format(
        HttpVersion.HTTP_10 if not request else request.get_http_version(), response.get_status_code(),
        response.serialize()
    )
