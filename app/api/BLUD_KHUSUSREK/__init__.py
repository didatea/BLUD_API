from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'KHUSUSREK'
apiPath = 'BLUD_KHUSUSREK'
modelName = 'KHUSUSREK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDKHUSUS": fields.Integer(required=True, example=1, ),
    "NMKHUSUS": fields.String(required=False, max_length=512, ),
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