from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'BENDKEG'
apiPath = 'BLUD_BENDKEG'
modelName = 'BENDKEG'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "IDBEND": fields.Integer(required=True, example=1, ),
    "IDKEG": fields.Integer(required=False, example=1, ),
    "NAMA": fields.String(readonly=True),
    "NUKEG": fields.String(readonly=True),
    "NMKEGUNIT": fields.String(readonly=True),
}
uniqueField = []
searchField = []
sortField = [""]
filterField = ["IDUNIT", "IDBEND"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'