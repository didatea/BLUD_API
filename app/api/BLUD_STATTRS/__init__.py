from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'STATTRS'
apiPath = 'BLUD_STATTRS'
modelName = 'STATTRS'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDSTATUS": fields.String(required=True, max_length=30, ),
    "LBLSTATUS": fields.String(required=True, max_length=30, ),
    "URAIAN": fields.String(required=True, max_length=30, ),
}
uniqueField = []
searchField = []
sortField = []
filterField = ["jenisBukti"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'