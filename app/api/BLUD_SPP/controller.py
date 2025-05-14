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
from .model import SPP
from .service import Service
from ..BLUD_DAFTUNIT.model import DAFTUNIT
from ..BLUD_RKAB.model import RKAB
from ..BLUD_RKABDET.model import RKABDET
from ..BLUD_RKAD.model import RKAD
from ..BLUD_RKADDET.model import RKADDET
from ..BLUD_RKAR.model import RKAR
from ..BLUD_RKARDET.model import RKARDET
from ..BLUD_USERTAHAP.model import USERTAHAP
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

    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):
        data = request.get_json()

        # Hapus TGLVALID agar tidak disimpan saat post
        data.pop('TGLVALID', None)
        # request._cached_json = data  # update cache JSON agar GeneralPost pakai data ini

        # Simpan data utama ke DB
        response, status_code = GeneralPost(doc, crudTitle, Service, request)

        # Ambil ID dari hasil response
        # inserted_id = response.get('data', {}).get('id')
        #
        # # Jalankan SQL tambahan jika KDSTATUS == '21'
        # if data.get('KDSTATUS', '').strip() == "21" and inserted_id:
        #     try:
        #         sqlQuery = text('''
        #             INSERT INTO SPPDETB(IDREK, IDSPP, IDNOJETRA, NILAI)
        #             VALUES (:idrek, :idspp, :idnojetra, :nilai)
        #         ''')
        #         db.session.execute(sqlQuery, {
        #             "idrek": 15968,
        #             "idspp": inserted_id,
        #             "idnojetra": "21",
        #             "nilai": 0
        #         })
        #         db.session.commit()
        #     except Exception as e:
        #         current_app.logger.error(f"Insert SPPDETB gagal: {e}")
        #         db.session.rollback()

        return response, status_code

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
        spp_status = SPP.query.filter_by(id=id).first()
        if not spp_status:
            return error_response("Data tidak ditemukan", 404)

        data = request.get_json()
        status = data.get("STATUS")

        if status == 0:
            # Jika status draft, abaikan input TGLVALID dan set ke NULL
            data['TGLVALID'] = None

        # Kalau status == 1, biarkan TGLVALID dari user tetap dikirim
        return GeneralPutById(id, doc, crudTitle, Service, request,modelName, current_user, fileFields, internalApi_byUrl)

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