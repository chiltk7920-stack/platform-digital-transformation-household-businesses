from marshmallow import Schema, fields

class CustomerRequestSchema(Schema):
    household_id = fields.Int(required=False, allow_none=True)
    tax_code = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False, allow_none=False)
    created_by = fields.Str(required=False, allow_none=True)

class CustomerResponseSchema(Schema):
    id = fields.Int(required=True)
    household_id = fields.Int(required=False, allow_none=True)
    tax_code = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_by = fields.Str(required=False, allow_none=True)
    updated_by = fields.Str(required=False, allow_none=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class CustomerUpdateSchema(Schema):
    household_id = fields.Int(required=False, allow_none=True)
    tax_code = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False)
    updated_by = fields.Str(required=False, allow_none=True)
