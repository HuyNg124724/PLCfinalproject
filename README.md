# PLC Final Project – Custom Programming Language

This is the final project for the Programming Languages and Compilers course at AIT. It is a custom-designed, Python-based compiler for a small programming language that supports essential features such as arithmetic expressions, booleans, strings, dynamic typing, control structures, functions, and a GUI for code interaction.

## Features

The language supports the following:

- **Types**: `int`, `float`, `boolean`, and `string`
- **Dynamic Typing**: Runtime type checking and error handling
- **Arithmetic Expressions**: `+`, `-`, `*`, `/` with correct precedence
- **Boolean Expressions**: `==`, `!=` between arithmetic expressions
- **String Operations**: Concatenation using `+` operator
- **Control Flow**: 
  - `if ... then ... else ... end`
  - `while ... do ... end`
- **Functions**: 
  - Definitional parameter passing (no recursion)
  - User-defined functions with `def ... end`
- **Built-in Function**: `print(...)`
- **PyQt6 GUI**: Built-in IDE with code input, AST tree view, and output display

---

## Architecture Overview

```

compiler-starter-project/
├── main.py                  # Main entry point with PyQt6 GUI
├── components/
│   ├── main.ui              # GUI layout file (created with Qt Designer)
│   ├── lexica.py            # Lexer implementation using SLY
│   ├── parsers.py           # Parser generating AST nodes
│   ├── memory.py            # Runtime memory & function environment
│   └── ast/
│       └── statement.py     # AST node definitions and execution logic

````

---

## How to Run

### Requirements:
- Python 3.9.x
- [PDM](https://pdm.fming.dev/latest/)
- PyQt6
- SLY

### Install dependencies:

```bash
pdm install
````

### Run the app:

```bash
pdm run app
```

If you're not using PDM:

```bash
python main.py
```

---

## Sample Test Case

🔗 [PLC_Language_Test_Cases.pdf](https://github.com/user-attachments/files/20034526/PLC_Language_Test_Cases.pdf)

---

## GitHub Deployment

This project is hosted at:
🔗 [github.com/HuyNg124724/PLCfinalproject](https://github.com/HuyNg124724/PLCfinalproject)

The repository includes:

* Full source code
* GUI layout
* Language grammar
* Example programs

---

## License

This project is for academic purposes and coursework submission. Contact the author for reuse or collaboration. You can copy this into a file called `README.md` and place it in the root of your GitHub project. Then run:

```bash
git add README.md
git commit -m "Add project README"
git push
````
