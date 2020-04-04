class Address:

    def __init__(self, addr: str):
        parsed_addr = Address.parse(addr)
        self.protocol = parsed_addr[0]
        self.host = parsed_addr[1]
        self.path = parsed_addr[2]

    # TODO rewrite
    @staticmethod
    def parse(addr: str) -> (str, str, str):
        if len(addr) < 8:
            raise ValueError("Bad address, please ensure it starts with http:// or https://")

        if addr[0:7].lower() == 'http://':
            protocol = addr[0:7]
            host = addr[7:].split('/')[0]
            path = '/'.join(addr[7:].split('/')[1:])
            return protocol, host, path

        elif addr[0:8].lower() == 'https://':
            protocol = addr[0:8]
            host = addr[8:].split('/')[0]
            path = '/'.join(addr[8:].split('/')[1:])
            return protocol, host, path

        else:
            raise ValueError("Bad address, please ensure it starts with http:// or https://")
