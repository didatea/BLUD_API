from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'APPSETT'
apiPath = 'BLUD_APPSETT'
modelName = 'APPSETT'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDSET": fields.String(required=False, max_length=50, example="", ),
    "VALSET": fields.String(required=False, example=50, ),
    "VALDESC": fields.String(required=False, max_length=100, example="", ),
    "MODEENTRY": fields.Integer(required=True, example=1, ),
    "VALLIST": fields.String(required=False,max_length=100, example="", ),
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