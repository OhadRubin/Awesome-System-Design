[![Build Status](https://travis-ci.org/OhadRubin/Awesome-System-Design.svg?branch=master)](https://travis-ci.org/OhadRubin/Awesome-System-Design)
[![codecov](https://codecov.io/gh/OhadRubin/Awesome-System-Design/branch/master/graph/badge.svg)](https://codecov.io/gh/OhadRubin/Awesome-System-Design)
# Awesome System Design

An example package. See [full documentation](https://advanced-system-design-awesome-system-design.readthedocs.io/en/latest/).

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

- In order to run this project, make sure you have docker-compose installed and run run-pipeline.sh.


    ```sh
    $ ./scripts/run-pipeline.sh

    ```

## Notes
- We used 

to use the clinet run python -m asd.client upload-sample -h 127.0.0.1 --port 8000 ../sample.mind.gz