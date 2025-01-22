from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'PGRMUNIT'
apiPath = 'BLUD_PGRMUNIT'
modelName = 'PGRMUNIT'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.Integer(required=True, example=1, ),
    "IDPRGRM": fields.Integer(required=True, example=1, ),
    "TARGET": fields.String(required=False, max_length=200, ),
    "SASARAN": fields.String(required=False, max_length=200, ),
    "NOPRIO": NullableInteger(required=False, example=1, ),
    "INDIKATOR": fields.String(required=False, max_length=200, ),
    "KET": fields.String(required=False, max_length=200, ),
    "IDSAS": NullableString(required=False, max_length=10, example="", ),
    "TGLVALID": fields.DateTime(required=False, example="2024-06-09 10:35", ),
    "IDXKODE": NullableInteger(required=False, example=1, ),
    "DATECREATE": fields.DateTime(required=False, example="2024-06-09 10:35", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-06-09 10:35", ),
    "NMPRGRM": fields.String(readonly=True),
    "NUPRGRM": fields.String(readonly=True),

}
uniqueField = ["IDPRGRM"]
searchField = [""]
sortField = [""]
filterField = ["parent_id", "MTGLEVEL", "TYPE", "KDTAHAP" ]
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