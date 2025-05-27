from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'DPA'
apiPath = 'BLUD_DPA'
modelName = 'DPA'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "IDXKODE": fields.Integer(required=True, example=1, ),
    "NODPA": fields.String(required=False, max_length=5, example="", ),
    "TGLDPA": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "NOSAH": fields.String(required=False, max_length=5, example="", ),
    "KETERANGAN": fields.String(required=False, max_length=5, example="", ),
    "TGLVALID": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "DATECREATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "KDUNIT": NullableString(readonly=True, example="", ),
    "UNIT": NullableString(readonly=True, example="", ),
    "TAHAPAN": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = ["NODPA"]
filterField = ["IDUNIT", "IDXKODE", ""]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'