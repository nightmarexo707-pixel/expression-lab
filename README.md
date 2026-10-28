# Expression Lab — Stack-Based Expression Evaluator & Converter

Expression Lab is a responsive educational web application that demonstrates a custom stack data structure through expression conversion and evaluation. The frontend is HTML/CSS/vanilla JavaScript; the backend is Python and Flask. User expressions are processed by the Python engine and are never executed as source code.

> **Live website:** Not deployed yet. Replace this line with the public Render URL only after deployment succeeds.  
> **Source code:** The URL of the GitHub repository will be available after you create and push it.

## Features

- Custom generic `Stack` class implemented with a Python list.
- Six conversions: infix↔postfix, infix↔prefix, postfix↔prefix and the reverse conversions to infix.
- Postfix and prefix arithmetic evaluation.
- Operators `+`, `-`, `*`, `/`, `^`; exponentiation is right-associative.
- Multi-digit and decimal operands; whitespace; nested `()` and `[]` in infix notation.
- Input validation, clear errors, division-by-zero checks, bounded expression size and bounded results.
- Responsive dark interface, sample expressions, copy-result action, and educational notes.
- Flask JSON API and `unittest` test suite.

## Technology stack

- Python 3.11 or compatible supported Python version
- Flask (web server and API)
- Gunicorn (production WSGI server)
- HTML5, CSS3, vanilla JavaScript and Fetch API
- Python standard library (`unittest`, `math`, `re`, `dataclasses`, `typing`)

## Project structure

```text
expression-lab/
├── app.py
├── stack.py
├── expression_engine.py
├── requirements.txt
├── render.yaml
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── tests/
│   ├── __init__.py
│   ├── test_stack.py
│   ├── test_conversion.py
│   ├── test_evaluation.py
│   └── test_api.py
└── docs/
    ├── project_report.md
    └── presentation_notes.md
```

## Run locally on Windows

1. Install Python 3.11+ and Git if not already installed.
2. Open the `expression-lab` folder in VS Code.
3. In VS Code's PowerShell terminal, create and activate a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or invoke `.venv\Scripts\python.exe` directly.
4. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Start the app:

   ```powershell
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser. Keep the terminal open while using it.

## Run tests

From the project root, with the virtual environment active:

```powershell
python -m unittest discover -s tests -v
```

Tests exercise the stack, all conversion directions, precedence and associativity, numeric evaluation, invalid input and Flask endpoints. Record the actual output from your own run in the submission report; do not claim a pass count without executing the command.

## API contract

`POST /api/operate` accepts JSON:

```json
{"operation":"infix_to_postfix","expression":"3 + 4 * 2"}
```

Successful response (`200`):

```json
{"success":true,"operation":"infix_to_postfix","result":"3 4 2 * +"}
```

Invalid user input returns a structured `400` response, unsupported media type returns `415`, and a request body over the Flask size limit returns `413`. The API allowlists operation names and never returns exception tracebacks to clients.

## Examples

| Operation | Input | Result |
|---|---|---|
| Infix → Postfix | `3 + 4 * 2` | `3 4 2 * +` |
| Infix → Prefix | `3 + 4 * 2` | `+ 3 * 4 2` |
| Evaluate Postfix | `3 4 2 * +` | `11` |
| Evaluate Prefix | `+ 3 * 4 2` | `11` |
| Right-associative exponent | `2 ^ 3 ^ 2` | postfix `2 3 2 ^ ^`; value `512` |

## Grammar and limitations

- Operands are unsigned decimal numeric literals; scientific notation is accepted.
- Unary `+` and `-` are intentionally unsupported and rejected with a clear message. Use binary operators only.
- Supported operators: `+`, `-`, `*`, `/`, `^`.
- Infix grouping accepts `()` and `[]`, including nested and correctly matched pairs.
- Prefix and postfix forms are token-based; use spaces between operands and operators for readability.
- Prefix/postfix notation does not accept grouping brackets.
- Input length is limited to 500 characters and 200 tokens; request bodies are limited to 16 KiB. Calculations with non-finite or excessively large results are rejected.
- The app is an academic demonstrator, not a symbolic algebra system; it does not simplify expressions or represent arbitrary-precision decimal arithmetic.

## Complexity

Let `n` be the number of tokens. Stack `push`, `pop`, `peek`, `is_empty`, and `size` are O(1) amortized/constant time. Tokenization is O(n) in input length. Shunting-yard conversion and prefix/postfix parsing are O(n) time and O(n) auxiliary space. Tree traversal for prefix/postfix output is O(n); infix tree rendering is O(n) output time, with recursive call depth proportional to tree height. Evaluation is O(n) stack operations and O(n) auxiliary space, excluding the cost of numeric arithmetic.

## Deploy to Render

1. Push the complete project to a GitHub repository (steps below).
2. Sign in to Render and choose **New → Blueprint** (or create a Web Service connected to the repository).
3. For Blueprint deployment, Render reads `render.yaml`; confirm service name `expression-lab`, build command `pip install -r requirements.txt`, and start command `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 30`.
4. Start the deployment and inspect the build/runtime logs. Fix any reported import or dependency error before sharing the link.
5. Once deployment reports success, open the assigned `https://...onrender.com` URL in a fresh/private browser session.
6. Test `3 + 4 * 2` with **Infix → Postfix** (expect `3 4 2 * +`), then evaluate postfix `3 4 2 * +` (expect `11`). Test one invalid input and confirm a readable error appears.
7. Copy the actual public website URL into the Google Form's working-project field. If the form has a source-code field, include the GitHub repository URL there.

The website URL is not the same as the local address or repository link:

- `http://127.0.0.1:5000`: only works on your own computer while the local server is running.
- `https://github.com/<your-account>/<your-repository>`: source code and project history; not the interactive deployed website.
- `https://<your-service>.onrender.com`: the public website after successful deployment.

## GitHub setup

Create an empty repository on GitHub, then from the project folder run:

```powershell
git init
git add .
git commit -m "Build Expression Lab stack expression evaluator"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/expression-lab.git
git push -u origin main
```

Replace the remote URL with your actual repository URL. Never commit `.env`, credentials, or private data.

## Team contributions

Update this section to reflect work that each person actually completed. Suggested four-person split:

1. **Member 1 — Stack module:** custom stack, underflow handling, stack unit tests.
2. **Member 2 — Expression algorithms:** parsing, conversions, evaluation, algorithm tests.
3. **Member 3 — Interface and API testing:** responsive frontend, Flask integration, endpoint tests and manual browser checks.
4. **Member 4 — Documentation and release:** report, complexity analysis, deployment, demo script and test evidence.

For a solo project, state that the same person completed all responsibilities. Do not report suggested allocations as completed contributions unless the team actually follows them.

## Future improvements

Potential extensions include a visual stack-operation trace generated from algorithm events, a syntax-highlighted expression editor, support for unary operators with a documented grammar, and a downloadable execution trace. These are not claimed as current features.
