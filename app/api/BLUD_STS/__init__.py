from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'STS'
apiPath = 'BLUD_STS'
modelName = 'STS'
respAnSTSyloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "IDBEND": fields.Integer(required=True, example=1, ),
    "KDSTATUS": fields.String(required=False, max_length=5, example="", ),
    "IDXKODE": fields.Integer(required=True, example=1, ),
    "NOSTS": fields.String(required=False, max_length=5, example="", ),
    "TGLSTS": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "PENYETOR": fields.String(required=False, example="", ),
    "ALAMAT": fields.String(required=False, example="", ),
    "URAIAN": fields.String(required=False, example="", ),
    "TGLVALID": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "DATECREATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "KDUNIT": NullableString(readonly=True, example="", ),
    "UNIT": NullableString(readonly=True, example="", ),
    "URAISTATUS": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = ["NOSTS"]
filterField = ["IDUNIT", "IDXKODE", "IDBEND"]
enableSTSgination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'