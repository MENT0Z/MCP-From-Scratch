from registry import BaseTool

class CalculatorTool(BaseTool):
    name = "calculator"
    description = """A calculator tool for arithmetic calculations only.
Use this ONLY for numerical operations like addition,
subtraction, multiplication, or division.
Do NOT use this tool for general questions."""
    input_schema = {
        "operation": {
            "type": "string",
            "enum": ["add", "subtract", "multiply", "divide"],
            "description": "The arithmetic operation to perform."
        },
        "operands": {
            "type": "array",
            "items": {"type": "number"},
            "minItems": 2,
            "description": "A list of numbers to perform the operation on."
        }
    }

    def execute(self, arguments):
        operation = arguments.get("operation")
        operands = arguments.get("operands")

        if not operation or not operands:
            raise ValueError("Both 'operation' and 'operands' must be provided.")

        if operation == "add":
            return sum(operands)
        elif operation == "subtract":
            result = operands[0]
            for num in operands[1:]:
                result -= num
            return result
        elif operation == "multiply":
            result = 1
            for num in operands:
                result *= num
            return result
        elif operation == "divide":
            result = operands[0]
            for num in operands[1:]:
                if num == 0:
                    raise ValueError("Division by zero is not allowed.")
                result /= num
            return result
        else:
            raise ValueError(f"Unsupported operation: {operation}")