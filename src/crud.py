from sqlalchemy.orm import Session
from . import models

def create_note(db: Session, title: str, content: str, notebook_id: int):
    db_note = models.Note(
        title=title,
        content=content,
        notebook_id=notebook_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    
    return db_note

def get_note_by_id(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()

def get_all_notes_by_notebook(db: Session, notebook_id: int):

    return db.query(models.Note).filter(models.Note.notebook_id == notebook_id).all()

def delete_note(db: Session, note_id: int):
    note_to_delete = get_note_by_id(db, note_id)
    
    if note_to_delete:
        db.delete(note_to_delete)
        db.commit()
        return True
    return False

def get_all_notes(db: Session):
    return db.query(models.Note).all()

def search_notes(db: Session, keyword: str):
    search_term = f"%{keyword.lower()}%"
    
    return db.query(models.Note).filter(
        models.Note.title.ilike(search_term) | models.Note.content.ilike(search_term)
    ).all()

def update_note_content(db: Session, note_id: int, new_title: str = None, new_content: str = None):
    
    note_to_update = get_note_by_id(db, note_id)
    
    if note_to_update:
        if new_title is not None:
            note_to_update.title = new_title
        if new_content is not None:
            note_to_update.content = new_content
            
        db.commit()
        db.refresh(note_to_update)
        return note_to_update
        
    return None # Nota não encontrada