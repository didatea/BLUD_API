from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'GOLONGAN'
apiPath = 'BLUD_GOLONGAN'
modelName = 'GOLONGAN'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDGOL": fields.String(required=True, max_length=10, example="", ),
    "NMGOL": fields.String(required=False, max_length=50, ),
    "PANGKAT": fields.String(required=False, max_length=30, ),
    "KDGOL_STRIP": fields.String(readonly=True, ),
}
uniqueField = []
searchField = ['NMGOL',]
sortField = ['NMGOL']
filterField = ['NMGOL','KDGOL']
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'