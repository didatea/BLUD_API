from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = ''
apiPath = 'BLUD_DAFTREKENING'
modelName = 'DAFTREKENING'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDPER": fields.String(required=True, max_length=50, ),
    "NMPER": fields.String(required=True, max_length=512, ),
    "MTGLEVEL": fields.Integer(required=True, example=1, ),
    "KDKHUSUS": fields.Integer(required=True, example=1, ),
    "JNSREK": fields.Integer(required=True, example=1, ),
    "IDJNSAKUN": NullableInteger(required=False, example=1, ),
    "TYPE": fields.String(required=True, max_length=2, example="", ),
    "STAKTIF": NullableInteger(required=False, example=1, ),
    "parent_id": fields.Integer(readonly=True, example=1, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-03-25 11:28", ),
    "NMREK": NullableString(readonly=True, example="", ),
    "has_child": fields.Boolean(readonly=True),

}
uniqueField = ["KDPER"]
searchField = ["KDPER", "NMPER"]
sortField = ["KDPER"]
filterField = ["MTGLEVEL", "parent_id"]
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