# Expression Lab — Project Report

**Project type:** Data Structures and Algorithms mini-project  
**Programme:** B.Tech CSE, Semester 3  
**Implementation:** Python, Flask, HTML, CSS and JavaScript  
**Team members:** Replace with actual names and contributions before submission.

## 1. Abstract

Expression Lab is a browser-based educational application for converting arithmetic expressions between infix, postfix and prefix notation and evaluating prefix/postfix expressions. The project demonstrates the stack abstract data type through a custom list-backed `Stack` class rather than relying on a third-party stack container. A Flask API connects the frontend to the Python expression engine. Input validation prevents malformed expressions from being evaluated, and arithmetic is implemented explicitly without using dynamic-code execution. The project combines a visible interface, documented algorithms, automated tests and deployment configuration to make core DSA concepts accessible during a live demonstration.

## 2. Problem statement and objectives

Arithmetic expressions can be written in different notations. In infix notation, an operator appears between its operands, so precedence and brackets are needed to determine the order of operations. Prefix and postfix notations encode operator order directly. Stacks provide a simple way to process operators and operands in the correct order.

The objectives are to implement a reusable stack, convert between all six notation directions, evaluate prefix and postfix expressions, reject invalid input safely, expose the algorithms through a responsive web interface, and test correctness with repeatable unit tests.

## 3. Requirements and tools

**Functional requirements:** accept an expression; run one of eight operations; display a computed result or readable error; copy results; support infix brackets; and provide sample inputs. **Non-functional requirements:** responsive layout, understandable source code, bounded input size, no unsafe expression execution, structured API responses and reproducible tests.

**Tools:** Python 3.11+, Flask, Gunicorn, HTML5, CSS3, vanilla JavaScript, Fetch API, Git/GitHub and Render. Python standard-library modules handle regular expressions, numeric checks, dataclasses and unit tests.

## 4. System architecture

The browser renders `templates/index.html` and loads `static/css/style.css` and `static/js/app.js`. When a user selects an operation, JavaScript sends `POST /api/operate` with JSON containing `operation` and `expression`. Flask validates the content type, JSON shape, allowlisted operation name and expression length. The handler invokes `operate()` in `expression_engine.py`. A successful response includes `success`, `operation` and `result`; user-correctable errors return a structured client error. The frontend renders the response without evaluating the expression itself.

The `Stack` class is isolated in `stack.py`. The expression engine uses this stack in shunting-yard conversion, prefix/postfix parsing, tree traversals and evaluation. Expression trees are an intermediate representation for conversions: they preserve operand order and allow each target notation to be generated from one validated structure. The tree is not a replacement for stacks; stack-based parsing constructs it, and stack-based traversals generate prefix/postfix outputs.

## 5. Stack design

The custom generic `Stack[T]` stores items in a private Python list. `push(item)` appends to the end; `pop()` removes the final item; `peek()` reads the final item without removing it; `is_empty()` checks whether the list is empty; and `size()` returns its length. `pop()` and `peek()` raise `StackError` on underflow.

| Method | Time | Explanation |
|---|---:|---|
| `push` | O(1) amortized | Append to list end; occasional resizing is amortized. |
| `pop` | O(1) | Remove from list end. |
| `peek` | O(1) | Read last item. |
| `is_empty` | O(1) | Compare length to zero. |
| `size` | O(1) | Read list length. |

The LIFO rule means the most recently pushed item is removed first. This is essential when applying an operator to the most recently available operands or processing pending operators by precedence.

## 6. Algorithms

### 6.1 Infix to postfix

The engine tokenizes the input and validates operand/operator positions and bracket pairing. It scans tokens left to right. Operands go directly to output. Opening brackets are pushed. For an operator, higher-precedence operators at the top of the stack are emitted first; equal precedence is emitted first for left-associative operators. Exponentiation is right-associative, so an equal-precedence `^` remains on the stack until the later exponent is processed. Closing brackets cause operators to be emitted until the matching opening bracket is removed.

### 6.2 Prefix and postfix parsing

For postfix, tokens are scanned left to right. An operand creates a leaf node and is pushed. An operator pops the right child first and then the left child, builds a node and pushes it. For prefix, tokens are scanned right to left; the first popped node becomes the left child, then the right child. Exactly one tree must remain at the end; too few operands or extra operands are errors.

### 6.3 Conversions

The validated tree preserves the operation and left/right operand relationship. Postorder traversal yields postfix; preorder traversal yields prefix; inorder traversal yields a fully parenthesized infix expression. This design avoids separate fragile conversion rules for every direction while retaining stack-based construction and traversal. The infix renderer is recursive; prefix and postfix output traversals use the custom stack.

### 6.4 Evaluation

