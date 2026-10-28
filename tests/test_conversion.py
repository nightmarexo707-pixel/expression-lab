import unittest
from expression_engine import operate, ExpressionError

class ConversionTests(unittest.TestCase):
    def test_infix_to_postfix_precedence(self):
        self.assertEqual(operate("infix_to_postfix", "3 + 4 * 2"), "3 4 2 * +")

    def test_infix_to_postfix_brackets(self):
        self.assertEqual(operate("infix_to_postfix", "(3 + 4) * 2"), "3 4 + 2 *")

    def test_right_associative_exponent(self):
        self.assertEqual(operate("infix_to_postfix", "2 ^ 3 ^ 2"), "2 3 2 ^ ^")
        self.assertEqual(operate("infix_to_prefix", "2 ^ 3 ^ 2"), "^ 2 ^ 3 2")

    def test_infix_to_prefix(self):
        self.assertEqual(operate("infix_to_prefix", "3 + 4 * 2"), "+ 3 * 4 2")

    def test_postfix_to_infix_and_prefix(self):
        self.assertEqual(operate("postfix_to_infix", "3 4 2 * +"), "(3 + (4 * 2))")
        self.assertEqual(operate("postfix_to_prefix", "3 4 2 * +"), "+ 3 * 4 2")

    def test_prefix_to_infix_and_postfix(self):
        self.assertEqual(operate("prefix_to_infix", "+ 3 * 4 2"), "(3 + (4 * 2))")
        self.assertEqual(operate("prefix_to_postfix", "+ 3 * 4 2"), "3 4 2 * +")

    def test_nested_square_brackets(self):
        self.assertEqual(operate("infix_to_postfix", "[3 + (4 * 2)]"), "3 4 2 * +")

    def test_multidigit_decimal_whitespace(self):
        self.assertEqual(operate("infix_to_postfix", "  12.5   /  2.5 + 3 "), "12.5 2.5 / 3 +")

    def test_subtraction_order(self):
        self.assertEqual(operate("postfix_to_infix", "9 2 -"), "(9 - 2)")
        self.assertEqual(operate("prefix_to_infix", "/ 8 2"), "(8 / 2)")

    def test_invalid_expressions(self):
        cases = ["", "3 +", "* 3 4", "3 4 +", "(3 + 4", "3 + 4]", "3 + -4", "3 @ 4", "1..2 + 3"]
        for expression in cases:
            with self.subTest(expression=expression):
                with self.assertRaises(ExpressionError):
                    operate("infix_to_postfix", expression)

    def test_invalid_prefix_postfix_arity(self):
        for operation, expression in [("evaluate_postfix", "2 +"), ("evaluate_postfix", "2 3"), ("evaluate_prefix", "+ 2"), ("evaluate_prefix", "+ 2 3 4")]:
            with self.subTest(operation=operation, expression=expression):
                with self.assertRaises(ExpressionError): operate(operation, expression)

    def test_unary_is_rejected(self):
        with self.assertRaisesRegex(ExpressionError, "Unary"):
            operate("infix_to_postfix", "-3 + 4")

if __name__ == "__main__": unittest.main()
