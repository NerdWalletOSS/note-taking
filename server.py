from datetime import datetime
from flask import Flask, jsonify, request


app = Flask(__name__)


""" Rough code to let us store notes in memory with out any DB complexity"""
notes = {
    1: {
        'id': 1,
        'title': 'Test Note',
        'body': 'This is a test note object that will be available by default',
        'created_at': datetime.now(),
        'created_by': 'admin',
    },
}
max_id = 1


def get_notes():
    global notes
    return notes


def get_note(id):
    return get_notes().get(id, None)


def update_note(id, update):
    note = get_note(id)
    note.update(update)
    return note


def remove_note(id):
    return get_notes().pop(id, False) is not False


def add_note(note):
    global max_id
    max_id = max_id + 1
    get_notes()[max_id] = note
    note['id'] = max_id
    note['created_at'] = datetime.now()
    return note


"""The public routes for manipulating notes"""


@app.route('/notes')
def get_all_notes():
    return jsonify(get_notes().values())


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
