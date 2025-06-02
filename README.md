# My Interpreter

A simple interpreter written in Python 3 for a custom programming language, built for coursework in Language Design and Implementation.

---

## 📦 Requirements

- Python 3.10+
- Lark parser

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

From the project root:

```bash
python src/main.py example_programs/stage1_arithmetic.txt
```

Or try:

```bash
python src/main.py example_programs/stage5_control_flow.txt
```

---

## 🗂️ Project Structure

```plaintext
src/
  ├── grammar.py        # Lark grammar definition
  ├── interpreter.py    # Execution logic
  ├── parser.py         # Lark parser setup
  └── main.py           # Entry point

example_programs/
  ├── stage1_arithmetic.txt
  ├── stage2_boolean.txt
  ├── stage3_text.txt
  ├── stage4_globals.txt
  └── stage5_control_flow.txt
```

---

## 🛠 Build Instructions (Optional)

You can also view `BUILD.txt` for detailed setup steps.

---

## 🧪 Tests

Run any `.txt` file from `example_programs/` to test a specific language feature.
