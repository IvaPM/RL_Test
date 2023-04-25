from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.schemas import FullNameSchema, FullNameResponseSchema

blp = Blueprint("fullnameAPI", __name__, description = "Combines first and last names by ID number")

@blp.route("/fullname")
class FullName(MethodView):
    @blp.arguments(FullNameSchema)
    @blp.response(200, FullNameResponseSchema)
    def post(self, body):
        
        names = sorted(body["first_names"], key=lambda x: int(x[1]))
        surnames = sorted(body["last_names"], key=lambda x: int(x[1]))

        full_names = [list([x[0]]+y) for x in names for y in surnames if x[1]==y[1]]
        
        unpaired={}

        [names.remove(x) for x in body["first_names"] for y in full_names if x[1]==y[2] if x in names]
        if names:
            unpaired["first_names"]=names
    
        [surnames.remove(x) for x in body["last_names"] for y in full_names if x[1]==y[2] if x in surnames]
        if surnames:
            unpaired["last_names"]=surnames
        

        response = {"full_names": full_names}
        if len(unpaired)>0:
            response["unpaired"] = unpaired

        return response