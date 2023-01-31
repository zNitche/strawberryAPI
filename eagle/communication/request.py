class Request:
    def __init__(self):
        self.protocol = None
        self.target = None
        self.method = None

        self.header = {}
        self.body = {}

    def parse_header(self, header_string):
        rs = header_string.replace("\r", "").split("\n")

        if len(rs) > 0:
            method, target, protocol = rs[0].split()

            self.protocol = protocol
            self.target = target
            self.method = method

            rs.pop(0)

            for raw_row in rs:
                row = raw_row.split(":")

                if len(row) == 2:
                    self.header[row[0].upper()] = row[1].strip()

    def parse_body(self, body_string):
        #TODO
        self.body = {"value": body_string}
