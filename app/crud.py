from typing import List
from app.models import Note, NoteCreate

# Simulación DB en Memoria
db: List[Note] = []
next_id = 1

def create_note(note: NoteCreate) -> Note:
    global next_id
    new_note = Note(id=next_id, **note.model_dump())
    db.append(new_note)
    next_id += 1
    return new_note

def get_notes() -> List[Note]:
    return db

def get_note_by_id(note_id: int) -> Note | None:
    note = None
    
    for n in db:
        if n.id == note_id:
            note = n
            break
        
    return note

def delete_note(note_id: int) -> bool:
    global db
    
    note = get_note_by_id(note_id)
    
    if note == None:
        return False
    
    db.remove(note)

    return True
