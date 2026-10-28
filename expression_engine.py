"""Safe stack-based expression conversion and evaluation.

Grammar: expression := operand (operator operand)*, with grouping in infix.
Operands are unsigned decimal numbers. Unary +/- are intentionally unsupported.
Operators: + - * / ^. Exponentiation is right-associative.
"""
from __future__ import annotations
import math
import re
from dataclasses import dataclass
from typing import Optional
from stack import Stack, StackError

MAX_EXPRESSION_LENGTH = 500
MAX_TOKENS = 200
MAX_ABS_RESULT = 1e100
NUMBER_RE = re.compile(r"(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\Z")
TOKEN_RE = re.compile(r"\s*(\d+(?:\.\d*)?(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?|[+\-*/^()\[\]])")
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
RIGHT_ASSOC = {"^"}
OPEN = {"(": ")", "[": "]"}
CLOSE = {")": "(", "]": "["}


class ExpressionError(ValueError):
    """A user-correctable expression or operation error."""


@dataclass(frozen=True)
class Node:
    value: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    @property
    def is_operand(self) -> bool:
        return self.left is None and self.right is None


def tokenize(expression: str) -> list[str]:
    if not isinstance(expression, str):
        raise ExpressionError("Expression must be text.")
    if not expression.strip():
        raise ExpressionError("Please enter an expression.")
    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ExpressionError(f"Expression is too long (maximum {MAX_EXPRESSION_LENGTH} characters).")
    tokens: list[str] = []
    pos = 0
    while pos < len(expression):
        match = TOKEN_RE.match(expression, pos)
        if not match:
            if expression[pos:].strip() == "":
                break
            char = expression[pos]
            if char.isalpha():
                raise ExpressionError(f"Invalid character '{char}'. Only numbers, brackets and + - * / ^ are supported.")
            raise ExpressionError(f"Invalid character '{char}'.")
        token = match.group(1)
        tokens.append(token)
        pos = match.end()
        if len(tokens) > MAX_TOKENS:
            raise ExpressionError(f"Expression contains too many tokens (maximum {MAX_TOKENS}).")
    for token in tokens:
        if token not in PRECEDENCE and token not in OPEN and token not in CLOSE and not NUMBER_RE.fullmatch(token):
            raise ExpressionError(f"Invalid token '{token}'.")
        if NUMBER_RE.fullmatch(token):
            try:
                value = float(token)
            except ValueError:
                raise ExpressionError(f"Invalid number '{token}'.") from None
            if not math.isfinite(value):
                raise ExpressionError(f"Number '{token}' is not finite.")
    return tokens


def _validate_infix_tokens(tokens: list[str]) -> None:
    expect_operand = True
    brackets: Stack[str] = Stack()
    for token in tokens:
        if NUMBER_RE.fullmatch(token):
            if not expect_operand:
                raise ExpressionError("Missing operator between adjacent operands.")
            expect_operand = False
        elif token in OPEN:
            if not expect_operand:
                raise ExpressionError("Missing operator before bracket.")
            brackets.push(token)
            expect_operand = True
        elif token in CLOSE:
            if expect_operand:
                raise ExpressionError("Missing operand before closing bracket.")
            if brackets.is_empty() or brackets.pop() != CLOSE[token]:
                raise ExpressionError("Mismatched brackets.")
            expect_operand = False
        else:
            if expect_operand:
                if token in {"+", "-"}:
                    raise ExpressionError("Unary plus and minus are not supported. Use non-negative operands and binary operators.")
                raise ExpressionError(f"Missing left operand for '{token}'.")
            expect_operand = True
    if not brackets.is_empty():
        raise ExpressionError("Mismatched brackets: a closing bracket is missing.")
    if expect_operand:
        raise ExpressionError("Expression ends with an operator or is missing an operand.")


