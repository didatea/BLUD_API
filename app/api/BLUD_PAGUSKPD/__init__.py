from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'PAGUSKPD'
apiPath = 'BLUD_PAGUSKPD'
modelName = 'PAGUSKPD'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.Integer(required=True, example=1, ),
    "NILAIUP": fields.Fixed(required=False, ),
    "NILAI": fields.Fixed(required=False, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 19:56", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-02-28 19:56", ),
}
uniqueField = []
searchField = ["NMURUS"]
sortField = ["NMURUS"]
filterField = ["paguSkpd", "KDLEVEL", "TYPE", " KDURUS", "URUS"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'