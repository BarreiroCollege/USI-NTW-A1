# HTTP Server

**HTTP server running over TCP IPv4**

**Assignment 1** for **[Computer Networking](https://search.usi.ch/en/courses/35263648/computer-networking)**
course during the Spring Semester 2022 @ [USI Università della Svizzera italiana](https://www.usi.ch).

* Aristeidis Vrazitoulis: [vrazia@usi.ch](mailto:vrazia@usi.ch)
* Marina Papageorgiou: [papagm@usi.ch](mailto:papagm@usi.ch)
* Diego Barreiro Perez: [barred@usi.ch](mailto:barred@usi.ch)

## Usage Instructions

This code has been written in **`Python 3.9`**, so it is guaranteed that no errors will appear there.
However, lower Python versions may work properly.

### Installation

No specific installation instructions are required. Just install a **`Python 3`** version.

### Running

To get the server up and running, just run the following command:

```bash
python server.py
```

By default, it will be running at port `8080`, but it can be changed with the respective flag.
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

WIP: How job was split. We used git for project management with Github issues, branches and other
stuff as if it were a software engineering project.

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

### Project Structure

WIP: Websites folder, http module, utils and server and settings.

### HTTP Implementation

WIP: Object oriented programming, based on Django. HttpRequest and HttpResponse. Internal process workflow:
from getting raw socket data to sending raw socket data. Parsing and entity file (custom error content).

#### GET

Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
with a list of possible response codes, and their trigger case.
Additionally, mention we support all content types, and we also return 415 error.

#### PUT

Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
with a list of possible response codes, and their trigger case.

#### DELETE

Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
with a list of possible response codes, and their trigger case.
Mention as well the automatic deletion of folders.

#### NTW22INFO

Explain procedure regarding the implementation, logic behind it, assumptions taken, extra features, etc. Finish
with a list of possible response codes, and their trigger case.
Mention as well that we also support other paths apart from just /.

## Acknowledgments

- Django
- StackOverflow question about multithread
- RFC's
- TA notes
