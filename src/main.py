from datetime import datetime

class Note:
    """
    A classe "Note" representa uma anotação individual no Caderno.
    """
    
    def __init__(self, title: str, content: str):
        """
        Inicializa uma nova anotação. Datetime obtido automaticamente.
        
        Args:
            content: O conteúdo textual da anotação.
            title: O título da anotação.
        """
        data = datetime.now()
        self.date = data
        self.content = content
        self.title = title

    def __str__(self):
        """Define a representação em string para o objeto Note."""
        data_formatada = self.date.strftime("%d/%m/%Y %H:%M:%S")
        return f"Nota: '{self.title}' (Data: {data_formatada}, Conteúdo: '{self.content[:20]}...')"

class Notebook:
    """
    A classe "Notebook" representa a totalidade do caderno de anotações, 
    atuando como um contêiner para objetos Note.
    """

    def __init__(self):
        self.notes = []

    def append_note(self, note: Note):
        """
        Adiciona uma nova nota ao final da lista.

        Args:
            note: O objeto Note a ser adicionado.
        """
        self.notes.append(note)

    def read_note(self, index: int):
        """
        Lê e retorna uma nota a partir do índice.

        Args:
            index: O índice (posição) da nota a ser lida na lista.

        Returns:
            O objeto Note encontrado no índice especificado.
        """
        if 0 <= index < len(self.notes):
            return self.notes[index]
        else:
            raise IndexError("Índice de nota fora do intervalo válido.")
        
    def delete_note(self, index: int):
        """
        Lê e deleta uma nota a partir do índice

        Args:
            index: O índice (posição) da nota a ser deletada.

        Returns:
            A confirmação de sucesso

        """
        nota_removida = self.notes.pop(index)
        
        confirmacao = False
        while(not confirmacao):
            entrada = str(input(f"Você tem certeza de que quer apagar a nota {nota_removida}? (Y/N)")).upper()
            if (entrada == "Y"):
                print("Nota apagada permanentemente.")
                confirmacao = True
            elif (entrada == "N"):
                print("Nota não foi apagada.")
                self.notes.insert(index, nota_removida)
                confirmacao = True
            else:
                print("A entrada esperada é Y (YES) ou N (NO)")

    def read_notebook(self):
        """
        Lê todas as notas do caderno
        """
        for note in self.notes:
            print(note)
