class Message(object):
    """Brokest message structure."""

    def __init__(self, runnable_string, args, kwargs):
        self.runnable_string = runnable_string
        self.args = args
        self.kwargs = kwargs
