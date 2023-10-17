import json

def json_to_string(json_data):
    """Converts JSON data into a string.

    Args:
        json_data (dict): JSON data as a dictionary.

    Returns:
        str: JSON data converted to a string.
    """
    return json.dumps(json_data)

# Example usage:
data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

json_string = json_to_string(data)
print(f"type: {type(json_string)}; str: {json_string}")
print("--" * 10)
json_data = json.loads(json_string)
print(f"type: {type(json_data)}; data: {json_data}")
print([(k, v) for k, v in json_data.items()])
print("--" * 10)
assert json_data == data