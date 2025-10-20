from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QTextEdit, 
    QDialogButtonBox, QLabel, QWidget
)
from . import models

class NoteDialog(QDialog):

    def __init__(self, parent: QWidget = None, note: models.Note = None):
        super().__init__(parent)

        self.note = note
        self.setWindowTitle("Editar Nota" if note else "Adicionar Nova Nota")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Título:"))
        self.title_edit = QLineEdit()
        layout.addWidget(self.title_edit)

        layout.addWidget(QLabel("Conteúdo:"))
        self.content_edit = QTextEdit()
        layout.addWidget(self.content_edit)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        if note:
            self.title_edit.setText(note.title)
            self.content_edit.setPlainText(note.content)

    def get_data(self):
        return self.title_edit.text(), self.content_edit.toPlainText()