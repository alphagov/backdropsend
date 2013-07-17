
class Status():
    def __init__(self, message, code):
        self.code = code
        self.message = message
        self.details = {}
  
    def description(self):
        return self.message.format(**self.details)
  
    def with_details(self, details):
        self.details = details
        return self
  
    def is_ok(self):
        return self.code == 0

OK = Status("", 0)
UNAUTHORIZED = Status("Unable to send to backdrop. "
                "Unauthorised: check your access token.", 4)
HTTP_ERROR = Status("Unable to send to backdrop. Server responded with {status}. "
              "Error: {message}.", 8)
CONNECTION_ERROR = Status("Unable to send to backdrop. Connection error.", 16)

