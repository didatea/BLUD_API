from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'STRUREK'
apiPath = 'BLUD_STRUREK'
modelName = 'STRUREK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "MTGLEVEL": fields.Integer(required=True, example=1, ),
    "NMLEVEL": fields.String(required=True, max_length=30, ),
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