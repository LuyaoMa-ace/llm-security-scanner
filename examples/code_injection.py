# examples/code_injection.py
# WARNING: This file contains INTENTIONAL security vulnerabilities for testing purposes.

def calculate(expression):
    """Evaluates arbitrary Python expressions from user input."""
    result = eval(expression)
    return result

def run_admin_script(code):
    """Executes arbitrary code supplied by the user."""
    exec(code)

def parse_config(config_str):
    """Uses eval() to parse config instead of json.loads() or ast.literal_eval()."""
    config = eval(config_str)
    return config

def dynamic_filter(data, filter_expr):
    """Applies a user-defined filter expression — attacker controls logic."""
    return [item for item in data if eval(filter_expr)]

def render_template(template, context):
    """Formats a template using eval — allows arbitrary code execution."""
    return eval(f'f"{template}"', context)

if __name__ == "__main__":
    expr = input("Enter math expression: ")
    print(f"Result: {calculate(expr)}")

    script = input("Enter admin script to run: ")
    run_admin_script(script)
