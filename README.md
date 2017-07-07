# anchorage-shortcut #

A flexible Wagtail app to make it easy to build roadmaps to employment.

## Features ##


## Quickstart ##

First clone or fork the repository

cd to your project and install the dependences

    pip install -r requirements.txt

If you need a database, edit the settings and create the Wagtail migrations

    python manage.py makemigrations

Apply the migrations you just made

    python manage.py migrate

Once everything it's setup you can run the development server: [http://localhost:8000/](http://localhost:8000/)

    python manage.py runserver

## How to use it ##

There are three basic templates you can create to make this "roadmap"

### Roadmap ###
The parent template -- a roadmap has a list of multiple "task lists" that need to be completed.
Example: a roadmap for a recent immigrant

### Task list ###
A task list has a singular focus that might require multiple steps to complete.
Example: a task list for "Identification" that outlines steps to getting IDs for I-9 eligibility

### Step page ###
Steps pages are the "leaves" of this Wagtail app tree -- each task list has multiple steps with information.
Example: a step page for how to obtain your Birth certificate