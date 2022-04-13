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
project. We used **Issues** to keep track of the pending tasks, bugs found, etc.; we set up a **Milestone** to view
the deadline and the progress done, and **Pull Requests** to independtly work on different branches to avoid breaking
or overwriting code.

For example, the **Issues** page looks like this right now after filtering for the specific tasks:

![](https://i.imgur.com/YJgBrxT.png)

### Project Structure

NOTE: _All the project has been created following an object-oriented pattern to ease operations. Some of these classes
override basic Python operations (like `__bytes__` or `__setitem__`), so code can be written clearer._

As required, **`server.py` file is the entry point**. It is actually the only executable file (the rest Python files
are just modules, and will not run anything unless invoked from a different file). Thus, such file must be run as a
Python script (and will not do anything if imported from a module). This file has the `Server` class, which actually
keeps the server socket alive and parses the `Vhost` file (one object per virtual host). It will start listening for
connections and, **for each connection, will process it in a new thread**.

The `settings.py` file defines some constants for the server, like the default running port (`8080`), the encoding
(`utf-8`) to keep all request uniform, the **server name (`Group AMD Server`)** and the virtual hosts file
(`vhost.confs`).

Task B websites are available in the respective folders (`arisvrazitoulis.ch`, `marina.ch`, `diegobarreiro.es`), as
well as the virtual hosts file (`vhosts.conf`).

The **`http` module** takes care of creating the response and request objects. **`HttpRequest` class will be constructed
from a raw HTTP request**, containing all the data inside the respective attributes. And then **`HttpResponse` will
contain all the data** for the output response, which can be **serialized into a raw HTTP response** (in this case,
some subclasses have been defined for the error codes to ease its usage). `enums.py` file contains several available
constants, like **`HttpMethod`**, **`HttpResponseCode`** and **`HttpVersion`** (which are used in the request and
response objects). And it has been defined a **`HttpHeader` class as a key-value standarized header**.

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

WIP: Object oriented programming, based on Django. HttpRequest and HttpResponse. Internal process workflow:
from getting raw socket data to sending raw socket data. Parsing and entity file (custom error content).

#### GET

Since Server receives the request and checks its structure for basic validity,
then proceeds for further checking. After inspecting the first line of the request
and ensures that is a GET method then we check for the file path existence in the server's
filesystem. If the requested file exists then we append its content to the body of the HTTP response
and add the required headers to the HTTP response and 200 as status code. In every other case, we raise the corresponding exception with the corresponding status code and we attach that in the HTTP response.

More specifically:
-If file does not exist: 404 NOT FOUND
In that case we make a special response with a body of the contents of the file 404.html 

-If user does not have permission to access the file: 403 FORBIDDEN
-If the requested resource is not a file: 405 METHOD NOT ALLOWED
#  If the file is   UnsupportedMediaType??



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
In this method (NTW22INFO) the client is giving as an input: 
                                      "NTW22INFO / HTTP/1.0
                                      Host: gyuincognito.ch"

The server answers automatically: "HTTP/1.0 200 OK
                                      Date: Wed, 24 Mar 2021 09:30:00 GMT
                                      Server: Guy incognito's Server
                                      Content-Length: 98
                                      Content-Type: text/plain"   
So my job is to write up to this input and the automatic server's answer the following answer: 
                                      "The administrator of guyncognito.ch is Guy incognito.
                                      The on contact him at guy.incognito@usi.ch"                                

// Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
// with a list of possible response codes, and their trigger case.
// Mention as well that we also support other paths apart from just /.

## Acknowledgments

- Django
- StackOverflow question about multithread
- RFC's
- TA notes
