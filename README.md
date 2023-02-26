### Hexlet tests and linter status:
[![Actions Status](https://github.com/georf1/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/georf1/python-project-83/actions)
[![Linter check](https://github.com/georf1/python-project-83/actions/workflows/lint.yml/badge.svg)](https://github.com/georf1/python-project-83/actions/workflows/lint.yml)

---

### Description:
Page Analyzer is a web application that allows you to analyze sites for SEO suitability

### Dependencies:
This project was built using these tools:

| Tool                                                  | Version         | Description                                                         |
|-------------------------------------------------------|-----------------|---------------------------------------------------------------------|
| [poetry](https://poetry.eustace.io)                   | "^1.2.2"        | "Python dependency management and packaging made easy"              |
| [flask](https://flask.palletsprojects.com)            | "^2.2.2"        | "Micro web framework written in Python"                             |
| [gunicorn](https://gunicorn.org)                      | "^20.1.0"       | "Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX"    |
| [requests](https://requests.readthedocs.io)           | "^2.28.2"       | "Elegant and simple HTTP library for Python"                        |
| [bs4](https://www.crummy.com/software/BeautifulSoup)  | "^0.0.1"        | "Python library for pulling data out of HTML and XML files"         |
| [psycopg2](https://www.psycopg.org)                   | "^2.9.5"        | "Most popular PostgreSQL adapter for Python"                        |
| [validators](https://validators.readthedocs.io)       | "^0.20.0"       | "Python data validation"                                            |
| [flake8](https://flake8.pycqa.org)                    | "^6.0.0"        | "Tool for style guide enforcement"                                  |

### Commands:
Install:
> make install
>
> add a .env file like example.env
>
> remove example.env

To start with gunicorn use:
> make start

To start in dev mode use:
> make dev

### Demonstration:
You can check the functionality of the project by clicking on this link - https://python-project-83-production-2732.up.railway.app
