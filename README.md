# Caderno Digital

<div align="center">
  
Uma aplicação desktop para gerenciamento de notas desenvolvida com Python, PySide6 e SQLAlchemy.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://www.qt.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)

</div>

## Sobre o Projeto

O Caderno Digital é uma aplicação desktop que permite criar, editar, excluir e organizar notas em cadernos. Este projeto foi desenvolvido como trabalho acadêmico para aplicar conceitos de programação desktop, persistência de dados e interfaces gráficas com QT.

**Nota:** Este é um projeto estudantil. O código não está refinado e pode apresentar limitações, bugs e áreas que necessitam de otimização. Não é um software de produção.

## Tecnologias

<div align="left">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="Qt"/>
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy"/>
</div>

### Stack

- **PySide6** - Framework QT para interfaces gráficas
- **SQLAlchemy** - ORM para gerenciamento de banco de dados
- **SQLite** - Banco de dados relacional local

## Estrutura

```
├── src/
│   ├── database.py      # Configuração do banco de dados e engine
│   ├── models.py        # Modelos ORM (Note, Notebook)
│   ├── crud.py          # Operações CRUD
│   ├── dialogs.py       # Componentes de diálogo
│   └── main.py          # Aplicação principal e interface
└── meu_banco.db         # SQLite database (gerado em runtime)
```

## Funcionalidades

- Gerenciamento de múltiplos cadernos
- CRUD completo de notas
- Sistema de busca por título e conteúdo
- Interface com tema escuro
- Persistência em SQLite
- Prévia de conteúdo na listagem
- Timestamp de criação/edição

## Download

### Executável Windows

Disponível na [Release v1.0.0](https://github.com/carlos-s-lima/notebook-python/releases/tag/v1.0.0) - Inclui arquivo `.exe` standalone.

## Arquitetura

### Modelo de Dados

**Notebooks**
```python
- id: Integer (PK)
- name: String
- created_at: DateTime
- notes: Relationship
```

**Notes**
```python
- id: Integer (PK)
- title: String
- content: String
- date: DateTime
- notebook_id: Integer (FK)
- notebook: Relationship
```

### Padrões Utilizados

- **ORM Pattern** via SQLAlchemy
- **Repository Pattern** no módulo CRUD
- **MVC** (parcial) - separação de models, views e lógica
- **Session Management** com context do SQLAlchemy

## Limitações

Este projeto possui limitações típicas de um trabalho acadêmico:

- Ausência de testes automatizados
- Tratamento de erros básico
- Sem sistema de backup/exportação
- Interface não totalmente responsiva
- Código não completamente modularizado
- Sem validações robustas de entrada

## Possíveis Melhorias

- Implementar testes unitários e de integração
- Sistema de tags e filtros avançados
- Exportação para Markdown, PDF e TXT
- Editor de texto rico (WYSIWYG)
- Refatoração seguindo SOLID
- Sincronização em nuvem
- Sistema de anexos
- Themes customizáveis

## Desenvolvimento

**Requisitos:**
- Python 3.8+
- PySide6
- SQLAlchemy

**Estrutura de commits:** Commits não seguem convenção específica (projeto estudantil).

## Licença

Projeto desenvolvido para fins educacionais.

## Autor

Carlos Lima
[Meu LinkedIn](https://www.linkedin.com/in/carlos-s-lima/)

---

**Aviso:** Código em estágio de aprendizado. Não utilizar como referência de boas práticas ou em produção.