# Define a string representing a simple function
function_string = "def my_function(x):\n\tprint(55)\n\treturn x * 2"

# Create a global namespace for the function
namespace = {}

# Execute the string as Python code
exec(function_string, namespace)

# Access the function from the namespace
my_function = namespace['my_function']

# Call the function
result = my_function(5)
print(result)  # Output: 10