Fyyur
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

TRY IT NOW! https://fyyur-musical-performance.herokuapp.com

All backend code base follows [PEP8 style guidelines.](https://www.python.org/dev/peps/pep-0008)

### Overview

Main functionality of fyyur application:

* creating new venues, artists, and creating new shows
* editing/deleting existing venues and artist
* searching for venues and artists
* learning more about a specific artist or venue

### Tech Stack

* **SQLAlchemy ORM** to be ORM library of choice
* **PostgreSQL** as database of choice
* **Python3** and **Flask** as server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes Flask Controllers and Endpoints
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── forms.py *** Frontedn forms
  ├── fabfile.py *** Setup and commands for Heroku server
  ├── manage.py *** DB migration manager
  ├── models.py *** SQLAlchemy models
  ├── utils.py *** Utility functions and helpers like date formatter etc.
  ├── requirements.txt *** The dependencies we need to install
  ├── migrations *** Flask-Migration and alembic migration config and versions
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `MODELS` section of `app.py`.
* Controllers are also located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`

### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ python3 -m venv venv
  $ source venv/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip3 install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

## Roadmap

Future TODOs:
* Add a live demo
* ~~Deploy application on Heroku~~
* Add unit tests
* Implement artist availability. An artist can list available times that they can be booked. Restrict venues from being able to create shows with artists during a show time that is outside of their availability.
* Show Recent Listed Artists and Recently Listed Venues on the homepage, returning results for Artists and Venues sorting by newly created. Limit to the 10 most recently listed items.
* Implement Search Artists by City and State, and Search Venues by City and State. Searching by "San Francisco, CA" should return all artists or venues in San Francisco, CA.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate and follow the PEP8 style guide.

## License

The content of this repository is licensed under a [MIT License.](https://github.com/jurayev/fyyur/blob/master/LICENSE.md)
