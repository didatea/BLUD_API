from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'JREK'
apiPath = 'BLUD_JREK'
modelName = 'JREK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "URAIAN": fields.String(required=True, max_length=512, ),
}
uniqueField = []
searchField = []
sortField = []
filterField = ["id", "URAIAN"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'