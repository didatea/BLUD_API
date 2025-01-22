from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'RKAD'
apiPath = 'BLUD_RKAD'
modelName = 'RKAD'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.String(required=True, max_length=5, example="", ),
    "IDREK": fields.Integer(required=True, example=1, ),
    "NILAI": fields.Fixed(required=False, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-04-01 13:16", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-04-01 13:16", ),
    "UNIT": NullableString(readonly=True, example="", ),
    "REKENING": NullableString(readonly=True, example="", ),
    "TAHAPAN": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = []
filterField = []
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'