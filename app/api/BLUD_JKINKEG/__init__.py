from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'JKINKEG'
apiPath = 'BLUD_JKINKEG'
modelName = 'JKINKEG'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "URJKK": fields.String(required=True, max_length=2, example="", ),

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