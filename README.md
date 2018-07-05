# Note Taking API
A basic Python Flask-based note-taking API. Supports CRUD operations via a RESTful API for manipulating basic note objects.

** Installation **

Run all instructions from within the note-taking repository root folder.

Runs on Python 2.7, installation guide [found here](http://docs.python-guide.org/en/latest/starting/install/osx/#install-osx).

If `pip` is not installed, first ensure you have [easy_install](https://setuptools.readthedocs.io/en/latest/easy_install.html#installing-easy-install) installed and then install with:

```sudo easy_install pip```

Once you have `pip`, the only dependency required is Flask:

```sudo pip install flask```

** Running **

Once you have all dependencies installed, the server can be run with:

```FLASK_APP=server.py flask run```

This will bind the web server to port 5000 locally.

** Troubleshooting **

```socket.error: [Errno 48] Address already in use```
Ensure you do not have any other application running on port 5000, then try starting the server again


## REST API

A note object looks like the following:

```
  {
    "id": 1,
    "title": "Test Note",
    "body": "This is a test note object that will be available by default",
    "created_at": "2018-07-05 14:22:49.491376",
    "created_by": "admin",
    "edit_history": [
      {
        "edited_at": "2018-07-05 14:22:49.491390",
        "edited_by": "A User"
      }
    ],
  }
```

`GET /notes`
Returns all notes

*Returns*:
array of note objects

`GET /notes/:id`
Returns a single note given its numeric id

*Args*:
id:int

*Returns*:
note object

`POST /notes`
Adds a new note, assigning it a new auto-incremented id and
created\_at field with the current timestamp. A new note also
has an empty edit\_history list. The new note is returned.

*Args*:
note:dict
    created\_by:string (required)
    title:string
    body:string

*Returns*:
note object

`POST /notes/:id`
For a given note id and dict of changes, updates the note with the changes
and updates the edit history to contain the user who made the change and the
current time.

*Args*:
id:int
update:dict
    edited\_by:string (required)
    title:string
    body:string

*Returns*:
note object

`DELETE /notes/:id`
Removes the note for the given id and returns True if removed,
False if the note was not removed or it did not exist in the first place.

*Args*:
id:int

*Returns*:
boolean

