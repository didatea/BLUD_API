from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'JNSAKUN'
apiPath = 'BLUD_JNSAKUN'
modelName = 'JNSAKUN'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "URAIAKUN": fields.String(required=False, max_length=50, ),
    "KDPERS": fields.String(required=False, max_length=1, example="", ),
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