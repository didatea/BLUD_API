from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'DPADETD'
apiPath = 'BLUD_DPADETD'
modelName = 'DPADETD'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.String(required=True, max_length=5, example="", ),
    "IDREK": fields.Integer(required=True, example=1, ),
    "IDDPAD": fields.Integer(required=True, example=1, ),
    "KDJABAR": fields.String(required=True, max_length=5, example="", ),
    "URAIAN": fields.String(required=True, max_length=5, example="", ),
    "JUMBYEK": fields.Fixed(required=False, ),
    "SATUAN": fields.String(required=True, max_length=5, example="", ),
    "TARIF": fields.Fixed(required=False, ),
    "SUBTOTAL": fields.Fixed(required=False, ),
    "EKSPRESI": fields.String(required=True, max_length=5, example="", ),
    "INCLSUBTOTAL": NullableString(readonly=True, example="", ),
    "TYPE": NullableString(readonly=True, example="", ),
    "IDSTDHARGA": fields.String(required=True, max_length=5, example="", ),
    "DATECREATE": fields.DateTime(required=False, example="2024-04-01 13:16", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-04-01 13:16", ),
    "UNIT": NullableString(readonly=True, example="", ),
    "KDREKENING": NullableString(readonly=True, example="", ),
    "REKENING": NullableString(readonly=True, example="", ),
    "TAHAPAN": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = ["KDJABAR"]
filterField = ["IDUNIT", "IDDPAD", "id"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'