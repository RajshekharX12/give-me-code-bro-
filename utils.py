def normalize_number(user_input):
    """Normalize the input number to ensure it starts with 888."""
    normalized_number = user_input.replace(" ", "").replace("+888", "")
    if not normalized_number.startswith("888"):
        normalized_number = "888" + normalized_number
    return normalized_number
