from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'KINKEG'
apiPath = 'BLUD_KINKEG'
modelName = 'KINKEG'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "KDJKK": fields.Integer(required=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.String(required=True, max_length=5, example="", ),
    "IDKEG": fields.Integer(required=True, example=1, ),
    "TOLOKUR": NullableString(required=False, max_length=4096, example="", ),
    "TARGET": NullableString(required=False, max_length=4096, example="", ),
    "DATECREATE": fields.DateTime(required=False, example="2024-06-09 20:11", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-06-09 20:11", ),

}
uniqueField = []
searchField = ["KDPER", "NMPER"]
sortField = []
filterField = ["parent_id", "MTGLEVEL", "TYPE", "kinkeg"]
enabledPagination = False
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