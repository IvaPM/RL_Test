from marshmallow import Schema, fields, ValidationError, validate, post_load

class FullNameSchema(Schema):
    first_names = fields.List(fields.List(fields.String(), validate = validate.Length(equal = 2)), required = True)
    last_names = fields.List(fields.List(fields.String(), validate = validate.Length(equal = 2)), required = True)

    @post_load
    def unwrap_first_names(self, data, **kwargs):
        try:
            data["first_names"] = sorted(data["first_names"], key=lambda x: int(x[1]))
            data["last_names"] = sorted(data["last_names"], key=lambda x: int(x[1]))
        except:
            raise ValidationError("Id string must contain digits only")
        
        return data


class FullNameResponseSchema(Schema):
    full_names = fields.List(fields.List(fields.String(), validate = validate.Length(equal = 3)), dump_only = True)
    unpaired = fields.Nested(FullNameSchema, dump_only = True)

class Braces(Schema):
    fields.Str(required = True, validate = validate.Length(min = 1))


class BracesResponse(Schema):
    response_text = fields.Str()
    