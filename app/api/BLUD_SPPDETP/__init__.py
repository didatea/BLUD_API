from flask_restx import fields

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'SPPDETP'
apiPath = 'BLUD_SPPDETP'
modelName = 'SPPDETP'
respAnSPPDETPyloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDSPP": fields.Integer(required=True, example=1, ),
    "IDPAJAK": fields.Integer(required=True, example=1, ),
    "NILAI": fields.Fixed(required=False, ),
    "KETERANGAN": NullableString(readonly=True, example="", ),
    "IDBILLING": NullableString(readonly=True, example="", ),
    "TGLBILLING": fields.DateTime(required=False, example="2024-03-26 10:19", ),
    "NTPN": NullableString(readonly=True, example="", ),
    "NTB": NullableString(readonly=True, example="", ),
    "KDPAJAK": NullableString(readonly=True, example="", ),
    "NMPAJAK": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = []
sortField = [""]
filterField = [ "IDBERITA", "IDREK", "IDKEG", "IDSPP"]
enableSPPDETPgination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'