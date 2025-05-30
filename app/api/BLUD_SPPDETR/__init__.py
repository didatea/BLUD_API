from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'SPPDETR'
apiPath = 'BLUD_SPPDETR'
modelName = 'SPPDETR'
respAnSPPDETRyloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDREK": fields.Integer(required=True, example=1, ),
    "IDKEG": fields.Integer(required=True, example=1, ),
    "IDSPP": fields.Integer(required=True, example=1, ),
    "IDNOJETRA": fields.Integer(required=True, example=1, ),
    "NILAI": fields.Fixed(required=False, ),
    "KDPER": NullableString(readonly=True, example="", ),
    "NMPER": NullableString(readonly=True, example="", ),
    "NMKEGUNIT": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = [""]
filterField = [ "IDBERITA", "IDREK", "IDKEG", "IDSPP"]
enableSPPDETRgination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'