from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'KEGUNIT'
apiPath = 'BLUD_KEGUNIT'
modelName = 'KEGUNIT'
respAndPayloadFields = {
    "id": fields.Integer(readonly=True, example=1, ),
    "IDUNIT": fields.Integer(required=True, example=1, ),
    "IDKEG": fields.Integer(required=True, example=1, ),
    "KDTAHAP": fields.String(required=True, max_length=5, example="", ),
    "IDPRGRM": fields.Integer(required=True, example=1, ),
    "NOPRIOR": NullableInteger(required=False, example=1, ),
    "IDSIFATKEG": fields.Integer(required=True, example=1, ),
    "IDPEG": NullableInteger(required=False, example=1, ),
    "TGLAKHIR": fields.DateTime(required=False, example="2024-06-09 10:29", ),
    "TGLAWAL": fields.DateTime(required=False, example="2024-06-09 10:29", ),
    "TARGETP": fields.Fixed(required=False, ),
    "LOKASI": fields.String(required=False, max_length=512, ),
    "JUMLAHMIN1": fields.Fixed(required=False, ),
    "PAGU": fields.Fixed(required=False, ),
    "JUMLAHPLS1": fields.Fixed(required=False, ),
    "SASARAN": fields.String(required=False, max_length=512, ),
    "KETKEG": fields.String(required=False, max_length=512, ),
    "IDPRIODA": fields.String(required=False, max_length=36, example="", ),
    "IDSAS": fields.String(required=False, max_length=36, example="", ),
    "TARGET": fields.String(required=False, max_length=10, example="", ),
    "TARGETIF": fields.String(required=False, max_length=10, example="", ),
    "TARGETSEN": fields.String(required=False, max_length=10, example="", ),
    "VOLUME": fields.String(required=False, max_length=10, example="", ),
    "VOLUME1": fields.String(required=False, max_length=10, example="", ),
    "SATUAN": fields.String(required=False, max_length=30, example="", ),
    "PAGUPLUS": fields.Fixed(required=False, ),
    "PAGUTIF": fields.Fixed(required=False, ),
    "TGLVALID": fields.DateTime(required=False, example="2024-06-09 10:29", ),
    "DATECREATE": fields.DateTime(required=False, example="2024-06-09 10:29", ),
    "DATEUPDATE": fields.DateTime(required=False, example="2024-06-09 10:29", ),

}
uniqueField = ["KDPER"]
searchField = ["KDPER", "NMPER"]
sortField = ["KDPER"]
filterField = ["parent_id", "MTGLEVEL", "TYPE" ]
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