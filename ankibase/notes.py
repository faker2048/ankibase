import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, Generator


@dataclass
class Note:
    id: int
    guid: str
    mid: int
    mod: int
    usn: int
    tags: str
    flds: str
    sfld: int
    csum: int
    flags: int
    data: str
    """
    -- Notes contain the raw information that is formatted into a number of cards
    -- according to the models
    -- https://github.com/ankidroid/Anki-Android/wiki/Database-Structure#Notes
    """

    @classmethod
    def from_row(cls, row: tuple) -> "Note":
        return cls(*row)

    def to_row(self) -> tuple:
        return tuple(self.__dict__.values())


class NoteDatabase:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            conn.commit()
            conn.close()

    def insert_note(self, note: Note) -> None:
        with self.connect() as cursor:
            cursor.execute(
                "INSERT INTO notes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                note.to_row(),
            )

    def get_note(self, note_id: int) -> Optional[Note]:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
            row = cursor.fetchone()
            return Note.from_row(row) if row else None

    def get_notes(self) -> Generator[Optional[Note], None, None]:
        with self.connect() as cursor:
            cursor.execute("SELECT * FROM notes")
            rows = cursor.fetchall()
            for row in rows:
                yield Note.from_row(row)

    def update_note(self, note: Note) -> None:
        with self.connect() as cursor:
            cursor.execute(
                """
                UPDATE notes 
                SET id=?, guid=?, mid=?, mod=?, usn=?, tags=?, flds=?, sfld=?, 
                    csum=?, flags=?, data=? 
                WHERE id=?
            """,
                note.to_row() + (note.id,),
            )

    def delete_note(self, note_id: int) -> None:
        with self.connect() as cursor:
            cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
