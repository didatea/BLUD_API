from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'BPK'
apiPath = 'BLUD_BPK'
modelName = 'BPK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1),
    "IDUNIT": fields.Integer(required=True, example=1),
    "IDPHK3": fields.Integer(required=False, example=1001),
    "PENERIMA": fields.String(required=True, example="Tunai"),
    "NOBPK": fields.String(required=True, example="BPK-001"),
    "KDSTATUS": fields.String(required=True, example="LS"),
    "STATUS": fields.String(required=True, example="Tunai"),
    "IDJBAYAR": fields.Integer(required=False, example=1001),
    "PEMBAYARAN": fields.String(required=False, example="Tunai"),
    "IDXKODE": fields.Integer(required=False, example=0),
    "IDBEND": fields.Integer(required=True, example=201),
    "TGLBPK": fields.DateTime(required=False, example="2025-05-20 10:00:00"),
    "URAIBPK": fields.String(required=False, example="Pembayaran honor kegiatan"),
    "TGLVALID": fields.DateTime(required=False, example="2025-05-21 09:00:00"),
    "IDBERITA": fields.Integer(required=True, example=10),
    "KDRILIS": fields.Integer(required=True, example=1),
    "STKIRIM": fields.Integer(required=False, example=0),
    "STCAIR": fields.Integer(required=False, example=0),
    "NOREF": fields.String(required=True, example="REF-001"),
    "DATECREATE": fields.DateTime(required=False, example="2025-05-20 10:00:00"),
    "DATEUPDATE": fields.DateTime(required=False, example="2025-05-20 10:00:00"),
}
uniqueField = []
searchField = []
sortField = []
filterField = ["IDUNIT", "IDBEND"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'