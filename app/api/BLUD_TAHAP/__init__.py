from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'TAHAP'
apiPath = 'BLUD_TAHAP'
modelName = 'TAHAP'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDTAHAP": fields.String(required=True, max_length=5, example="", ),
    "URAIAN": fields.String(required=True, max_length=512, ),
    "TGLTRANSFER": fields.DateTime(required=False, example="2024-04-01 11:07", ),

}
uniqueField = []
searchField = []
sortField = []
filterField = []
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'