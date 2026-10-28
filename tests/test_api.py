import json
import unittest
from app import app

class ApiTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Expression Lab", response.data)

    def test_successful_conversion(self):
        response = self.client.post("/api/operate", json={"operation": "infix_to_postfix", "expression": "3 + 4 * 2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"success": True, "operation": "infix_to_postfix", "result": "3 4 2 * +"})

    def test_successful_evaluation(self):
        response = self.client.post("/api/operate", json={"operation": "evaluate_postfix", "expression": "3 4 2 * +"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["result"], "11")

    def test_missing_fields(self):
        response = self.client.post("/api/operate", json={"operation": "infix_to_postfix"})
        self.assertEqual(response.status_code, 400)

    def test_malformed_json(self):
        response = self.client.post("/api/operate", data="{broken", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_wrong_content_type(self):
        response = self.client.post("/api/operate", data="{}", content_type="text/plain")
        self.assertEqual(response.status_code, 415)

    def test_invalid_operation(self):
        response = self.client.post("/api/operate", json={"operation": "eval", "expression": "1+1"})
        self.assertEqual(response.status_code, 400)

    def test_invalid_expression(self):
        response = self.client.post("/api/operate", json={"operation": "evaluate_postfix", "expression": "3 0 /"})
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.get_json()["success"])

    def test_json_not_object(self):
        response = self.client.post("/api/operate", data=json.dumps([1, 2]), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_expression_limit(self):
        response = self.client.post("/api/operate", json={"operation": "infix_to_postfix", "expression": "1" * 501})
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__": unittest.main()
