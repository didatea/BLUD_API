from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'SPP'
apiPath = 'BLUD_SPP'
modelName = 'SPP'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "NOSPP": fields.String(required=True, max_length=100, ),
    "KDSTATUS": fields.String(required=True, max_length=3, example="", ),
    "IDBEND": NullableInteger(required=False, example=1, ),
    "IDPHK3": NullableInteger(required=False, example=1, ),
    "IDXKODE": fields.Integer(required=True, example=1, ),
    "NOKONTRAK": fields.String(required=False, max_length=100, ),
    "KEPERLUAN": fields.String(required=False, max_length=1024, ),
    "PENOLAKAN": fields.String(required=False, max_length=10, example="", ),
    "TGLVALID": fields.DateTime(required=False, example="2025-05-11 22:34", ),
    "TGLSPP": fields.DateTime(required=False, example="2025-05-11 22:34", ),
    "STATUS": fields.Integer(required=False, max_length=10, example=0, ),
}
uniqueField = []
searchField = []
sortField = ["NOSPP"]
filterField = ["IDUNIT", "IDXKODE", "IDBEND", "KDSTATUS"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'