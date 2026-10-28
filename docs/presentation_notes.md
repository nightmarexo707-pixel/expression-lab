# Expression Lab — 5–10 Minute Demonstration and Viva Notes

## Suggested 7-minute demonstration

1. **Introduction (30 seconds):** “Expression Lab is a DSA mini-project that demonstrates a custom stack through expression conversion and evaluation. The UI sends requests to a Python Flask API; the Python engine does the actual computation.”
2. **Infix → Postfix (45 seconds):** Enter `3 + 4 * 2`, choose Infix → Postfix, and show `3 4 2 * +`. Explain that multiplication has higher precedence, so `4 * 2` is emitted before `+`.
3. **Infix → Prefix (30 seconds):** Use the same input and show `+ 3 * 4 2`. Explain that prefix places each operator before its operands.
4. **Evaluation (45 seconds):** Enter postfix `3 4 2 * +`, choose Evaluate Postfix, and show `11`. Explain the stack pops right operand first, then left operand.
5. **Error handling (45 seconds):** Enter postfix `5 0 /`; show the division-by-zero error. Optionally show `3 +` to demonstrate missing-operand validation.
6. **Code walkthrough (90 seconds):** Open `stack.py` and explain `push`, `pop`, `peek`, `is_empty`, `size` and `StackError`. Then show `infix_to_postfix_tokens()` and `_calculate()` in `expression_engine.py`.
7. **Tests (45 seconds):** Run `python -m unittest discover -s tests -v` in the terminal. Show the real output, including any failures. Do not present unrun tests as passing.
8. **Complexity and repository (60 seconds):** Explain O(n) conversion/evaluation and O(n) auxiliary space. Open the GitHub repository and, if deployed, open the public Render URL in a fresh browser session.

## Likely viva questions and answers

**1. What is a stack?**  A linear abstract data type that follows LIFO: Last In, First Out.

**2. Why is a stack appropriate for expression conversion?** It temporarily stores operators until precedence, associativity or a closing bracket determines when they should be emitted.

**3. What is the difference between infix, prefix and postfix?** Infix puts the operator between operands (`A + B`); prefix puts it before (`+ A B`); postfix puts it after (`A B +`).

**4. Why is `3 + 4 * 2` converted to `3 4 2 * +`?** Multiplication has higher precedence, so it is processed before addition.

**5. Why is exponentiation right-associative?** By the specified arithmetic convention, `2 ^ 3 ^ 2` is interpreted as `2 ^ (3 ^ 2)`, giving 512 rather than `(2 ^ 3) ^ 2`.

**6. How do you preserve subtraction/division operand order in postfix?** Pop the right operand first, then the left operand; calculate `left operator right`.

**7. Why build an expression tree?** It preserves operand relationships and lets all notation conversions use a common validated structure. Stack-based parsing constructs it.

**8. What is the complexity?** Conversion and evaluation are O(n) time and O(n) auxiliary space for n tokens, excluding numeric-operation costs.

**9. Why not use `eval()`?** It can execute arbitrary Python expressions and is not a safe or suitable arithmetic parser. The engine validates tokens and implements operators explicitly.

**10. What happens on stack underflow?** `pop()` and `peek()` raise the custom `StackError` with a clear message.

**11. Why is Flask used?** It serves the web page and exposes a small HTTP API that calls the Python algorithms.

**12. What is the difference between localhost, GitHub and the deployed URL?** Localhost is the developer's own machine; GitHub hosts source code; the deployed URL runs the application on a public hosting service.

**13. Are unary minus and negative operands supported?** No. The grammar deliberately supports unsigned numeric literals and binary operators only; unary signs are rejected clearly.

**14. What are limitations?** It does not simplify symbolic expressions, support unary operators, persist history, or use arbitrary-precision decimal arithmetic.

## Final pre-demo checklist

- Run the complete test suite and keep its actual output ready.
- Start the local app and verify all eight operations.
- Verify invalid input displays an inline error, not a browser alert.
- If using Render, open the public URL in a private/fresh browser session and test conversion and evaluation.
- Have the GitHub repository ready and replace the report's team placeholders with real contributions.
