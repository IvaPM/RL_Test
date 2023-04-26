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
        braces_index = []
        response_text = str()
        index = 1
        for c in txt:
            if c in braces_dict.keys():
                braces_stack.append(c)
                braces_index.append(index)
            elif c in braces_dict.values():
                if not braces_stack:
                    response_text += c
                    return {"response_text": response_text + " << brace is unbalanced"}, 400
                else:
                    last_opened_brace = braces_stack.pop()
                    unbalanced_brace_position = braces_index.pop()
                    if c not in braces_dict[last_opened_brace]:
                        response_text=response_text[:unbalanced_brace_position]
                        return {"response_text": response_text + " << brace is unbalanced"}, 400        
            index+=1 
            response_text += c
           
        if braces_stack:
            unbalanced_brace_position = braces_index[0]
            response_text=response_text[:unbalanced_brace_position]
            return {"response_text": response_text + " << brace is unbalanced"}, 400
        else:
            response_text={"response_text": "Braces are balanced."}
        
        return  response_text