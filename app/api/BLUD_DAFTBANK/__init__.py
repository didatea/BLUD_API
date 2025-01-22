from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'DAFTBANK'
apiPath = 'BLUD_DAFTBANK'
modelName = 'DAFTBANK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDBANK": fields.Integer(required=False, example=1, ),
    "AKBANK": fields.String(required=False, max_length=100, ),
    "ALAMAT": fields.String(required=False, max_length=512, ),
    "TELEPON": fields.String(required=False, max_length=512, ),
    "CABANG": fields.String(required=False, max_length=512, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-03-21 11:07", )
}
uniqueField = []
searchField = ["AKBANK"]
sortField = []
filterField = ["AKBANK"]
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