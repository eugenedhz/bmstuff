from api.routes.schemas_config import JsonSchema
from marshmallow import fields, validate


class TodoSchema(JsonSchema):
	title = fields.Str(required=True, validate=validate.Length(min=1, max=150, error='INVALID_LENGTH'))
	text = fields.Str(required=True, validate=validate.Length(min=1, max=2000, error='INVALID_LENGTH'))
	date_to = fields.Date(required=True)
	date = fields.Date(required=True)


class TodoSchemaUpdate(JsonSchema):
	title = fields.Str(validate=validate.Length(min=1, max=150, error='INVALID_LENGTH'))
	text = fields.Str(validate=validate.Length(min=1, max=2000, error='INVALID_LENGTH'))
	date_to = fields.Date()
	date = fields.Date()