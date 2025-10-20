import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QComboBox, QHBoxLayout, QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox,
    QInputDialog, QStatusBar 
)
from src.database import SessionLocal, engine, Base
import src.models as models
import src.crud as crud
from src.dialogs import NoteDialog

STYLESHEET = """
QWidget {
    background-color: #2E2E2E;
    color: #E0E0E0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
}
QMainWindow {
    background-color: #2E2E2E;
}
QTableWidget {
    background-color: #3A3A3A;
    border: 1px solid #4A4A4A;
    gridline-color: #4A4A4A;
}
QTableWidget::item {
    padding: 8px 5px;
    border: none;
}
QTableWidget::item:selected {
    background-color: #007AFF; /* Azul da Apple */
    color: #FFFFFF;
}
QHeaderView::section {
    background-color: #4A4A4A;
    padding: 5px;
    border: 1px solid #5A5A5A;
    font-weight: bold;
}
QTableCornerButton::section {
    background-color: #4A4A4A;
    border: 1px solid #5A5A5A;
}
QPushButton {
    background-color: #4A4A4A;
    border: 1px solid #5A5A5A;
    padding: 8px 12px;
    border-radius: 5px;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #5A5A5A;
}
QPushButton:pressed {
    background-color: #6A6A6A;
}
QLineEdit, QComboBox {
    background-color: #3A3A3A;
    border: 1px solid #5A5A5A;
    padding: 8px;
    border-radius: 5px;
}
QComboBox {
    padding: 8px 5px;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView { /* Estilo do dropdown */
    background-color: #3A3A3A;
    border: 1px solid #5A5A5A;
    selection-background-color: #007AFF;
    color: #E0E0E0;
    padding: 5px;
}
QStatusBar {
    padding: 5px;
}
QStatusBar::item {
    border: none;
}
QLabel {
    padding-top: 5px;
    font-size: 12px;
    color: #AAAAAA;
}
QDialog {
    background-color: #2E2E2E;
}
QTextEdit {
    background-color: #3A3A3A;
    border: 1px solid #5A5A5A;
    border-radius: 5px;
    padding: 5px;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = self.get_db()
        self.setup_database()
        
        self.setWindowTitle("Caderno Digital")
        self.setGeometry(100, 100, 900, 700)
        
        # --- Box maior: container vertical ---
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Seletor de Caderno (incluído na Box Maior)
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("CADERNO:"))
        self.notebook_selector = QComboBox()
        self.notebook_selector.currentIndexChanged.connect(self.on_notebook_selected)
        selector_layout.addWidget(self.notebook_selector, 1) 
        main_layout.addLayout(selector_layout)

        # Box pequena 1: horizontal, botões e pesquisa
        toolbar_layout = QHBoxLayout()
        
        self.add_button = QPushButton("Adicionar")
        self.edit_button = QPushButton("Editar")
        self.delete_button = QPushButton("Excluir")
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Pesquisar notas...")
        
        toolbar_layout.addWidget(self.add_button)
        toolbar_layout.addWidget(self.edit_button)
        toolbar_layout.addWidget(self.delete_button)
        toolbar_layout.addStretch(1) # Espaçador flexível
        toolbar_layout.addWidget(self.search_bar)
        
        main_layout.addLayout(toolbar_layout)

        # Box pequena 2: vertical, lista de notas
        self.note_table = QTableWidget()
        self.note_table.setColumnCount(3)
        self.note_table.setHorizontalHeaderLabels(["Título", "Prévia", "Data da Última Edição"])
        self.note_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.note_table.setEditTriggers(QAbstractItemView.EditTriggers.NoEditTriggers)
        self.note_table.verticalHeader().setVisible(False)
        
        # Ajuste das colunas
        header = self.note_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        self.note_table.setColumnWidth(0, 200)
        self.note_table.setColumnWidth(2, 160)

        main_layout.addWidget(self.note_table)
        
        # Definir widget central
        self.setCentralWidget(main_widget)
        
        # --- Barra de Status ---
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        self.status_message = QLabel("Pronto.")
        status_bar.addWidget(self.status_message)
        
        # --- Conectar Sinais ---
        self.add_button.clicked.connect(self.handle_add_note)
        self.edit_button.clicked.connect(self.handle_edit_note)
        self.delete_button.clicked.connect(self.handle_delete_note)
        self.search_bar.textChanged.connect(self.handle_search)
        self.note_table.itemDoubleClicked.connect(self.handle_edit_note)
        
        # --- Configuração de Ícones ---
        try:
            self.add_button.setIcon(QIcon.fromTheme("list-add"))
            self.edit_button.setIcon(QIcon.fromTheme("document-edit"))
            self.delete_button.setIcon(QIcon.fromTheme("list-remove"))
            self.add_button.setIconSize(QSize(20, 20))
            self.edit_button.setIconSize(QSize(20, 20))
            self.delete_button.setIconSize(QSize(20, 20))
        except Exception:
            pass
        
        # --- Carregamento Inicial ---
        self.load_notebooks()

    # --- Métodos de Lógica da UI ---

    def load_notebooks(self):
        self.notebook_selector.blockSignals(True) 
        
        current_id = self.get_current_notebook_id()
        self.notebook_selector.clear()
        
        notebooks = crud.get_all_notebooks(self.db)
        
        if not notebooks:
            crud.create_notebook(self.db, "Caderno 1")
            notebooks = crud.get_all_notebooks(self.db)
            
        new_index = 0
        for i, notebook in enumerate(notebooks):
            self.notebook_selector.addItem(notebook.name, userData=notebook.id)
            if notebook.id == current_id:
                new_index = i
        
        self.notebook_selector.addItem("— — — — —")
        separator_index = self.notebook_selector.count() - 1
        
        FLAGS_ROLE_VALUE = 3
        
        self.notebook_selector.setItemData(
            separator_index, 
            Qt.ItemFlag.NoItemFlags, 
            FLAGS_ROLE_VALUE
        ) 
        
        self.notebook_selector.addItem("Criar novo caderno...")
        self.notebook_selector.setItemData(self.notebook_selector.count() - 1, -1, Qt.ItemDataRole.UserRole)
        
        
        self.notebook_selector.setCurrentIndex(new_index)
        self.notebook_selector.blockSignals(False)
        
        if self.get_current_notebook_id() != -1:
            self.load_notes()
        else:
            self.note_table.setRowCount(0)

    def on_notebook_selected(self, index):
        if index == -1:
            return
            
        notebook_id = self.notebook_selector.itemData(index)

        if notebook_id == -1:
            # --- Criar Novo Caderno ---
            text, ok = QInputDialog.getText(self, "Novo Caderno", "Nome do novo caderno:")
            if ok and text.strip():
                crud.create_notebook(self.db, text)
                self.load_notebooks() 
            else:
                self.notebook_selector.setCurrentIndex(0) 
        else:
            # --- Carregar Notas do Caderno ---
            self.load_notes()

    def load_notes(self):
        notebook_id = self.get_current_notebook_id()
        if notebook_id is None or notebook_id == -1:
            self.note_table.setRowCount(0)
            return
        
        search_term = self.search_bar.text()
        if search_term:
            notes = crud.search_notes(self.db, search_term, notebook_id)
        else:
            notes = crud.get_all_notes_by_notebook(self.db, notebook_id)
        
        self.populate_table(notes)
        self.statusBar().showMessage(f"{len(notes)} nota(s) encontrada(s).")

    def populate_table(self, notes: list):
        # Helper para preencher a tabela com uma lista de notas.
        self.note_table.setRowCount(0) 
        
        for note in notes:
            row = self.note_table.rowCount()
            self.note_table.insertRow(row)
            
            title_item = QTableWidgetItem(note.title if note.title else "(Sem Título)")
            title_item.setData(Qt.ItemDataRole.UserRole, note.id)
            
            content_preview = note.content if note.content else ""
            preview = (content_preview[:80] + '...') if len(content_preview) > 80 else content_preview
            preview_item = QTableWidgetItem(preview.replace("\n", " "))
            
            date_str = note.date.strftime("%d/%m/%Y %H:%M")
            date_item = QTableWidgetItem(date_str)
            
            self.note_table.setItem(row, 0, title_item)
            self.note_table.setItem(row, 1, preview_item)
            self.note_table.setItem(row, 2, date_item)

    def handle_add_note(self):
        # Abre o diálogo para criar uma nova nota.
        current_notebook_id = self.get_current_notebook_id()
        if current_notebook_id is None or current_notebook_id == -1:
            QMessageBox.warning(self, "Erro", "Selecione um caderno válido primeiro.")
            return

        dialog = NoteDialog(self)
        if dialog.exec():
            title, content = dialog.get_data()
            if not title and not content:
                return
                
            crud.create_note(self.db, title, content, current_notebook_id)
            self.load_notes()

    def handle_edit_note(self):
        # Abre o diálogo para editar a nota selecionada.
        note_id, _ = self.get_selected_note_id()
        if note_id is None:
            QMessageBox.warning(self, "Seleção", "Por favor, selecione uma nota para editar.")
            return
            
        note_to_edit = crud.get_note_by_id(self.db, note_id)
        if not note_to_edit:
            QMessageBox.critical(self, "Erro", "Nota não encontrada no banco de dados.")
            return
            
        dialog = NoteDialog(self, note=note_to_edit)
        if dialog.exec():
            title, content = dialog.get_data()
            crud.update_note_content(self.db, note_id, new_title=title, new_content=content)
            self.load_notes()

    def handle_delete_note(self):
        note_id, row = self.get_selected_note_id()
        
        if note_id is None:
            QMessageBox.warning(self, "Seleção", "Por favor, selecione uma nota para excluir.")
            return

        title = self.note_table.item(row, 0).text()
        
        reply = QMessageBox.question(
            self, 
            "Confirmar Exclusão", 
            f"Tem certeza que deseja excluir a nota \"{title}\"?\nEsta ação não pode ser desfeita.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel
        )

        if reply == QMessageBox.StandardButton.Yes:
            success = crud.delete_note(self.db, note_id)
            if success:
                self.load_notes()
            else:
                QMessageBox.critical(self, "Erro", "Não foi possível excluir a nota.")

    def handle_search(self, text: str):
        self.load_notes()

    # --- Métodos Helper ---

    def get_current_notebook_id(self):
        return self.notebook_selector.currentData()

    def get_selected_note_id(self):
        selected_items = self.note_table.selectedItems()
        if not selected_items:
            return None, None
            
        selected_row = selected_items[0].row()
        note_id_item = self.note_table.item(selected_row, 0)
        
        if not note_id_item:
            return None, None
            
        return note_id_item.data(Qt.ItemDataRole.UserRole), selected_row

    def get_db(self):
        return SessionLocal()

    def setup_database(self):
        try:
            Base.metadata.create_all(bind=engine)
        except Exception as e:
            print(f"Erro ao criar tabelas: {e}")
            QMessageBox.critical(self, "Erro de Banco de Dados", f"Não foi possível inicializar o banco de dados: {e}")
            sys.exit(1)

if __name__ == "__main__":
    app = None
    window = None
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet(STYLESHEET) 
        
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"Erro fatal: {e}")
        QMessageBox.critical(None, "Erro Fatal", f"Ocorreu um erro inesperado e a aplicação será fechada:\n{e}")
        
    finally:
        if 'window' in locals() and window and hasattr(window, 'db'):
            print("Fechando conexão com o banco de dados.")
            window.db.close()