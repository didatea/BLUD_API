from flask_restx import fields, reqparse
from werkzeug.datastructures import FileStorage

from app.utils import NullableString, NullableInteger

moduleTitle = ''
crudTitle = 'asetBulan'
apiPath = 'asetBulan'
modelName = 'asetBulan'
respAndPayloadFields = {
"id": fields.Integer(readonly=True, example=1, ),
"nama": fields.String(required=True, max_length=100, example="", ),
"semester": fields.Integer(required=False, example=1, ),
"triwulan": fields.Integer(required=False, example=1, ),
}
uniqueField = ["nama"]
searchField = ["nama"]
sortField = ["id"]
filterField = ["semester", "triwulan", "periode", "tahun"]
enabledPagination = False
fileFields = []

######################### GEN
moduleName = moduleTitle.replace(' ', '_').lower() + '_' if moduleTitle and len(moduleTitle) > 0 else ''
crudName = crudTitle.replace(' ', '_').lower() if crudTitle else ''
apiName = f'{moduleTitle} - {crudTitle}'
docName = f'{moduleName}{crudName}'