"""
Handles Presentation logic
"""
from http_client.response import Response


def check_output_file(path: str) -> bool:
    """
    Checks IO context to write to
    """
    try:
        with open(path, "w+") as file:
            return True
    except FileNotFoundError or PermissionError:
        raise ValueError("Please check file and writing permissions")


def outprint_to_console(resp: Response) -> None:
    """
    Prints a beautified response to console
    """
    print("————— Response: " + str(resp.status) + " —————")
    print("————— Response body length: " + str(resp.body_length) + " —————")
    print("————— Headers —————")
    print("{:<15} {:<15}".format("Name", "Value"))
    for k, v in resp.headers.items():
        print("{:<15} {:<15}".format(k, v))
    print("————— Body —————")
    print(resp.body)


def outprint_to_file(file_path: str, resp: Response) -> None:
    """
    Prints a simplified output to the IO context
    """
    with open(file_path, "w+", encoding=resp.encoding) as f:
        f.write(resp.body)


def outprint(file_path: str or None, resp: Response):
    if file_path is None:
        outprint_to_console(resp)
    else:
        outprint_to_file(file_path, resp)
