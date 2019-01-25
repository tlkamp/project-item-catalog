# Project: Item Catalog
The second project in the Fullstack Web Developer Nanodegree.

## Runtime Dependencies
* [Python 2.7](https://docs.python.org/2.7/) - the application runtime.
* [Flask](http://flask.pocoo.org/) - the web application framework.
* [sqlalchemy](https://www.sqlalchemy.org/) - the ORM library for the underlying database.
* [requests-oauthlib](https://requests-oauthlib.readthedocs.io/en/latest/) - for handling OAuth2 flows.
* [flask-login](https://flask-login.readthedocs.io/en/latest/) - for handling session management and protecting views.
* [psycopg2](http://initd.org/psycopg/) - the PostgreSQL DB API for Python.

### Dev Dependencies
* [pycodestyle](https://pycodestyle.readthedocs.io/en/latest/) - for checking code style practices.
* [autopep8](https://pypi.org/project/autopep8/) - for automatically fixing issues reported by `pycodestyle`.

## Deployment Details
The application is deployed at [www.tlkamp.com](https://www.tlkamp.com) using [nginx](https://www.nginx.com/) as a
reverse proxy to a [gunicorn](https://gunicorn.org/) `wsgi` application server enabled via `systemd`.

The database backend is [PosgreSQL](https://www.postgresql.org/).

HTTPS is enabled thanks to [LetsEncrypt](https://letsencrypt.org/).

## Running the App - Local
1. Ensure the [fullstack-nanodegree-vm project](https://github.com/udacity/fullstack-nanodegree-vm) has been downloaded.
2. Ensure [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/) have been installed.
3. Clone or download this repository and copy the file contents to the `vagrant/catalog/` directory in the `fullstack-nanodegree-vm project` mentioned in step 1. <br/><br/>
4. Bring up the vagrant machine and `ssh` into it.
   ```shell
    $ cd fullstack-nanodegree-vm/vagrant
    $ vagrant up
    $ vagrant ssh
    ```
5. Ensure all of the project dependencies are installed.
    ```shell
    $ cd /vagrant/catalog/
    $ sudo pip install -r requirements.txt
    ```
6. Create a file called `client_secrets.json` and paste the provided text into it. This file is required for GitHub (the OAuth2 provider) to verify this application. <br/><br/>
7. Do the database setup and run the application
    ```shell
    # setup the database
    $ python dbhelper.py

    # run the flask app
    $ python application.py
    ```
8. To stop the application, go back to your vagrant session and hit `control + c`.
  
## Interacting With the Application
If you are using the deployed version of the application, please substitute the references to `localhost:8000` with 
`https://tlkamp.com`.

Navigate to [`http://localhost:8000/`](http://localhost:8000) in a browser. To interact with the json endpoints, please use the following:
  * [`http://localhost:8000/catalog/json`](http://localhost:8000/catalog/json/) for a full catalog listing
  * [`http://localhost:8000/catalog/json/item/<item id number>`](http://localhost:8000/catalog/json/item/1) for informaiton about a specific database item.

**An item that does not exist**
```shell
$ curl -i http://localhost:8000/catalog/json/item/3
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 29
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Mon, 21 Jan 2019 01:05:02 GMT

{
  "message": "Not found"
}
```

**An individual item**
```shell
$ curl -i http://localhost:8000/catalog/json/item/2
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 209
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Mon, 21 Jan 2019 01:05:00 GMT

{
  "item": {
    "category": "Default",
    "description": "something with a later modified date",
    "id": 2,
    "last_updated": "2019-01-20 13:31",
    "name": "another default",
    "user": 1
  }
}
```

**The full catalog listing**
```shell
$ curl -i http://localhost:8000/catalog/json/
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 580
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Mon, 21 Jan 2019 01:05:06 GMT

{
  "categories": [
    {
      "id": 1,
      "items": [
        {
          "category": "Default",
          "description": "something to test with",
          "id": 1,
          "last_updated": "2019-01-20 13:31",
          "name": "default item",
          "user": 1
        },
        {
          "category": "Default",
          "description": "something with a later modified date",
          "id": 2,
          "last_updated": "2019-01-20 13:31",
          "name": "another default",
          "user": 1
        }
      ],
      "name": "Default"
    }
  ]
}
```
