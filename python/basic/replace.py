def replace_all(text, substring, replacement):
    """
    Replaces all occurrences of a substring in a string with a replacement string.

    Args:
        text: The original string.
        substring: The substring to be replaced.
        replacement: The string to replace the substring with.

    Returns:
        The modified string with all occurrences of the substring replaced.
    """

    # Use the built-in str.replace method with optional count argument
    return text.replace(substring, replacement)

def read_query_from_file(file_path):
    """Reads the query string from a specified file."""
    with open(file_path, "r") as file:
        return file.read()


original_query = read_query_from_file("./file.sql")
temp = "Src"
r = "run_Date"
updated_query=original_query.replace("temp_table_name", temp).replace("run_Date_col", r)
# uqn = updated_query.replace("run_Date_col", r)
# print(uqn)
print(updated_query)
# Example usage
original_text = "This is a string with some subs. It also has more subs!"
substring = "sub"
new_text = replace_all(original_text, substring, "replaced")

print(f"Original text: {original_text}")
print(f"New text: {new_text}")
