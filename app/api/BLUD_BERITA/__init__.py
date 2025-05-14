from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'BERITA'
apiPath = 'BLUD_BERITA'
modelName = 'BERITA'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "IDKEG": fields.Integer(required=True, example=1, ),
    "NOBERITA": fields.String(required=True, max_length=100, ),
    "TGLBA": fields.DateTime(required=True, example="2025-05-11 10:37", ),
    "IDKONTRAK": fields.Integer(required=True, example=1, ),
    "URAI_BERITA": fields.String(required=False, max_length=512, ),
    "TGLVALID": fields.DateTime(required=False, example="2025-05-11 10:37", ),
    "KDSTATUS": fields.String(required=False, max_length=3, example="", ),
    "LBLSTATUS": NullableString(readonly=True, example="", ),
}
uniqueField = []
searchField = ["NOBERITA"]
sortField = []
filterField = ["NOBERITA"]
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