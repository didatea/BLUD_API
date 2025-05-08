from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'DPAB'
apiPath = 'BLUD_DPAB'
modelName = 'DPAB'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDDPA": fields.Integer(required=True, example=1, ),
    "IDREK": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.String(required=True, max_length=5, example="", ),
    "NILAI": fields.Fixed(required=False, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "REKENING": NullableString(readonly=True, example="", ),
    "TAHAPAN": NullableString(readonly=True, example="", ),

}
uniqueField = []
searchField = []
sortField = ["IDREK"]
filterField = ["IDDPA", "biaya"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'