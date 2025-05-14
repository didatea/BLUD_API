from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'KONTRAK'
apiPath = 'BLUD_KONTRAK'
modelName = 'KONTRAK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "NOKONTRAK": fields.String(required=True, max_length=100, ),
    "IDPHK3": fields.Integer(required=True, example=1, ),
    "IDKEG": fields.Integer(required=True, example=1, ),
    "TGLKON": fields.DateTime(required=False, example="2025-05-10 21:55", ),
    "TGLAWALKONTRAK": fields.DateTime(required=False, example="2025-05-10 21:55", ),
    "TGLAKHIRKONTRAK": fields.DateTime(required=False, example="2025-05-10 21:55", ),
    "URAIAN": fields.String(required=False, max_length=512, ),
    "NILAI": fields.Fixed(required=False, ),
    "NMPHK3": fields.String(required=True, max_length=100, ),
}
uniqueField = []
searchField = ["NMPHK3"]
sortField = []
filterField = ["NMPHK3"]
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