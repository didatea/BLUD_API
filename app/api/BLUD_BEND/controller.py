import decimal
import json
import math
from _pydecimal import Decimal
from cgitb import text
from datetime import datetime

import sqlalchemy
from flask import request, current_app, jsonify, Flask
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import Null

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, generateDefaultResponse, message, \
    error_response, DateTimeEncoder, logger
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .model import BEND
from .service import Service
from ..BLUD_DAFTBANK.model import DAFTBANK
from ... import internalApi_byUrl, db
from ...sso_helper import token_required, current_user

api = doc.api

parser = reqparse.RequestParser()
parser.add_argument('fetch_child', type=inputs.boolean, help='boolean input for fetch unit children', default=True)

parser.add_argument('sort', type=str, help='for sorting, fill with column name')
parser.add_argument('sort_dir', type=str, choices=('asc', 'desc'), help='fill with "asc" or "desc"')


#### LIST
@api.route("")
class List(Resource):
    if enabledPagination:
        parser.add_argument('page', type=int, help='page/start, fill with number')
        parser.add_argument('length', type=int, help='length of data, fill with number')
        parser.add_argument('search', type=str, help='for filter searching')
    if 'parent_id' in respAndPayloadFields:
        parser.add_argument('flat_mode', type=inputs.boolean, default=False, help='flat response data')
    if filterField:
        for row in filterField:
            parser.add_argument(row.split(":")[2] if len(row.split(":")) > 2 else row.split(":")[0])
    import sqlalchemy
    from datetime import datetime
    from flask import jsonify

    #### GET
    @doc.getRespDoc
    @api.expect(parser)
    @token_required
    def get(self):
        return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)
        # resultFinal = {'input_data': request.args}  # Add input_data to resultFinal
        # try:
        #     sqlQuery = "SELECT b.id, b.NMCABBANK, b.REKBEND, b.NPWPBEND, b.IDPEG, b.JNSBEND, b.IDBANK, b.JABBEND," \
        #                "b.SALDOBEND, b.SALDOBENDT, b.TGLSTOPBEND, b.STAKTIF, j.JNSBEND, j.URAIBEND, j.IDREK, p.NIP," \
        #                "p.NAMA, p.JABATAN, p.NPWP, p.IDUNIT " \
        #                "FROM BEND AS b " \
        #                "LEFT JOIN JBEND AS j ON j.JNSBEND = b.JNSBEND " \
        #                "LEFT JOIN PEGAWAI AS p ON p.id = b.IDPEG"
        #
        #     print(sqlQuery)
        #     select_query = db.engine.execute(sqlQuery)
        #     results = [dict(row) for row in select_query]
        #
        #     if results:
        #         data = []
        #         for row in results:
        #             tgl_stop_bend = row['TGLSTOPBEND'].date() if row['TGLSTOPBEND'] else None
        #             # Konversi objek date menjadi string format ISO
        #             tgl_stop_bend_str = tgl_stop_bend.isoformat() if tgl_stop_bend else None
        #             data.append({
        #                 'id': row['id'],
        #                 'NMCABBANK': str(row['NMCABBANK']).rstrip() if row['NMCABBANK'] else None,
        #                 'REKBEND': str(row['REKBEND']).rstrip() if row['REKBEND'] else None,
        #                 'NPWPBEND': str(row['NPWPBEND']).rstrip() if row['NPWPBEND'] else None,
        #                 'IDPEG': str(row['IDPEG']).rstrip() if row['IDPEG'] else None,
        #                 'IDBANK': str(row['IDBANK']).rstrip() if row['IDBANK'] else None,
        #                 'JABBEND': str(row['JABBEND']).rstrip() if row['JABBEND'] else None,
        #                 'SALDOBEND': str(row['SALDOBEND']).rstrip() if row['SALDOBEND'] else None,
        #                 'SALDOBENDT': str(row['SALDOBENDT']).rstrip() if row['SALDOBENDT'] else None,
        #                 'TGLSTOPBEND': tgl_stop_bend_str,
        #                 'STAKTIF': str(row['STAKTIF']).rstrip() if row['STAKTIF'] else None,
        #                 'JNSBEND': str(row['JNSBEND']).rstrip() if row['JNSBEND'] else None,
        #                 'URAIBEND': str(row['URAIBEND']).rstrip() if row['URAIBEND'] else None,
        #                 'IDREK': str(row['IDREK']).rstrip() if row['IDREK'] else None,
        #                 'NIP': str(row['NIP']).rstrip() if row['NIP'] else None,
        #                 'NAMA': str(row['NAMA']).rstrip() if row['NAMA'] else None,
        #                 'JABATAN': str(row['JABATAN']).rstrip() if row['JABATAN'] else None,
        #                 'NPWP': str(row['NPWP']).rstrip() if row['NPWP'] else None,
        #                 'IDUNIT': str(row['IDUNIT']).rstrip() if row['IDUNIT'] else None,
        #             })
        #         resultFinal['data'] = data
        #         return resultFinal, 200
        #     else:
        #         return {'message': 'No data found'}, 404
        #
        # except Exception as e:
        #     resultFinal = {'message': 'Get data failed!', 'status': False}
        #     logger.error(e)
        #     return resultFinal, 500

    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):

        return GeneralPost(doc, crudTitle, Service, request)

    #### MULTIPLE-DELETE
    @doc.deleteMultiRespDoc
    @api.expect(doc.default_delete_multi_payload, validate=True)
    @token_required
    def delete(self):
        return GeneralDelete(crudTitle, Service, request, fileFields, modelName, current_user, internalApi_byUrl)


