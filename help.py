"""Module is holding helping string"""

ARGUMENTS_PARSING = {
    'address': 'What do you want to fetch?',
    'output': 'Output path for the file, will be created if not existed, will use stdout if not specified',
    'method': 'Custom method for request, POST, GET, OPTIONS are supported',
    'timeout': 'Timeout for request',
    'body': 'Custom body for request,'
            ' supports only JSON, use like this: {argument:value, argument2:value2} or specify a path',
    'header': 'Custom headers for request,'
            ' supports only JSON, use like this: {argument:value, argument2:value2} or specify a path',
}

HELP_MISC = {
    'description':'Fetch them'
}