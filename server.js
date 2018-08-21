const express = require('express');
const _ = require('lodash');
const bodyParser = require('body-parser');
const cors = require('cors');

const app = express();

app.use(bodyParser.json());
app.use(cors());

// Rough code to let us store notes in memory with out any DB complexity
const notes = {
  1: {
    id: 1,
    title: 'Test Note',
    body: 'This is a test note object that will be available by default',
    created_at: Date.now(),
    created_by: 'admin',
    edit_history: [{
      edited_at: Date.now(),
      edited_by: 'A User',
    }],
  },
};


const getNextId = () => _.parseInt(
  _.maxBy(Object.keys(notes), _.parseInt)
) + 1;

const addNote = ({ title, body, created_by }) => {
  const id = getNextId();
  notes[id] = {
    id,
    title,
    body,
    created_by,
    created_at: Date.now(),
    edit_history: [],
  };
  return notes[id];
};

const getNotes = () => notes;

const getNote = (id) => {
  const note = getNotes()[id];
  return note || null;
};

const updateNote = (id, update) => {
  const note = getNote(id);
  _.assign(
    note,
    _.pick(update, ['title', 'body'])
  );
  note.edit_history.push({
    edited_by: update.edited_by,
    edited_at: Date.now(),
  });
  return note;
};

const removeNote = (id) => {
  if (getNote(id)) {
    delete getNotes()[id];
    return true;
  }
  return false;
};

app.post('/notes', (req, res) => {
  const note = addNote(req.body);
  res.json(note);
});

app.get('/notes', (req, res) => {
  res.json(_.map(getNotes()));
});

app.get('/notes/:id', (req, res) => {
  const note = getNote(req.params.id);
  res.json(note);
});

app.post('/notes/:id', (req, res) => {
  const note = updateNote(req.params.id, req.body);
  res.json(note);
});

app.delete('/notes/:id', (req, res) => {
  const result = removeNote(req.params.id);
  res.json(result);
});

app.listen(5000, () => console.log('Server running on port 5000'));
