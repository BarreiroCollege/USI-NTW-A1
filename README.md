# HTTP Server

**HTTP server running over TCP IPv4**

**Assignment 1** for **[Computer Networking](https://search.usi.ch/en/courses/35263648/computer-networking)**
course during the Spring Semester 2022 @ [USI Università della Svizzera italiana](https://www.usi.ch).

* Aristeidis Vrazitoulis: [vrazia@usi.ch](mailto:vrazia@usi.ch)  
  _Task B Website: [`arisvrazitoulis.ch`](http://arisvrazitoulis.ch:8080)_
* Marina Papageorgiou: [papagm@usi.ch](mailto:papagm@usi.ch)  
  _Task B Website: [`marina.ch`](http://marina.ch:8080)_
* Diego Barreiro Perez: [barred@usi.ch](mailto:barred@usi.ch)  
  _Task B Website: [`diegobarreiro.es`](http://diegobarreiro.es:8080)_

## Usage Instructions

This code has been written in **`Python 3.9`**, so it is guaranteed that no errors will appear there. However, lower
Python versions may work properly.

### Installation

No specific installation instructions are required. Just install a **`Python 3`** version.

### Running

To get the server up and running, just run the following command:

```bash
python server.py
```

By default, it will be running at port `8080`, but it can be changed with the `--port` flag.  
All options are listed here:

```bash
PS C:\Github\NTW22-1> python server.py --help
usage: server.py [-h] [-p [PORT]]

HTTP server based on TCP IPv4 with multithreading support.

optional arguments:
  -h, --help            show this help message and exit
  -p [PORT], --port [PORT]
                        port to use to listen connections
PS C:\Github\NTW22-1>
```

## Tasks

This assignment was divided into several tasks. Each member of the group worked on different tasks as stated in the
table below. As it can be seen, multiple members have worked on the same task.

|                    | **Aristeidis** | **Marina** | **Diego** |
|:-------------------|:--------------:|:----------:|:---------:|
| Task A             |                |            |     ●     |
| Task B             |       ●        |     ●      |     ●     |
| Task C             |       ●        |            |           |
| Task D             |                |     ●      |           |
| Task E             |       ●        |            |           |
| Task F             |                |     ●      |           |
| Task G             |       ●        |     ●      |           |
| Task H             |                |            |     ●     |
| Task I             |       ●        |     ●      |     ●     |
| Task J             |       ●        |     ●      |     ●     |
| _Optional Task A_  |                |            |     ●     |
| _Optional Task B_  |                |            |     ●     |

Thus, to properly manage the project, we have used **Github** and their features to manage it as a "big" software
project. We used **Issues** to keep track of the pending tasks, bugs found, etc.; we set up a **Milestone** to view the
deadline and the progress done, and **Pull Requests** to independtly work on different branches to avoid breaking or
overwriting code.

For example, the **Issues** page looks like this right now after filtering for the specific tasks:

![](https://i.imgur.com/YJgBrxT.png)

### Project Structure

_All the project has been created following an object-oriented pattern to ease operations. Some of these classes
override basic Python operations (like `__bytes__` or `__setitem__`), so code can be written clearer._

As required, **`server.py` file is the entry point**. It is actually the only executable file (the rest Python files are
just modules, and will not run anything unless invoked from a different file). Thus, such file must be run as a Python
script (and will not do anything if imported from a module). This file has the `Server` class, which actually keeps the
server socket alive and parses the `Vhost` file (one object per virtual host). It will start listening for connections
and, **for each connection, will process it in a new thread**.

The `settings.py` file defines some constants for the server, like the default running port (`8080`), the encoding
(`utf-8`) to keep all request uniform, the **server name (`Group AMD Server`)** and the virtual hosts file
(`vhost.confs`).

Task B websites are available in the respective folders (`arisvrazitoulis.ch`, `marina.ch`, `diegobarreiro.es`), as well
as the virtual hosts file (`vhosts.conf`).

The **`http` module** takes care of creating the response and request objects. **`HttpRequest` class will be constructed
from a raw HTTP request**, containing all the data inside the respective attributes. And then **`HttpResponse` will
contain all the data** for the output response, which can be **serialized into a raw HTTP response** (in this case, some
subclasses have been defined for the error codes to ease its usage which extend `Exception`, allowing to be raised and
later caught by the `Server` to be sent as "valid" responses). `enums.py` file contains several available constants,
like **`HttpMethod`**, **`HttpResponseCode`** and **`HttpVersion`** (which are used in the request and response objects)
. And it has been defined a **`HttpHeader` class as a key-value standarized header**.

And finally, the **`utils` module** takes care of other minor tasks. **`entity.py`** file will generate the raw HTTP
response from both request and response (from an OOP perspective, response could receive the request, but it would
create a dependency between these objects which, in theory, are independent, as the response object "only" varies in
status code, headers and body), and it will also inject some auto independent headers like `Content-Length` or `Date`.
The `mime.py` file defines some custom MIME types for the `GET` method (_this is explained later_). And finally the
**`vhosts.py`** file which contains the `Vhost` class with the attributes of a virtual host.

```txt
NTW22-1
├── README.md
├── arisvrazitoulis.ch
│   ├── giannena.jpeg
│   ├── index.html
│   └── me.jpg
├── diegobarreiro.es
│   ├── 404.html
│   ├── about.html
│   ├── assets
│   │   ├── css
│   │   │   └── features.css
│   │   ├── img
│   │   │   ├── etse.jpg
│   │   │   ├── home.jpg
│   │   │   ├── ies1.jpg
│   │   │   ├── ies2.jpg
│   │   │   ├── ies3.jpg
│   │   │   ├── mit1.jpg
│   │   │   ├── mit2.jpg
│   │   │   ├── pc1.png
│   │   │   └── pc2.jpg
│   │   ├── js
│   │   ├── vendor
│   │   │   ├── bootstrap-5.1.3
│   │   │   └── bootstrap-icons-1.8.1
│   │   └── video
│   │       └── kodular.mp4
│   ├── contact.html
│   ├── edu.html
│   ├── favicon.ico
│   └── work.html
├── guyincognito.ch
│   ├── home.html
│   ├── images
│   │   ├── avatar.png
│   │   ├── paddlin.png
│   │   ├── pglit2.gif
│   │   └── under_construction.gif
│   └── test
├── http
│   ├── enums.py
│   ├── header.py
│   ├── request.py
│   └── response.py
├── marina.ch
│   ├── images
│   │   ├── 1.jpeg
│   │   ├── 2.jpeg
│   │   └── 3.jpeg
│   ├── index.html
│   └── style.css
├── server.py
├── settings.py
├── utils
│   ├── entity.py
│   ├── mime.py
│   └── vhosts.py
└── vhosts.conf
```

### HTTP Implementation

The first step of the HTTP process is **generating the `HttpRequest` object**. Upon receiving a new connection, `Server`
will launch a new thread to start processing this new request (such thread will keep listening for connections in
`HTTP/1.1` if `Connection: Close` is not present). This new thread will call the constructor for `HttpRequest`, sending
the raw bytes in the socket. The constructor will try to parse this HTTP request, considering the breakline as `CRLF`.
If no errors are found, the `HttpRequest` object will be created. The following errors may be triggered (in the
specified priority), and will raise the corresponding error breaking the procedure and returning the HTTP response
earlier:

| **Status Code** | **Class**                             | **Reason**                                          |
|:---------------:|:--------------------------------------|:----------------------------------------------------|
|     **501**     | `HttpResponseNotImplemented`          | Specified request method is not implemented         |
|     **505**     | `HttpResponseHttpVersionNotSupported` | Not `HTTP/1.0` or `HTTP/1.1`                        |
|     **403**     | `HttpResponseForbidden`               | Specified path is outside of the virtual host scope |
|     **404**     | `HttpResponseNotFound`                | Specified host is not available in the server       |
|     **400**     | `HttpResponseBadRequest`              | Error parsing the request (_malformed data_)        |

Once the `HttpRequest` object is generated, the next step is generating the appropiate response for such request. So,
back into the **`Server` object**, it **will generate the `HttpResponse` object for such request**. Depending on the
method, different code is executed, so _this part is better explained in the sections below for each method_. Keep in
mind that some errors can appear when generating the response as well, so a similar table as the one above will be
present for each method.

And finally, now that both `HttpRequest` and `HttpResponse` objects are created, **they are ready to be "merged" into
the raw output** for the socket to be sent to the client. Thus, `entity.py` will receive both objects and start
generating this string, and will also **inject some "auto" headers into the response object**. These headers include
`Date` or `Server`, for example. The return data is the **actual string encoded in bytes** that has to be sent back to
the client as response.

Additionally, a **custom error page feature has been implemented**. In the root of a virtual host folder, files named
`CODE.html` can be created, where `CODE` is an `HTTP` error code. When `entity.py` detects that response is an error
response, if no content is specified and `GET` method has been requested, it will **try to search for such file and put
it as response content**. This is pretty useful for cases like designing custom not found pages, or other error pages.

#### GET

The first step is to check if the provided path is a folder or not. As a `Vhost` specifies an index file, **if the user
tries to access a folder, they are in fact trying to access to the index file of such folder**. So, it has to be
appended.

The next steps is to check if the specified file exists in the filesystem. `Vhost` already provides a method to get the
`Path` of the root for its files, so the **request path has to be appended to this path**. Once done, the file can be
checked if it **exists or not in the filesystem**. And, if it exists, check that **is not a folder**.

Finally, we can try to **open the file** (assuming we have permission to do so), and **get its contents in bytes**. Now
the **`HttpResponse` object gets constructed, with the specified content**. However, before it becomes a valid response,
the MIME type of such file has to be checked. `Server` will try to guess its type using the standard `mimetypes`
library and, if it cannot get resolved with either the library or the custom ones, an error will be raised.

The list of error responses that this method can return are the following ones (with the given priority):

| **Status Code** | **Class**                          | **Reason**                                                 |
|:---------------:|:-----------------------------------|:-----------------------------------------------------------|
|     **404**     | `HttpResponseNotFound`             | Specified file (or folder) does not exist                  |
|     **405**     | `HttpResponseMethodNotAllowed`     | Specified "file" path is a folder in the filesystem        |
|     **403**     | `HttpResponseForbidden`            | Cannot read file contents (missing filesystem permissions) |
|     **415**     | `HttpResponseUnsupportedMediaType` | File exists but its MIME type cannot be guessed            |

If no error appears, **`HttpResponse` will have code `200 OK` and as body the contents of such file**.

#### PUT
In the PUT method the user gives a path as an input. Then it is happening a check with try - exception with the following conditions:
- if the input path contains at the end "/", it means that is not a file but it is a directory, so it prints the error 405 (HttpMethodNotAllowed)
- If the input path exists then the server opens the file of that path and writes in it. 
- If the input path does not exist then the server creats this path and this file and additionally, it prints the error 403     (HttpResponseForbidden).

// Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
// with a list of possible response codes, and their trigger case.

#### DELETE

For the HTTP DELETE method we check first for the file existence. If the file exists then we delete it from the file system
and then check if the folder is empty to remove it as well. Then we recursively check if the parent is empty so as to delete it.
After this procedure, we return a response with the suitable headers and status code 200 OK. Otherwise we raise an exception

-If file does not exist: 404 NOT FOUND
-If user does not have permission to access the file: 403 FORBIDDEN
-If the requested resource is not a file: 405 METHOD NOT ALLOWED


#### NTW22INFO

This method generates a **static response**. It does not really depend on the request: output is always a constant.
Thus, for all paths, a request would look like the following one:

```http request
NTW22INFO / HTTP/1.0
Host: gyuincognito.ch
```

And the response will look like this:

```http response
HTTP/1.0 200 OK
Date: Wed, 24 Mar 2021 09:30:00 GMT
Server: Guy incognito's Server
Content-Length: 98
Content-Type: text/plain

The administator of guyncognito.ch is Guy incognito.
You can contact him at guy.incognito@usi.ch.
```

The only variables are in the content of the response, which **depends on the virtual host** the user is trying to
access. It is not possible to get an error in this method.

## Acknowledgments

- Lecture Notes _by Professor Silvia Santini_
- Assignment Description _by Matias Laporte_
- [RFC1945](https://datatracker.ietf.org/doc/html/rfc1945) - HTTP/1.0
- [RFC2616](https://datatracker.ietf.org/doc/html/rfc2616) - HTTP/1.1
- [Multithread Socket Server - Stack Overflow](https://stackoverflow.com/a/23828265)
- [Django Project](https://www.djangoproject.com/)
