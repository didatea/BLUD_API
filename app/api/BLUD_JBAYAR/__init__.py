from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'JBAYAR'
apiPath = 'BLUD_JBAYAR'
modelName = 'JBAYAR'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDBAYAR": fields.Integer(required=True, example=1),
    "URAIANBAYAR": fields.String(required=True, max_length=500, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 20:05", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-02-28 20:05", ),

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