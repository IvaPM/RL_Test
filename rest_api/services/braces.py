import re
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.schemas import Braces, BracesResponse

blp = Blueprint("bracesAPI", __name__, description = "Checks if the braces are balanced.")

@blp.route("/braces")
class Braces(MethodView):

    @blp.arguments(Braces, content_type = "text/plain")
    @blp.response(200, BracesResponse)
    def post(self, text):
        txt = re.sub("[\n\t\r]", "", str(request.get_data(as_text = True)))
        
        if not re.search("[\(\)\[\]\{\}]", txt):
            return {"response_text": "There are no braces in the given input"}
        
        braces_dict = {"(":")", "{":"}", "[":"]"}
        braces_stack = []
        response_text = str()
        
        for index, c in enumerate(txt):
            if c in braces_dict.keys():
                braces_stack.append({index+1:c})
            elif c in braces_dict.values():
                if not braces_stack:
                    response_text += c
                    return {"response_text": response_text + " << brace is unbalanced"}, 400
                else:
                    last_opened_brace = braces_stack.pop()
                    val = list(last_opened_brace.values())
                    i = list(last_opened_brace.keys())
                    if c not in braces_dict[val[0]]:
                        response_text=response_text[:i[0]]
                        return {"response_text": response_text + " << brace is unbalanced"}, 400        
            response_text += c
           
        if braces_stack:
            unbalanced_brace_position = list(braces_stack[0].keys())
            response_text=response_text[:unbalanced_brace_position[0]]
            return {"response_text": response_text + " << brace is unbalanced"}, 400
        else:
            response_text={"response_text": "Braces are balanced."}
        
        return  response_text