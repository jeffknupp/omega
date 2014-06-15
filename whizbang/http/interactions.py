from werkzeug import Response
from whi
class CRUD(object):
    def __init__(self, name, definition):
        self.name = name
        self.definition = definition

    def __call__(self, request):
        if request.method == 'POST':
            return self.create(request)
        elif request.method == 'GET':
            return self.collection(request)
        elif request.method == 'DELETE':
            return self.delete(request)
    def create(self, request):
        for field in self.definition:
            if field not in request.json:
                return 'bad'
        request.json 
