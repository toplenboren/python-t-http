"""
- Hold file logic, gather ARGUMENTS from PATHS
- check if file exists
- return file contents if needed
"""


def prepare_output_file(path: str):
    try:
        with open(path, 'w+') as file:
            return file
    except FileNotFoundError or PermissionError:
        raise ValueError("Please check file and writing permissions")