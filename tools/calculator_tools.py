from langchain.tools import tool

class CalculatorTools:
    @tool("Make a calculation")
    def perform_calculation(self, expression):
        """
        Perform a calculation based on the given mathematical expression.

        Args:
            expression (str): The mathematical expression to calculate.

        Returns:
            float: The result of the calculation.
        """
        try:
            # Evaluate the mathematical expression
            result = eval(expression)
            return result
        except Exception as e:
            return f"An error occurred: {str(e)}"