#### BY ID
@api.route("/<int:id>")
class ById(Resource):
    #### GET
    @doc.getByIdRespDoc
    @token_required
    def get(self, id):
        # resultFinal = []
        # try:
        #     sqlQuery = f"""
        #         SELECT d.AKBANK, b.NMCABBANK, b.REKBEND, b.NPWPBEND, b.IDPEG, b.JNSBEND, b.IDBANK, b.JABBEND,
        #                b.SALDOBEND, b.SALDOBENDT, b.id, b.TGLSTOPBEND, b.STAKTIF, j.JNSBEND, j.URAIBEND,
        #                j.IDREK, p.NIP, p.NAMA, p.JABATAN, p.NPWP, p.IDUNIT
        #         FROM BEND AS b
        #         LEFT OUTER JOIN JBEND AS j ON j.JNSBEND = b.JNSBEND
        #         LEFT OUTER JOIN PEGAWAI AS p ON p.id = b.IDPEG
        #         LEFT JOIN DAFTBANK AS d ON d.id = b.IDBANK
        #         WHERE b.id = {id};
        #     """
        #     select_query = db.engine.execute(sqlQuery)
        #     results = [dict(row) for row in select_query]
        #     resultStr = json.dumps(results, cls=DateTimeEncoder)
        #     result = json.loads(resultStr)
        #     if result:
        #         resultFinal = result[0]
        #         resultFinal['id'] = result[0]['id']
        #         # Proses .rstrip() untuk setiap nilai dalam resultFinal
        #         for key, value in resultFinal.items():
        #             if isinstance(value, str):
        #                 resultFinal[key] = value.rstrip()
        #
        #         return {
        #             "message": "Success",
        #             "status": True,
        #             "data": resultFinal
        #         }, 200
        # except Exception as e:
        #     logger.error(e)
        #     return {
        #         "message": "Error",
        #         "status": False,
        #         "data": resultFinal
        #     }, 500
        return GeneralGetById(id, doc, crudTitle, Service)

    #### PUT
    @doc.putRespDoc
    @api.expect(doc.default_data_response)
    @token_required
    def put(self, id):
        # try:
        #     # Pastikan STAKTIF tidak kosong atau null
        #     staktif = request.json.get('STAKTIF')
        #     if staktif is None or staktif == "":
        #         return {
        #             "message": "Maaf, Status harus di isi!!",
        #             "status": False,
        #             "data": None
        #         }, 400
        #
        #     # Jika STAKTIF tidak kosong atau null, lanjutkan dengan proses update
        #     return GeneralPutById(id, doc, crudTitle, Service, request, modelName, current_user, fileFields,
        #                           internalApi_byUrl)
        # except Exception as e:
        #     logger.error(e)
        #     return {
        #         "message": "Error",
        #         "status": False,
        #         "data": None
        #     }, 500
        return GeneralPutById(id, doc, crudTitle, Service, request, modelName, current_user, fileFields,
                              internalApi_byUrl)

    #### DELETE
    @doc.deleteRespDoc
    @token_required
    def delete(self, id):
        return GeneralDeleteById(id, doc, crudTitle, Service, request, modelName, current_user, fileFields,
                                 internalApi_byUrl)


#### GET SUMMARY
@api.route("/summary")
class Summary(Resource):
    @doc.getSummaryRespDoc
    @token_required
    def get(self):
        try:
            args = parser.parse_args()
            resultData = Service.getSummary(args)
            # if not resultData:
            #     return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)
            resp = message(True, generateDefaultResponse(crudTitle, 'get-sum', 200))
            resp['data'] = resultData or []
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)