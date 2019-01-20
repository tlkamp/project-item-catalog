# Project: Item Catalog
The second project in the Fullstack Web Developer Nanodegree.

## Runtime Dependencies
* [Python 2.7](https://docs.python.org/2.7/) - the application runtime.
* [Flask](http://flask.pocoo.org/) - the web application framework.
* [sqlalchemy](https://www.sqlalchemy.org/) - the ORM library for the underlying database.
* [requests-oauthlib](https://requests-oauthlib.readthedocs.io/en/latest/) - for handling OAuth2 flows.
* [flask-login](https://flask-login.readthedocs.io/en/latest/) - for handling session management and protecting views.

### Dev Dependencies
* [pycodestyle](https://pycodestyle.readthedocs.io/en/latest/) - for checking code style practices.
* [autopep8](https://pypi.org/project/autopep8/) - for automatically fixing issues reported by `pycodestyle`.

## Running the App
1. Ensure the [fullstack-nanodegree-vm project](https://github.com/udacity/fullstack-nanodegree-vm) has been downloaded.
2. Ensure [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/) have been installed.
3. Clone or download this repository and copy the file contents to the `vagrant/catalog/` directory in the `fullstack-nanodegree-vm project` mentioned in step 1.
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
6. Do the database setup and run the application
    ```shell
    # setup the database
    $ python dbhelper.py

    # run the flask app
    $ python application.py
    ```
7. Navigate to [`http://localhost:8000/`](http://localhost:8000) in a browser.

To stop the application, go back to your vagrant session and hit `control + c`.
