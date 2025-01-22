from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'JBEND'
apiPath = 'BLUD_JBEND'
modelName = 'JBEND'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "JNSBEND": fields.String(required=True, max_length=2, example="", ),
    "IDREK": fields.Integer(required=True, example=1, ),
    "URAIBEND": fields.String(required=False, max_length=100, example="", ),

}
uniqueField = []
searchField = ['AKBANK',]
sortField = ['AKBANK']
filterField = ['KDBANK','AKBANK']
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'