from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'MPGRM'
apiPath = 'BLUD_MPGRM'
modelName = 'MPGRM'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDURUS": fields.Integer(required=True, example=1, ),
    "NMPRGRM": fields.String(required=True, max_length=512, ),
    "NUPRGRM": fields.String(required=True, max_length=5, example="", ),
    "IDPRIODA": NullableInteger(required=False, example=1, ),
    "IDPRIOPROV": NullableInteger(required=False, example=1, ),
    "IDPRIONAS": NullableInteger(required=False, example=1, ),
    "IDXKODE": NullableInteger(required=False, example=1, ),
    "STAKTIF": fields.Boolean(required=False, example=True, ),
    "STVALID": fields.Boolean(required=False, example=True, ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-02-28 20:12", ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 20:12", ),
}
uniqueField = []
searchField = ["NMPRGRM"]
sortField = ["NUPRGRM"]
filterField = ["IDURUS"]
enabledPagination = True
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'