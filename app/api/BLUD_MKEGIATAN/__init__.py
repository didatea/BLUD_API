from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'MKEGIATAN'
apiPath = 'BLUD_MKEGIATAN'
modelName = 'MKEGIATAN'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDPRGRM": fields.Integer(required=True, example=1, ),
    "KDPERSPEKTIF": NullableInteger(required=False, example=1, ),
    "NUKEG": fields.String(required=True, max_length=30, example="", ),
    "NMKEGUNIT": fields.String(required=True, max_length=512, ),
    "LEVELKEG": fields.Integer(required=True, example=1, ),
    "TYPE": fields.String(required=True, max_length=5, example="", ),
    "parent_id": NullableInteger(required=False, example=1, ),
    "STAKTIF": fields.Boolean(required=False, example=True, ),
    "STVALID": fields.Boolean(required=False, example=True, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 20:07", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-02-28 20:07", ),
    "has_child": fields.Boolean(readonly=True),
    "LOOKUP": fields.String(required=True, max_length=5, example="", ),
}
uniqueField = []
searchField = ["NMKEGUNIT"]
sortField = ["NUKEG", "LEVELKEG", "TYPE"]
filterField = ["IDPRGRM", "LEVELKEG", "parent_id", "LOOKUP" ]
enabledPagination = True
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'