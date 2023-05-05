from flask.views import MethodView
from flask_smorest import Blueprint
from schemas.schemas import FullNameSchema, FullNameResponseSchema

blp = Blueprint("fullnameAPI", __name__, description = "Combines first and last names by ID number")

@blp.route("/fullname")
class FullName(MethodView):

    @blp.arguments(FullNameSchema)
    @blp.response(200, FullNameResponseSchema)
    def post(self, body): 
        names = {x[1]:x[0] for x in body["first_names"]}
        surnames = {x[1]:x[0] for x in body["last_names"]}

        full_names=[]
        first_names=[]
        
        for x in names:
            if x in surnames.keys():
                full_names.append([names[x], surnames[x], x])
                surnames.pop(x)
            else:
                first_names.append([x, names[x]])
    
        unpaired={}
        if first_names:
            unpaired["first_names"] = first_names
        if surnames:
            unpaired["last_names"]=[[value, key] for key, value in surnames.items()]
        
        response = {"full_names": full_names}
        if unpaired:
            response["unpaired"] = unpaired

        return response