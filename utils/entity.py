from __future__ import annotations

import datetime
import locale

from http.enums import HttpVersion, HttpMethod
from http.header import HttpHeader, HEADER_DATE, HEADER_CONTENT_LENGTH
from http.request import HttpRequest
from http.response import HttpResponse


def generate_header_date(response: HttpResponse):
    locale.setlocale(locale.LC_TIME, 'en_US')
    header = HttpHeader(name=HEADER_DATE, value=datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'))
    response[HEADER_DATE] = header


def generate_header_content_length(response: HttpResponse):
    length = len(response.get_content()) if response.get_content() is not None else 0
    header = HttpHeader(name=HEADER_CONTENT_LENGTH, value=str(length))
    response[HEADER_CONTENT_LENGTH] = header


def generate_auto_headers(request: HttpRequest, response: HttpResponse):
    # TODO: Server
    if request.get_method() == HttpMethod.GET:
        generate_header_date(response)
        generate_header_content_length(response)
        # TODO: Content-Type
    elif request.get_method() == HttpMethod.PUT:
        # TODO: Content-Location
        pass
    elif request.get_method() == HttpMethod.DELETE:
        generate_header_date(response)
    elif request.get_method() == HttpMethod.NTW22INFO:
        generate_header_date(response)
        generate_header_content_length(response)
        # TODO: Content-Type


def generate_output(request: HttpRequest | None, response: HttpResponse) -> str:
    if request:
        generate_auto_headers(request, response)
    return "{} {}\r\n{}\r\n".format(
        HttpVersion.HTTP_10 if not request else request.get_http_version(), response.get_status_code(),
        response.serialize()
    )
