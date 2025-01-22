from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'DAFTUNIT'
apiPath = 'BLUD_DAFTUNIT'
modelName = 'DAFTUNIT'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDURUS": NullableInteger(required=False, example=1, ),
    "KDUNIT": fields.String(required=True, max_length=50, ),
    "NMUNIT": fields.String(required=True, max_length=500, ),
    "KDLEVEL": fields.Integer(required=True, example=1, ),
    "TYPE": fields.String(required=True, max_length=1, example="", ),
    "AKROUNIT": fields.String(required=False, max_length=200, ),
    "ALAMAT": fields.String(required=False, max_length=200, ),
    "TELEPON": fields.String(required=False, max_length=200, ),
    "STAKTIF": NullableInteger(required=False, example=1, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 20:04", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-02-28 20:04", ),
    "has_child": fields.Boolean(readonly=True),
    "parent_id": fields.Integer(readonly=False, example=1, ),
    "jns": fields.String(readonly=False, max_length=200, ),
}
uniqueField = []
searchField = ["NMUNIT"]
sortField = ["KDUNIT"]
filterField = ["IDURUS", "parent_id", "jns"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'