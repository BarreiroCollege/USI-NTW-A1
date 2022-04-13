from __future__ import annotations

import datetime
import locale

from http.enums import HttpVersion, HttpMethod
from http.header import HttpHeader, HEADER_DATE, HEADER_CONTENT_LENGTH, HEADER_SERVER, HEADER_CONTENT_TYPE, \
    HEADER_CONTENT_TYPE_TEXT_HTML, HEADER_CONTENT_TYPE_TEXT_PLAIN
from http.request import HttpRequest
from http.response import HttpResponse, HttpResponseError
from settings import HTTP_ENCODING, SERVER_NAME
from utils.vhosts import Vhost


def generate_error_response_content(request: HttpRequest, response: HttpResponse):
    """
    If the specified request method is GET and the response is an error, try to insert the "CODE.html" file
    as response content, if exist. Otherwise, just proceed with the reason.
    :param request: HttpRequest object
    :param response: HttpResponse object
    """
    # Only applies to GET method
    if request.get_method() != HttpMethod.GET:
        return
    # And only applies to error responses
    if not isinstance(response, HttpResponseError):
        return

    # If already specified some content, ignore
    if response.get_content() is not None:
        return

    # Search for CODE.html file and, if exists and is file, put such contents as response
    error_file_path = request.get_vhost().get_host_root_path().joinpath(
        "{}.html".format(str(response.get_status_code().get_code()))
    )
    if error_file_path.exists() and error_file_path.is_file():
        content = Vhost.get_file_contents(error_file_path)
        content_type_header = HttpHeader(HEADER_CONTENT_TYPE, HEADER_CONTENT_TYPE_TEXT_HTML)
    else:
        content = response.get_status_code().get_reason()
        content_type_header = HttpHeader(HEADER_CONTENT_TYPE, HEADER_CONTENT_TYPE_TEXT_PLAIN)

    # Update the response content and Content-Type header
    response.set_content(content)
    response[HEADER_CONTENT_TYPE] = content_type_header


def generate_header_server(response: HttpResponse):
    """
    Given a response, appends the Server header.
    :param response: response object where the Server header will be added
    """
    header = HttpHeader(HEADER_SERVER, SERVER_NAME)
    response[HEADER_SERVER] = header


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
    v = response.get_content()
    if isinstance(response.get_content(), str):
        v = response.get_content().encode(HTTP_ENCODING)
    header = HttpHeader(name=HEADER_CONTENT_LENGTH, value=str(len(v)))
    response[HEADER_CONTENT_LENGTH] = header


def generate_auto_headers(request: HttpRequest, response: HttpResponse):
    """
    Given a request and a response, add to the response object the "automatic" headers.
    :param request: original request from the client
    :param response: response object to be modified
    """
    # Server header is used in all methods
    generate_header_server(response)
    if request.get_method() == HttpMethod.GET:
        # We need Date, Content-Length and Content-Type
        generate_header_date(response)
        generate_header_content_length(response)
        # Content-Type is generated at server.py
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
        # Content-Type is generated at server.py


def generate_output(request: HttpRequest | None, response: HttpResponse) -> bytes:
    """
    Given a request object and a response, generates the corresponding HTTP responding as a string.
    :param request: original request from the client
    :param response: prepared response from the server
    :return: valid HTTP response string
    """
    if request:
        # Check if the specified response is an error and, if is, try to inject the output
        generate_error_response_content(request, response)
        # If we receive a valid request, then try to generate the needed headers automatically
        generate_auto_headers(request, response)
    # Generate the response-line and append the response serialization (headers and body) afterwards
    return "{} {}\r\n".format(HttpVersion.HTTP_10 if not request else request.get_http_version(),
                              response.get_status_code()).encode(HTTP_ENCODING) + bytes(response)
