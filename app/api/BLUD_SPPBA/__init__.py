from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'SPPBA'
apiPath = 'BLUD_SPPBA'
modelName = 'SPPBA'
respAnSPPBAyloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDSPP": fields.Integer(required=True, example=1, ),
    "IDBERITA": fields.Integer(required=True, example=1, ),
    "NOBERITA": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = [""]
filterField = [ "IDBERITA", "IDSPP"]
enableSPPBAgination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'