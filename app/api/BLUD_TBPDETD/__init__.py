from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'TBPDETD'
apiPath = 'BLUD_TBPDETD'
modelName = 'TBPDETD'
respAnTBPDETDyloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "IDTBP": fields.Integer(required=True, example=1, ),
    "IDREK": fields.Integer(required=True, example=1, ),
    "NILAI": fields.Fixed(required=False, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "KDUNIT": NullableString(readonly=True, example="", ),
    "UNIT": NullableString(readonly=True, example="", ),
    "KDREKENING": NullableString(readonly=True, example="", ),
    "REKENING": NullableString(readonly=True, example="", ),
    # "URAISTATUS": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = [""]
filterField = ["IDUNIT", "IDTBP", "IDREK"]
enableTBPDETDgination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'