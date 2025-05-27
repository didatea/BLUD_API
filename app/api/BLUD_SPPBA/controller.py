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
from . import crudTitle, enableSPPBAgination, respAnSPPBAyloadFields, fileFields, modelName, filterField
from .doc import doc
from .model import SPPBA
from .service import Service
from ..BLUD_BERITADETR.model import BERITADETR
from ..BLUD_SPPDETR.model import SPPDETR
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
    if enableSPPBAgination:
        parser.add_argument('page', type=int, help='page/start, fill with number')
        parser.add_argument('length', type=int, help='length of data, fill with number')
        parser.add_argument('search', type=str, help='for filter searching')
    if 'parent_id' in respAnSPPBAyloadFields:
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
        return GeneralGetList(doc, crudTitle, enableSPPBAgination, respAnSPPBAyloadFields, Service, parser)

    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    # @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):
        try:
            request_post = request.get_json()
            print("Request data:", request_post)

            if not request_post:
                return {"message": "Empty request data"}, 400

            data = request_post[0] if isinstance(request_post, list) else request_post

            # Ambil nilai yang dibutuhkan
            IDBERITA = data.get("IDBERITA")
            IDSPP = data.get("IDSPP")
            IDKEG = data.get("IDKEG")

            if not all([IDBERITA, IDSPP, IDKEG]):
                return {"message": "Missing required fields"}, 400

            # Insert ke SPPBA
            new_sppba = SPPBA(
                IDSPP=IDSPP,
                IDBERITA=IDBERITA,
                DATECREATE=datetime.now()
            )
            db.session.add(new_sppba)
            db.session.flush()

            # Ambil semua baris dari BERITADETR sesuai IDBERITA
            beritadetr_rows = BERITADETR.query.with_entities(
                BERITADETR.IDREK, BERITADETR.NILAI
            ).filter_by(IDBERITA=IDBERITA).all()

            if not beritadetr_rows:
                db.session.rollback()
                return {"message": f"No BERITADETR found for IDBERITA={IDBERITA}"}, 404

            for row in beritadetr_rows:
                if not row.IDREK or row.NILAI is None:
                    db.session.rollback()
                    return {"message": "Invalid data in BERITADETR row"}, 400

                new_sppdetr = SPPDETR(
                    IDREK=row.IDREK,
                    IDKEG=IDKEG,
                    IDSPP=IDSPP,
                    IDNOJETRA=21,
                    NILAI=row.NILAI,
                    DATECREATE=datetime.now(),
                    DATEUPDATE=datetime.now()
                )
                db.session.add(new_sppdetr)

            db.session.commit()

            return {
                "success": True,
                "message": "SPPBA and SPPDETR inserted successfully",
                "SPPBA": {"IDSPP": IDSPP, "IDBERITA": IDBERITA},
                "SPPDETR_rows": len(beritadetr_rows)
            }, 201

        except Exception as e:
            db.session.rollback()
            print(f"Exception occurred: {str(e)}")
            return {"success": False, "message": f"Internal Server Error: {str(e)}"}, 500

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