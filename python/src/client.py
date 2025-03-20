from openapi import Error, PutTodoEndpoint
from python.openapi import Token, PotentialTodoDto
from python.shared import Wirespec

def handle(req:Wirespec.Request):
    return req.queries