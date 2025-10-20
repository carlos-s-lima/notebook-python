from src.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Note(Base):
    __tablename__ = "Notes"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    content = Column(String)
    date = Column(DateTime, default=datetime.now)
    notebook_id = Column(Integer, ForeignKey("notebooks.id"))

    notebook = relationship("Notebook", back_populates="notes")

    def __repr__(self):
        content_preview = self.content if self.content else ""
        content_preview = (content_preview[:20] + '...') if len(content_preview) > 20 else content_preview
        
        data_formatada = self.date.strftime("%d/%m/%Y %H:%M:%S")

        return (
            f"<Note(id={self.id}, title='{self.title}', "
            f"content_preview='{content_preview}', date='{data_formatada}')>"
        )
    
class Notebook(Base):
    __tablename__ = "notebooks"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, default='Meu Caderno ')
    created_at = Column(DateTime, default=datetime.now)

    notes = relationship("Note", back_populates="notebook")

    def __repr__(self):
        data_formatada = self.created_at.strftime("%d/%m/%Y %H:%M:%S")
        return f"<Notebook(id={self.id}, name='{self.name}', created_at='{data_formatada}')>"