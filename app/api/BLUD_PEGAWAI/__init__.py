from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'PEGAWAI'
apiPath = 'BLUD_PEGAWAI'
modelName = 'PEGAWAI'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "NIP": fields.String(required=True, max_length=50, example="", ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "KDGOL": fields.String(required=True, max_length=10, example="", ),
    "NAMA": fields.String(required=False, max_length=200, ),
    "ALAMAT": fields.String(required=False, max_length=512, ),
    "JABATAN": fields.String(required=False, max_length=512, ),
    "PDDK": fields.String(required=False, max_length=30, ),
    "NPWP": fields.String(required=False, max_length=50, example="", ),
    "STAKTIF": fields.Boolean(required=False, example=True, ),
    "STVALID": fields.Boolean(required=False, example=True, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-02-28 20:08", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-02-28 20:08", ),
    "NMUNIT": fields.String(readonly=True),
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