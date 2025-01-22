from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'JBANK'
apiPath = 'BLUD_JBANK'
modelName = 'JBANK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDBANK": fields.String(required=True, max_length=10, example="", ),
    "NMBANK": fields.String(required=True, max_length=500, ),
    "URAIAN": fields.String(required=True, max_length=500, ),
    "AKRONIM": fields.String(required=False, max_length=200, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 20:05", ),

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