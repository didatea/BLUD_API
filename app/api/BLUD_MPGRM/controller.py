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

    #### GET
    @doc.getRespDoc
    @api.expect(parser)
    @token_required
    def get(self):
        # # Membuat query untuk mengambil semua data tanpa filter
        # query = """
        #     SELECT PG.IDPRGRM, PG.IDURUS, PG.NMPRGRM, PG.NUPRGRM, PG.STAKTIF AS STAKTIF_PG, PG.STVALID AS STVALID_PG,
        #            PG.DATEUPDATE AS DATEUPDATE_PG, PG.DATECREATE AS DATECREATE_PG, KG.IDKEG, KG.KDPERSPEKTIF, KG.NUKEG,
        #            KG.NMKEGUNIT, KG.LEVELKEG, KG.TYPE AS TYPE_KEG, KG.IDKEGINDUK, KG.STAKTIF AS STAKTIF_KEG,
        #            KG.STVALID AS STVALID_KEG, KG.DATECREATE AS DATECREATE_KEG, KG.DATEUPDATE AS DATEUPDATE_KEG
        #     FROM MPGRM PG
        #     JOIN MPGRM KG ON PG.IDPRGRM = KG.IDPRGRM
        #     ORDER BY PG.NUPRGRM ASC
        #     """
        #
        # # Eksekusi query menggunakan SQLAlchemy
        # engine = sqlalchemy.create_engine(
        #     'mssql+pyodbc://sa:123456@DJUNIE/SALUR_BOP?driver=SQL+Server')
        # connection = engine.connect()
        # result = connection.execute(query)
        #
        # # Mengubah hasil query ke dalam format JSON yang diinginkan
        # data = [{
        #     "IDPRGRM": row['IDPRGRM'],
        #     "IDURUS": row['IDURUS'],
        #     "NMPRGRM": row['NMPRGRM'],
        #     "NUPRGRM": row['NUPRGRM'],
        #     "STAKTIF_PG": row['STAKTIF_PG'],
        #     "STVALID_PG": row['STVALID_PG'],
        #     "DATEUPDATE_PG": row['DATEUPDATE_PG'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row['DATEUPDATE_PG'],
        #                                                                                       datetime) else None,
        #     "DATECREATE_PG": row['DATECREATE_PG'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row['DATECREATE_PG'],
        #                                                                                       datetime) else None,
        #     "IDKEG": row['IDKEG'],
        #     "KDPERSPEKTIF": row['KDPERSPEKTIF'],
        #     "NUKEG": row['NUKEG'],
        #     "NMKEGUNIT": row['NMKEGUNIT'],
        #     "LEVELKEG": row['LEVELKEG'],
        #     "TYPE_KEG": row['TYPE_KEG'],
        #     "IDKEGINDUK": row['IDKEGINDUK'],
        #     "STAKTIF_KEG": row['STAKTIF_KEG'],
        #     "STVALID_KEG": row['STVALID_KEG'],
        #     "DATECREATE_KEG": row['DATECREATE_KEG'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row['DATECREATE_KEG'],
        #                                                                                         datetime) else None,
        #     "DATEUPDATE_KEG": row['DATEUPDATE_KEG'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(row['DATEUPDATE_KEG'],
        #                                                                                         datetime) else None
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
        #     "message": "Get data from GETDATAPROGKEGIATAN successfully",
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