from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'DAFTURUS'
apiPath = 'BLUD_DAFTURUS'
modelName = 'DAFTURUS'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDURUS": fields.String(required=True, max_length=50, ),
    "NMURUS": fields.String(required=True, max_length=500, ),
    "KDLEVEL": fields.Integer(required=True, example=1, ),
    "TYPE": fields.String(required=True, max_length=5, example="", ),
    "AKROUNIT": fields.String(required=False, max_length=200, ),
    "ALAMAT": fields.String(required=False, max_length=200, ),
    "TELEPON": fields.String(required=False, max_length=200, ),
    "STAKTIF": NullableInteger(required=False, example=1, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 19:56", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-02-28 19:56", ),
}
uniqueField = []
searchField = ["NMURUS"]
sortField = ["NMURUS"]
filterField = ["IDURUS", "KDLEVEL", "TYPE", " KDURUS", "URUS"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'