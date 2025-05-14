from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'PAJAK'
apiPath = 'BLUD_PAJAK'
modelName = 'PAJAK'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDPAJAK": fields.String(required=False, max_length=10, example="", ),
    "NMPAJAK": fields.String(required=True, max_length=512, ),
    "URAIAN": fields.String(required=False, max_length=512, ),
    "RUMUSPAJAK": fields.String(required=False, max_length=36, example="", ),
    "IDJNSPAJAK": NullableInteger(required=False, example=1, ),
    "STAKTIF": NullableInteger(required=False, example=1, ),
    "NMJNSPAJAK": fields.String(required=False, max_length=50, ),
}
uniqueField = []
searchField = ["KDPAJAK"]
sortField = []
filterField = ["KDPAJAK"]
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