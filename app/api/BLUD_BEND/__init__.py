from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'BEND'
apiPath = 'BLUD_BEND'
modelName = 'BEND'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "JNSBEND": fields.String(required=True, max_length=2, example="", ),
    "IDPEG": fields.Integer(required=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "IDBANK": fields.Integer(required=True, example=1, ),
    "NMCABBANK": fields.String(required=False, max_length=100, ),
    "REKBEND": fields.String(required=True, max_length=50, example="", ),
    "NPWPBEND": fields.String(required=True, max_length=50, example="", ),
    "JABBEND": fields.String(required=True, max_length=100, ),
    "SALDOBEND": fields.Fixed(required=False, ),
    "SALDOBENDT": fields.Fixed(required=False, ),
    "TGLSTOPBEND": fields.DateTime(required=False, example="2024-02-28 19:58", ),
    "WARGANEGARA": fields.String(required=False, max_length=100, ),
    "STPENDUDUDUK": fields.String(required=False, max_length=100, ),
    "STAKTIF": NullableInteger(required=False, example=1, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 19:58", ),
    "NIP": fields.String(required=True, max_length=50, example="", ),
    "NAMA": fields.String(required=True, max_length=100, ),
}
uniqueField = []
searchField = ["NAMA", "NIP"]
sortField = []
filterField = ["IDUNIT"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'