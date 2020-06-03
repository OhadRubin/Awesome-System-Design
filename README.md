[![Build Status](https://travis-ci.org/OhadRubin/Awesome-System-Design.svg?branch=master)](https://travis-ci.org/OhadRubin/Awesome-System-Design)
[![codecov](https://codecov.io/gh/OhadRubin/Awesome-System-Design/branch/master/graph/badge.svg)](https://codecov.io/gh/OhadRubin/Awesome-System-Design)
# Awesome System Design
- [Awesome System Design](#awesome-system-design)
  - [Installation](#installation)
  - [Usage](#usage)
- [Client module](#client-module)
  - [Usage](#usage-1)
  - [Notes](#notes)
- [Server module](#server-module)
  - [Usage](#usage-2)
  - [Notes](#notes-1)
- [Parsers module](#parsers-module)
  - [Usage](#usage-3)
    - [How to add a new parser](#how-to-add-a-new-parser)
- [Saver module](#saver-module)
  - [Usage](#usage-4)
  - [Notes](#notes-2)
- [API module](#api-module)
  - [Usage](#usage-5)
  - [Notes](#notes-3)
- [CLI module](#cli-module)
  - [Usage](#usage-6)
- [GUI module](#gui-module)
  - [Usage](#usage-7)
  - [Notes](#notes-4)


## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:OhadRubin/awesome-system-design.git
    ...
    $ cd awesome-system-design/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [awesome-system-design] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

- In order to run this project, make sure you have docker-compose installed and run:


    ```sh
    $ ./scripts/run-pipeline.sh

    ```


# Client module 

## Usage
- To use the client via the command line run 
    ```sh
        $ python -m asd.client upload-sample -h 127.0.0.1 --port 8000 ../sample.mind.gz
    ```
- To use it via python:
    ```python
        >>> from asd.client import upload_sample
        >>> upload_sample(host='127.0.0.1', port=8000, path='../sample.mind.gz')
        
    ```

## Notes
- Our protocol is implemented in the client as a get request to let the server know which fields the client has, where the server returns the available parsers, 
- This is followed by a post request by the client to send the Snapshot.
- We added to the protobuf file another class called Packet, which we use the combine the user and the snapshot and send it using our protocol. 


# Server module  

## Usage
- To use via python
    ```python
        >>> from asd.server import run_server
        >>> def print_message(message):
        ...     print(message)
        >>> run_server(host='127.0.0.1', port=8000, publish=print_message)
        # listen on host:port and pass received messages to publish

    ```

- To use via cli
    ```sh
    $ python -m asd.server run-server \
        -h/--host '127.0.0.1'          \
        -p/--port 8000                 \
        'rabbitmq://127.0.0.1:5672/'
    ```
## Notes
- We used flask_restful to implement the RESTful interface.
# Parsers module 

## Usage 
- To use with python:
    ```python
    >>> from asd.parsers import run_parser
    >>> data = ...
    >>> result = run_parser('pose', data)

    ```

- To use with the cli:
    ```sh
    $ python -m cortex.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
    ```
    - This interace accepts a parser name and a path to some raw data, as consumed from the  message queue, and prints the result, as published to the message queue (optionally redirecting it to a file.
- Note that we only accept .raw files,

### How to add a new parser
The parser file must contain either of the following:
1. A class with a method `parse` with the signature (self, context, snapshot)
2.  A method that begins with `parse_`, for example `parse_feelings` and has the signature (context, snapshot). 
    - For example: [feelings.py ](asd/parsers/feelings.py)
    

    Either way, it should return a dict, the keys for the dict will be the values that will be saved via the saver.


# Saver module 

## Usage
- To use with python:
    ```python
    >>> from asd.saver import Saver
    >>> saver = Saver(database_url)
    >>> data = …
    >>> saver.save('pose', data)
    ```
- To save a result with the cli:    
    ```sh
    python -m asd.saver save                     \
        -d/--database 'sqlite:///./data/asd.sqlite' \
        'pose'                                       \
        'pose.result' 

    ```
- To run the saver using the cli:
    ```sh
    python -m asd.saver run-saver  "sqlite:///./data/asd.sqlite"  'rabbitmq://127.0.0.1:5672'
    ```
## Notes
- We choose to use sqlite as the backend because of the nice integration with sqlalchamy.

# API module 

## Usage
- To use with python:
    ```python
    >>> from asd.api import run_api_server
    >>> run_api_server(
    ...     host = '127.0.0.1',
    ...     port = 5000,
    ...     database_url = 'sqlite:///./data/asd.sqlite',
    ... )
    … # listen on host:port and serve data from database_url
    ```
- To use with the cli:
    ```sh
    $ python -m asd.api run-server \
        -h/--host '127.0.0.1'       \
        -p/--port 5000              \
        -d/--database 'sqlite:///./data/asd.sqlite'
    ```
## Notes
- We used flask_restful to implement the RESTful interface.


# CLI module 

## Usage
```sh
$ python -m asd.cli get-users
…
$ python -m asd.cli get-user 1
…
$ python -m asd.cli get-snapshots 1
…
$ python -m asd.cli get-snapshot 1 2
…
$ python -m asd.cli get-result 1 2 'pose'
```

# GUI module 

## Usage
- Using python:
    ```python
    >>> from asd.gui import run_server
    >>> run_server(
    ...     host = '127.0.0.1',
    ...     port = 8080,
    ...     api_host = '127.0.0.1',
    ...     api_port = 5000,
    ... )
    ```
- Using the cli:
    ```sh
    $ python -m asd.gui run-server \
        -h/--host '127.0.0.1'       \
        -p/--port 8080              \
        -H/--api-host '127.0.0.1'   \
        -P/--api-port 5000
    ```
## Notes
- We used flask
- For the gui, we implemented a infinite scrolling view.
