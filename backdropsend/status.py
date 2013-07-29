from collections import namedtuple

class Status(namedtuple('Status', ['code', 'message'])):
    details = {}

    def description(self):
        return self.message.format(**self.details)
  
    def with_details(self, details):
        self.details = details
        return self
  
    def is_ok(self):
        return self.code == 0

OK = Status(0, "")
UNAUTHORIZED = Status(4, "Unable to send to backdrop. "
                "Unauthorised: check your access token.")
HTTP_ERROR = Status(8, "Unable to send to backdrop. Server responded with {status}. "
              "Error: {message}.")
CONNECTION_ERROR = Status(16, "Unable to send to backdrop. Connection error.")
TIMEOUT_ERROR = Status(32, "Unable to send to backdrop. Request timeout.")

