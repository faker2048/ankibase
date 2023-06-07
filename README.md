# 📝 Note Database

This is a Python module for working with a SQLite database that stores notes. It provides a class `Note` to represent notes, and a class `NoteDatabase` to interact with the database.

## 🚀 Getting Started

### Prerequisites

Before using this module, you will need:

- Python 3.6 or later
- SQLite 3

### Installation

To install, simply download `note.py` and add it to your Python project.

### Usage

To use this module, first create an instance of `NoteDatabase`, passing the path to your SQLite database file:

```python
from note_database import NoteDatabase

db = NoteDatabase('/path/to/notes.sqlite')
```

#### Inserting a Note

To insert a new note, create a `Note` object and pass it to `insert_note()`:

```python
from note_database import Note

note = Note(
    id=1,
    guid='1234',
    mid=2,
    mod=12345678,
    usn=1,
    tags='tag1 tag2',
    flds='front back',
    sfld=0,
    csum=12345678,
    flags=0,
    data=''
)

db.insert_note(note)
```

#### Getting a Note

To get a single note by ID:

```python
note = db.get_note(1)
```

#### Getting All Notes

To get all notes:

```python
notes = list(db.get_notes())
```

#### Updating a Note

To update an existing note, modify the `Note` object and call `update_note()`:

```python
note = db.get_note(1)
note.tags = 'tag3 tag4'

db.update_note(note)
```

#### Deleting a Note

To delete a note:

```python
db.delete_note(1)
```

## 📖 Class Reference

### `Note`

A data class representing a note.

**Properties:**

- `id` (int): The ID of the note.
- `guid` (str): A unique identifier for the note.
- `mid` (int): The ID of the note's model.
- `mod` (int): The modification time of the note, in seconds since the Unix epoch.
- `usn` (int): The update sequence number of the note.
- `tags` (str): A space-separated list of tags associated with the note.
- `flds` (str): The fields of the note, separated by a null character.
- `sfld` (int): The sort field of the note.
- `csum` (int): The checksum of the note.
- `flags` (int): Bit flags for the note.
- `data` (str): The raw data of the note.

**Class Methods:**

- `from_row(row: tuple) -> Note`: Creates a `Note` object from a tuple returned by the database.
- `to_row() -> tuple`: Returns a tuple representation of the `Note` object.

### `NoteDatabase`

A class for interacting with a note database.

**Constructor:**

- `NoteDatabase(db_path: str)`: Creates a `NoteDatabase` object for the database at `db_path`.

**Methods:**

- `insert_note(note: Note) -> None`: Inserts a new note into the database.
- `get_note(note_id: int) -> Optional[Note]`: Returns the note with the specified ID, or `None` if it does not exist.
- `get_notes() -> Generator[Optional[Note], None, None]`: Yields all notes in the database.
- `update_note(note: Note) -> None`: Updates an existing note in the database.
- `delete_note(note_id: int) -> None`: Deletes the note with the specified ID from the database.


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
