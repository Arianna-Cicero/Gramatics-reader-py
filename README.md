## Functional Language Processing Application (FLPA)

# Introduction

This project aims to provide students of the Language Processing course with hands-on experience in defining lexical and syntactic analyzers, as well as semantic actions to translate implemented languages. The practical work should follow these steps:

Specify the concrete grammar of the input language.
Build a lexical analyzer using the lex library to recognize terminal symbols identified in the grammar and test it with some example words from the input language.
Build a syntactic analyzer using the yacc library to recognize the concrete grammar, and test it with some example sentences from the input language.
Plan an abstract syntax tree to represent the input language and associate semantic translation actions with the grammar productions to build the corresponding abstract syntax tree.
Develop a code generator that produces the requested output by evaluating the abstract syntax tree.
The goal is to implement an application for processing a functional language named "Linguagem Funcional do Cávado e do Ave" (FCA). The implemented application should be capable of reading a text file containing a program written in the FCA language (described in section 3.1) and executing the commands contained therein. Optionally, the application generates a text file with the corresponding C code.

# Project Structure

This practical work requires students to implement a Python application using the PLY library that interprets a language capable of specifying some instructions commonly found in functional programming languages. The application should start by reading a text file (with the .fca extension, representing "Funcional do Cávado e do Ave") containing a sequence of language specification commands and apply these commands to compute the desired result. The result of processing the entrada.fca text file is presented to the user in the terminal. Optionally, the program can generate a file with the corresponding C code implementation. If no input file is provided, the commands should be read from the terminal as the user enters them.

# Requirements

Python 3.x
PLY library (Python Lex-Yacc)
Installation

1. Clone the repository:

```bash
git clone https://github.com/username/FLPA.git
cd FLPA
```

2. Install the required dependencies:

```bash
Copiar código
pip install ply
```

3. Usage
   To run the application with an FCA file:

```bash
python main.py entrada.fca
```

To run the application and input commands directly via the terminal:

```bash
python main.py
```

# Example

An example of an FCA file (entrada.fca):

```py
# Example content of entrada.fca

def add(x, y) = x + y
print(add(5, 3))
```

Expected output when running the above example:

```py
8
```

# Features

- Lexical Analysis: Recognizes terminal symbols in the FCA language.
- Syntactic Analysis: Recognizes and parses the structure of FCA language.
- Abstract Syntax Tree (AST): Represents the structure of the FCA program.
- Semantic Actions: Translates FCA commands into executable actions.
- Code Generation: Optionally generates C code corresponding to the FCA program.

# Optional Features

- Generate a C file corresponding to the FCA program by running:

```bash
python main.py entrada.fca -o output.c
```

# Contribution

Contributions are welcome! Please fork the repository and submit a pull request.

# License

This project is licensed under the MIT License. See the LICENSE file for details.
