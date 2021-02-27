from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

""" Rough code to let us store notes in memory with out any DB complexity"""
notes = {
    1: {
        'id': 1,
        'title': 'Test Note',
        'body': 'This is a test note object that will be available by default',
        'created_at': str(datetime.now()),
        'created_by': 'admin',
        'edit_history': [{
            'edited_at': str(datetime.now()),
            'edited_by': 'A User',
        }],
    },
}


def get_notes():
    """"
    Return all notes
    """
    global notes
    return notes


def get_note(id):
    """
    Returns a single note given its numeric id

    Args:
    id:int

    Returns:
    dict
    """
    return get_notes().get(id, None)


def update_note(id, update):
    """
    For a given note id and dict of changes, updates the note with the changes
    and updates the edit history to contain the user who made the change and the
    current time.

    Args:
    id:int
    update:dict
        edited_by:string
        title:string
        body:string

    Returns:
    dict
    """
    note = get_note(id)

    editor = None
    if update.get('edited_by'):
        editor = update.pop('edited_by')

    note.update(update)
    if editor:
        note['edit_history'].append({
            'edited_by': editor,
            'edited_at': str(datetime.now()),
        })
    return note


def remove_note(id):
    """
    Removes the note for the given id and returns True if removed,
    False if the note was not removed or it did not exist in the first place.

    Args:
    id:int

    Returns:
    bool
    """
    return get_notes().pop(id, False) is not False


def add_note(note):
    """
    Adds a new note, assigning it a new auto-incremented id and
    created_at field with the current timestamp. A new note also
    has an empty edit_history list. The new note is returned.

    Args:
    note:dict
        created_by:string
        title:string
        body:string

    Returns:
    dict
    """
    notes = get_notes()
    new_id = int(max(notes.keys())) + 1
    get_notes()[new_id] = note
    note['id'] = new_id
    note['created_at'] = str(datetime.now())
    note['edit_history'] = []
    return note


"""The public routes for manipulating notes"""


@app.route('/notes')
def get_all_notes():
    return jsonify(list(get_notes().values()))


@app.route('/notes/<int:id>')
def get_one_note(id):
    return jsonify(get_note(id))


@app.route('/notes', methods=['POST'])
def create_note():
    body = request.get_json()
    note = add_note({
        'title': body.get('title'),
        'body': body.get('body'),
        'created_by': body.get('created_by'),
    })
    return jsonify(note)


@app.route('/notes/<int:id>', methods=['POST'])
def update_one_note(id):
    return jsonify(update_note(id, request.get_json()))


@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_one_note(id):
    success = remove_note(id)
    return jsonify(success)
