import sqlite3
from dataclasses import dataclass
from typing import Optional, Generator


@dataclass
class Note:
    """
    -- Notes contain the raw information that is formatted into a number of cards
    -- according to the models
    -- https://github.com/ankidroid/Anki-Android/wiki/Database-Structure#Notes
    """

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

    @classmethod
    def from_row(cls, row: tuple) -> "Note":
        return cls(*row)

    def to_row(self) -> tuple:
        return tuple(self.__dict__.values())


class NoteDatabase:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def close(self) -> None:
        self.conn.commit()
        self.conn.close()

    def insert_note(self, note: Note) -> None:
        self.cursor.execute(
            "INSERT INTO notes VALUES (" + ", ".join(["?"] * len(note.to_row())) + ")",
            note.to_row(),
        )
        self.conn.commit()

    def get_note(self, note_id: int) -> Optional[Note]:
        self.cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
        row = self.cursor.fetchone()
        return Note.from_row(row) if row else None

    def get_notes(self) -> Generator[Optional[Note], None, None]:
        self.cursor.execute("SELECT * FROM notes")
        while True:
            row = self.cursor.fetchone()
            if row is None:
                break
            yield Note.from_row(row)

    def update_note(self, note: Note) -> None:
        set_query = ", ".join(f"{field} = ?" for field in Note.__annotations__.keys())
        self.cursor.execute(
            f"""
            UPDATE notes 
            SET {set_query}
            WHERE id=?
            """,
            note.to_row() + (note.id,),
        )
        self.conn.commit()

    def delete_note(self, note_id: int) -> None:
        self.cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
        self.conn.commit()