def infix_to_postfix_tokens(tokens: list[str]) -> list[str]:
    _validate_infix_tokens(tokens)
    output: list[str] = []
    operators: Stack[str] = Stack()
    for token in tokens:
        if NUMBER_RE.fullmatch(token):
            output.append(token)
        elif token in OPEN:
            operators.push(token)
        elif token in CLOSE:
            while not operators.is_empty() and operators.peek() not in OPEN:
                output.append(operators.pop())
            if operators.is_empty() or operators.pop() != CLOSE[token]:
                raise ExpressionError("Mismatched brackets.")
        else:
            while not operators.is_empty() and operators.peek() not in OPEN:
                top = operators.peek()
                higher = PRECEDENCE[top] > PRECEDENCE[token]
                equal_left_assoc = PRECEDENCE[top] == PRECEDENCE[token] and token not in RIGHT_ASSOC
                if not (higher or equal_left_assoc):
                    break
                output.append(operators.pop())
            operators.push(token)
    while not operators.is_empty():
        op = operators.pop()
        if op in OPEN:
            raise ExpressionError("Mismatched brackets.")
        output.append(op)
    return output


def _node_from_postfix(tokens: list[str]) -> Node:
    if not tokens:
        raise ExpressionError("Please enter an expression.")
    stack: Stack[Node] = Stack()
    for token in tokens:
        if token in PRECEDENCE:
            if stack.size() < 2:
                raise ExpressionError(f"Insufficient operands for operator '{token}'.")
            right, left = stack.pop(), stack.pop()
            stack.push(Node(token, left, right))
        else:
            if not NUMBER_RE.fullmatch(token):
                raise ExpressionError(f"Invalid operand '{token}'.")
            stack.push(Node(token))
    if stack.size() != 1:
        raise ExpressionError("Extra operands: the expression has more than one result.")
    return stack.pop()


def _node_from_prefix(tokens: list[str]) -> Node:
    if not tokens:
        raise ExpressionError("Please enter an expression.")
    stack: Stack[Node] = Stack()
    for token in reversed(tokens):
        if token in PRECEDENCE:
            if stack.size() < 2:
                raise ExpressionError(f"Insufficient operands for operator '{token}'.")
            left, right = stack.pop(), stack.pop()
            stack.push(Node(token, left, right))
        else:
            if not NUMBER_RE.fullmatch(token):
                raise ExpressionError(f"Invalid operand '{token}'.")
            stack.push(Node(token))
    if stack.size() != 1:
        raise ExpressionError("Extra operands: the expression has more than one result.")
    return stack.pop()


def _postorder(node: Node) -> list[str]:
    result: list[str] = []
    stack: Stack[tuple[Node, bool]] = Stack()
    stack.push((node, False))
    while not stack.is_empty():
        current, visited = stack.pop()
        if current.is_operand:
            result.append(current.value)
        elif visited:
            result.append(current.value)
        else:
            stack.push((current, True))
            assert current.right is not None and current.left is not None
            stack.push((current.right, False))
            stack.push((current.left, False))
    return result


def _preorder(node: Node) -> list[str]:
    out: list[str] = []
    stack: Stack[Node] = Stack()
    stack.push(node)
    while not stack.is_empty():
        current = stack.pop()
        out.append(current.value)
        if current.right is not None:
            stack.push(current.right)
        if current.left is not None:
            stack.push(current.left)
    return out


def _inorder(node: Node) -> str:
    if node.is_operand:
        return node.value
    assert node.left is not None and node.right is not None
    return f"({ _inorder(node.left) } {node.value} { _inorder(node.right) })"


def _tokens_for_notation(expression: str, notation: str) -> list[str]:
    tokens = tokenize(expression)
    if any(t in OPEN or t in CLOSE for t in tokens):
        raise ExpressionError(f"Brackets are only accepted in infix notation, not {notation}.")
    return tokens


