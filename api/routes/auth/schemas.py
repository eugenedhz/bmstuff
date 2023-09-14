from api.routes.schemas_config import JsonSchema
from marshmallow import fields, validate


class LoginAndSignupSchema(JsonSchema):
	username = fields.Str(required=True, validate=validate.Length(min=1, max=64, error='INVALID_LENGTH'))
	password = fields.Str(required=True, validate=validate.Length(min=1, error='INVALID_LENGTH'))