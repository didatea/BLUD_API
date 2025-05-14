from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'DAFTPHK3'
apiPath = 'BLUD_DAFTPHK3'
modelName = 'DAFTPHK3'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "NMPHK3": fields.String(required=True, max_length=100, ),
    "NMINST": fields.String(required=True, max_length=100, ),
    "IDBANK": NullableInteger(required=False, example=1, ),
    "CABANGBANK": fields.String(required=True, max_length=200, ),
    "ALAMATBANK": fields.String(required=False, max_length=200, ),
    "NOREKBANK": fields.String(required=True, max_length=50, example="", ),
    "IDJUSAHA": NullableInteger(required=False, example=1, ),
    "ALAMAT": fields.String(required=False, max_length=100, ),
    "TELEPON": fields.String(required=False, max_length=100, ),
    "NPWP": fields.String(required=True, max_length=50, example="", ),
    "WARGANEGARA": fields.String(required=False, max_length=100, ),
    "STPENDUDUK": fields.String(required=False, max_length=100, ),
    "STVALID": NullableInteger(required=False, example=1, ),
    "NMBANK": fields.String(required=True, max_length=100, ),
}
uniqueField = []
searchField = ["NMBANK"]
sortField = []
filterField = ["NMBANK"]
enabledPagination = True
fileFields = []

# argsParser = reqparse.RequestParser()
# if fileFields:
#     for argKey in respAndPayloadFields.keys():
#         print(respAndPayloadFields[argKey], respAndPayloadFields[argKey].__dict__)
#         typeArg = str
#         if argKey in fileFields:
#             typeArg = FileStorage
#         else:
#             print(str(respAndPayloadFields[argKey]))
#             if 'NullableInteger' in str(respAndPayloadFields[argKey]):
#                 typeArg = int
#             elif 'Integer' in str(respAndPayloadFields[argKey]):
#                 typeArg = int
#             # elif 'Integer' in str(respAndPayloadFields[argKey]):
#             #     typeArg = int
#
#         argsParser.add_argument(
#             argKey,
#             required=respAndPayloadFields[argKey].required,
#             type=typeArg,
#             location="files" if argKey in fileFields else "form"
#         )
#         print(argsParser)

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'