def convert(operation: str, expression: str) -> str:
    if operation in {"infix_to_postfix", "infix_to_prefix"}:
        tokens = tokenize(expression)
        postfix = infix_to_postfix_tokens(tokens)
        tree = _node_from_postfix(postfix)
    elif operation in {"postfix_to_infix", "postfix_to_prefix"}:
        tokens = _tokens_for_notation(expression, "postfix")
        tree = _node_from_postfix(tokens)
    elif operation in {"prefix_to_infix", "prefix_to_postfix"}:
        tokens = _tokens_for_notation(expression, "prefix")
        tree = _node_from_prefix(tokens)
    else:
        raise ExpressionError("Unsupported conversion operation.")
    if operation.endswith("to_postfix"):
        return " ".join(_postorder(tree))
    if operation.endswith("to_prefix"):
        return " ".join(_preorder(tree))
    return _inorder(tree)


def _calculate(operator: str, left: float, right: float) -> float:
    try:
        if operator == "+": result = left + right
        elif operator == "-": result = left - right
        elif operator == "*": result = left * right
        elif operator == "/":
            if right == 0: raise ExpressionError("Division by zero is not allowed.")
            result = left / right
        elif operator == "^":
            if abs(right) > 10000: raise ExpressionError("Exponent is too large.")
            if left == 0 and right < 0: raise ExpressionError("Zero cannot be raised to a negative power.")
            result = left ** right
        else: raise ExpressionError(f"Unsupported operator '{operator}'.")
    except ExpressionError:
        raise
    except (OverflowError, ZeroDivisionError, ValueError):
        raise ExpressionError("The expression produces an invalid or excessively large result.") from None
    if isinstance(result, complex) or not math.isfinite(result) or abs(result) > MAX_ABS_RESULT:
        raise ExpressionError("The expression produces a non-finite or excessively large result.")
    return result


def evaluate_postfix(expression: str) -> str:
    tokens = _tokens_for_notation(expression, "postfix")
    stack: Stack[float] = Stack()
    for token in tokens:
        if token in PRECEDENCE:
            if stack.size() < 2:
                raise ExpressionError(f"Insufficient operands for operator '{token}'.")
            right, left = stack.pop(), stack.pop()
            stack.push(_calculate(token, left, right))
        else:
            if not NUMBER_RE.fullmatch(token): raise ExpressionError(f"Invalid operand '{token}'.")
            stack.push(float(token))
    if stack.size() != 1:
        raise ExpressionError("Extra operands: the expression has more than one result.")
    return _format_number(stack.pop())


def evaluate_prefix(expression: str) -> str:
    tokens = _tokens_for_notation(expression, "prefix")
    stack: Stack[float] = Stack()
    for token in reversed(tokens):
        if token in PRECEDENCE:
            if stack.size() < 2:
                raise ExpressionError(f"Insufficient operands for operator '{token}'.")
            left, right = stack.pop(), stack.pop()
            stack.push(_calculate(token, left, right))
        else:
            if not NUMBER_RE.fullmatch(token): raise ExpressionError(f"Invalid operand '{token}'.")
            stack.push(float(token))
    if stack.size() != 1:
        raise ExpressionError("Extra operands: the expression has more than one result.")
    return _format_number(stack.pop())


def _format_number(value: float) -> str:
    if not math.isfinite(value):
        raise ExpressionError("The expression produces a non-finite result.")
    if value == 0: return "0"
    if value.is_integer(): return str(int(value))
    return format(value, ".12g")


def operate(operation: str, expression: str) -> str:
    """Dispatch a validated operation name to conversion or evaluation."""
    if operation in {"infix_to_postfix", "infix_to_prefix", "postfix_to_infix", "postfix_to_prefix", "prefix_to_infix", "prefix_to_postfix"}:
        return convert(operation, expression)
    if operation == "evaluate_postfix": return evaluate_postfix(expression)
    if operation == "evaluate_prefix": return evaluate_prefix(expression)
    raise ExpressionError("Unsupported operation.")
