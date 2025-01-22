from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'PEMDA'
apiPath = 'BLUD_PEMDA'
modelName = 'PEMDA'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "CONFIGID": fields.String(required=True, max_length=50, example="", ),
    "CONFIGVAL": fields.String(required=True, example=50, ),
    "CONFIGDES": fields.String(required=False, max_length=100, example="", ),

}
uniqueField = []
searchField = ["CONFIGID", "CONFIGVAL", "CONFIGDES"]
sortField = ["id"]
filterField = ['CONFIGID', 'CONFIGDES']
enabledPagination = True
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'