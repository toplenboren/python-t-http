[![Coverage Status](https://coveralls.io/repos/github/toplenboren/python-t-http/badge.svg?branch=master)](https://coveralls.io/github/toplenboren/python-t-http?branch=master)

# python-t-http
A simple console http client, that was made during my time at the Uni

# HTTP client:
Http client is a program, which is capable of sending and recieving http-requests
More on http on [RFC](https://tools.ietf.org/html/2616)

# Requirements:
* `Python 3.7+`

# Usage:
`python main.py http(s)//{host} [args]`
`python main.py -h`

## Usage examples:
* Preform a simple GET request to the address and use console as output: `python main.py https://example.com`
* Use file as output `python main.py https://example.com -o test.html`
* Send custom POST request `python main.py https://api.somethig.com -m POST -h Content-Language=ru -b login=user,password=1234`

# Under the hood:
Basically sending an HTTP request and getting the HTTP response goes like that:
1. Get user arguments: address, method, headers, body
2. Compile a request from this arguments
3. Create a python `socket` from the request and arguments
4. Get the response from `socket.recv`
5. Serve the response to the user via console or file

For every number there are a module or a class that does the work. 
 
1. Setup `argparse` module in `main.py`, I use some constants from `help.py`. Process arguments in form of `dict` in `client.py`
2. Compile HTTP request in `request.py` module
3. Use `fetch.py` to create a python `socket` 
4. Send python `socket` to the `response.py` where it gets processed
5. Serve the respone using `io_hanlder.py`

There are also: 
* `socket_extensions.py` — handles some additional methods to the socket class, they help me recieve the data: `read_line` and `read_section`
* `address.py` — handles some logic, that is connected with http address processing
