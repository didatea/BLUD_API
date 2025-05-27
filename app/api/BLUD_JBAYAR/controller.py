import decimal
import json
import math
from cgitb import text
from datetime import datetime

import sqlalchemy
from flask import request, current_app, jsonify
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.elements import Null

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, generateDefaultResponse, message, \
    error_response, DateTimeEncoder, logger
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .service import Service
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
        # # Membuat query untuk mengambil data dari tabel JBAYAR dengan menggunakan IDUNIT sebagai primary key
        # query = """
        #     SELECT id, KDBANK, NMBANK, URAIAN, AKRONIM, DATECREATE
        #     FROM JBAYAR
        #     """
        #
        # # Eksekusi query menggunakan SQLAlchemy
        # engine = sqlalchemy.create_engine(
        #     'mssql+pyodbc://sa:123456@DJUNIE/INSABA_BOP_2024?driver=SQL+Server')
        # connection = engine.connect()
        # result = connection.execute(query)
        #
        # # Mengubah hasil query ke dalam format JSON yang diinginkan
        # data = [{
        #     "id": row['id'],
        #     "KDBANK": row['KDBANK'],
        #     "NMBANK": row['NMBANK'],
        #     "URAIAN": row['URAIAN'],
        #     "AKRONIM": row['AKRONIM'],
        #     "DATECREATE": row['DATECREATE'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row['DATECREATE'],
        #                                                                                 datetime) else None,
        # } for row in result]
        #
        # # Menutup koneksi
        # connection.close()
        #
        # # Menghitung jumlah total data
        # total = len(data)
        #
        # # Membuat respons JSON
        # response = {
        #     "message": "Get data JBAYAR successfully",
        #     "status": True,
        #     "total": total,
        #     "data": data
        # }
        #
        # # Mengembalikan respons JSON
        # return jsonify(response)
        return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)


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
        # # Membuat query untuk mengambil data dengan IDUNIT tertentu
        # query = f"""
        #         SELECT id, KDBANK, NMBANK, URAIAN, AKRONIM, DATECREATE
        #         FROM JBAYAR
        #         WHERE id = {id}
        #         """
        #
        # # Eksekusi query menggunakan SQLAlchemy
        # engine = sqlalchemy.create_engine(
        #     'mssql+pyodbc://sa:123456@DJUNIE/INSABA_BOP_2024?driver=SQL+Server')
        # connection = engine.connect()
        # result = connection.execute(query)
        #
        # # Mengambil hasil query
        # row = result.fetchone()
        #
        # # Jika tidak ada data yang ditemukan, kembalikan response kosong
        # if not row:
        #     return jsonify({}), 404
        #
        # # Menutup koneksi
        # connection.close()
        #
        # # Mengembalikan data dalam format JSON
        # # return jsonify(data)
        return GeneralGetById(id, doc, crudTitle, Service)

    #### PUT
    @doc.putRespDoc
    @api.expect(doc.default_data_response)
    @token_required
    def put(self, id):
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