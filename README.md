# Grunge Rock Development Application

## Overview

This Django project implements a catalogue of Grunge rock music.  It has a fully-functional Django admin interface, and a read-only REST API.  It contains three related data models:

1. `Artist`
2. `Album`
3. `Track`

If you are applying for a Full Stack role, your submission should satisfy the Full Stack Candidate goals.
Otherwise, your submission should satisfy the Backend Candidate goals.

## Backend Candidate Goals

* Implement the ability to fetch, create, update, and delete playlists through the REST API.  A playlist should have a `uuid`, a `name`, and contain 0 or more tracks from this catalogue.  The tracks should be orderable in the playlist.
* Implement the test cases in `tests/test_playlists.py`.  The goal is to have no skipped or failing tests.
* Update the Django admin with the ability to browse and manage playlists.

## Fullstack Candidate Goals

* Implement the ability to fetch, create, update, and delete playlists using Django views and templates.  A playlist should have a `uuid`, a `name`, and contain 0 or more tracks from this catalogue.  The tracks should be orderable in the playlist.
* Update the Django admin with the ability to browse and manage playlists.

## Developing

You can check your work at any time by running:

```shell
$ make ready
```

This will run the default code linters and the test suite.  You can format your code to what the linters expect with:

```shell
$ make format
```

Please ensure that there are no code format or lint errors.

## Getting started

#### Create an account

Create an account at [https://code.livelike.com/user/sign_up](https://code.livelike.com/user/sign_up)

#### Fork this repository

When you have completed the goals then you can open a Pull Request to this main repository.

### Set up a virtualenv

```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

### Install dependencies

```shell
$ pip install --upgrade pip wheel
$ pip install --requirement=requirements.txt
```

### Initialize the development database

```shell
$ python manage.py migrate
$ python manage.py loaddata initial_data
```

### Add a development superuser

```shell
$ python manage.py createsuperuser
```

### Run the development server

```shell
$ python manage.py runserver
```

Log into the Django admin with your superuser account at:

[http://localhost:8000/admin/](http://localhost:8000/admin/)

Browse the REST API at:

[http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).