Postfix evaluation scans left to right. For an operator, the first popped value is the right operand and the second is the left operand. Prefix evaluation scans right to left; the first popped value is the left operand. The arithmetic helper explicitly implements the five supported operators, checks division by zero and rejects non-finite or excessively large results. No expression text is passed to `eval()` or `exec()`.

## 7. Worked stack trace

Expression: `3 + 4 * 2`

| Token | Action | Operator stack (bottom → top) | Output |
|---|---|---|---|
| `3` | Emit operand | empty | `3` |
| `+` | Push operator | `+` | `3` |
| `4` | Emit operand | `+` | `3 4` |
| `*` | Higher precedence than `+`; push | `+`, `*` | `3 4` |
| `2` | Emit operand | `+`, `*` | `3 4 2` |
| End | Pop `*`, then `+` | empty | `3 4 2 * +` |

Multiplication is emitted before addition because `*` has higher precedence. Evaluating `3 4 2 * +` gives `4 × 2 = 8`, then `3 + 8 = 11`.

## 8. Sample input/output

| Operation | Input | Output |
|---|---|---|
| Infix → Postfix | `3 + 4 * 2` | `3 4 2 * +` |
| Infix → Prefix | `3 + 4 * 2` | `+ 3 * 4 2` |
| Postfix → Infix | `3 4 2 * +` | `(3 + (4 * 2))` |
| Prefix → Postfix | `+ 3 * 4 2` | `3 4 2 * +` |
| Evaluate Postfix | `3 4 2 * +` | `11` |
| Evaluate Prefix | `+ 3 * 4 2` | `11` |
| Right-associative power | `2 ^ 3 ^ 2` | postfix `2 3 2 ^ ^`; result `512` |
| Invalid arithmetic | `5 0 /` | Division-by-zero error |

## 9. Validation and security

The app limits expressions to 500 characters and 200 tokens and limits JSON request bodies to 16 KiB. Operation names are checked against an explicit allowlist. The API verifies JSON content type and object shape. Invalid expressions return readable `400` responses; oversized bodies return `413`; unsupported content types return `415`. Unexpected server failures are logged server-side but do not expose tracebacks in public responses. Expressions are not persisted, and no user accounts or personal information are required.

The grammar supports unsigned integer/decimal operands, optional scientific notation, binary `+ - * / ^`, and nested `()`/`[]` in infix notation. Unary signs are explicitly unsupported. Prefix and postfix expressions are token-based and do not accept brackets. The implementation is not a symbolic algebra system and does not use arbitrary-precision decimal arithmetic.

## 10. Testing and results

Tests are organized in `tests/test_stack.py`, `tests/test_conversion.py`, `tests/test_evaluation.py` and `tests/test_api.py`. They cover stack underflow and LIFO behavior, all six conversion directions, precedence and exponent associativity, decimal and multi-digit operands, operand order, malformed expressions, division by zero, API validation and request limits.

**Actual verification in the build environment:** The stack, conversion and evaluation suites were executed: **25 tests passed, 0 failed**. Python source compilation also succeeded. The Flask API suite is included but could not be executed in this environment because Flask was not installed and package installation was blocked by unavailable network access. After installing `requirements.txt` on your computer, run `python -m unittest discover -s tests -v` to execute the complete suite; report its actual result. A fresh-browser smoke test should additionally verify the deployed page, conversion and evaluation through the public backend.

## 11. Complexity analysis

Let `n` be the number of expression tokens. Tokenization is O(n) in the expression length. Infix validation and shunting-yard conversion each take O(n) time and O(n) space because each token is processed a constant number of times and stacks may hold O(n) items. Prefix/postfix parsing takes O(n) time and O(n) space for the stack and expression tree. Prefix/postfix tree traversal is O(n) time and O(h) traversal stack space, bounded by O(n), where `h` is tree height. Infix rendering emits each node once and takes O(n) output time; recursive call depth is O(h). Evaluation takes O(n) stack operations and O(n) auxiliary space. These estimates treat arithmetic operations as constant-time; very large integer/power calculations have additional numeric cost and are bounded by application checks.

## 12. Contributions, conclusion and future scope

Record each team member's real contribution. Suggested four-person allocation: (1) stack and tests, (2) expression engine and algorithms, (3) UI/API integration and browser testing, (4) documentation, report, deployment and demonstration. Change this allocation to reflect actual work; for an individual submission, state that one student completed all areas.

Expression Lab demonstrates how stacks solve a practical parsing and evaluation problem. Its separation into stack, expression engine, API and frontend makes it easy to test and explain. Future work could include an algorithm trace panel generated from real execution events, a richer expression editor, carefully specified unary operators and downloadable traces.
