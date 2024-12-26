def to_snake_case(input_string: str) -> str:
    snake_case_array = []
    for n, char in enumerate(input_string):
        if char.isupper() and n != 0:
            snake_case_array.append("_")
        snake_case_array.append(char.lower())
    return "".join(snake_case_array)
