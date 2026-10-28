import unittest
from expression_engine import operate, ExpressionError

class EvaluationTests(unittest.TestCase):
    def test_postfix_evaluation(self):
        self.assertEqual(operate("evaluate_postfix", "3 4 2 * +"), "11")

    def test_prefix_evaluation(self):
        self.assertEqual(operate("evaluate_prefix", "+ 3 * 4 2"), "11")

    def test_precedence_and_brackets(self):
        self.assertEqual(operate("evaluate_postfix", "3 4 2 * +"), "11")
        self.assertEqual(operate("evaluate_postfix", "3 4 + 2 *"), "14")

    def test_exponent_associativity(self):
        self.assertEqual(operate("evaluate_postfix", "2 3 2 ^ ^"), "512")

    def test_decimal_and_multi_digit(self):
        self.assertEqual(operate("evaluate_postfix", "12.5 2.5 / 3 +"), "8")
        self.assertEqual(operate("evaluate_prefix", "/ 7 2"), "3.5")

    def test_subtraction_division_order(self):
        self.assertEqual(operate("evaluate_postfix", "9 2 -"), "7")
        self.assertEqual(operate("evaluate_postfix", "8 2 /"), "4")
        self.assertEqual(operate("evaluate_prefix", "- 9 2"), "7")
        self.assertEqual(operate("evaluate_prefix", "/ 8 2"), "4")

    def test_division_by_zero(self):
        for operation, expression in [("evaluate_postfix", "5 0 /"), ("evaluate_prefix", "/ 5 0")]:
            with self.subTest(operation=operation):
                with self.assertRaisesRegex(ExpressionError, "Division by zero"):
                    operate(operation, expression)

    def test_non_finite_or_excessive_result(self):
        with self.assertRaises(ExpressionError): operate("evaluate_postfix", "2 1000 ^")
        with self.assertRaises(ExpressionError): operate("evaluate_postfix", "2 3 - 0.5 ^")

if __name__ == "__main__": unittest.main()
