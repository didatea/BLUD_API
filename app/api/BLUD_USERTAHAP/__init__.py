from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'USERTAHAP'
apiPath = 'BLUD_USERTAHAP'
modelName = 'USERTAHAP'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDTAHAP": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.String(required=True, max_length=5, example="", ),
    "USERID": fields.String(required=True, max_length=512, ),
    "URAIAN": fields.String(required=False, max_length=512, ),
}
uniqueField = []
searchField = []
sortField = ["KDTAHAP"]
filterField = ["USERID", "KDTAHAP"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'