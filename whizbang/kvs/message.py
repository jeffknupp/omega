class CommandMessage(object):

    def __init__(self, command, value):
        self.command = command
        self.value = value


class StatusMessage(object):
    def __init__(self, outcome, value=None):
        self.outcome = outcome
        self.value = value

    def __eq__(self, other):
        return self.outcome == other.outcome and self.value == other.value
