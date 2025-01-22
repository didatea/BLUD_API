import decimal
import json
import math
from cgitb import text
from datetime import datetime

from sqlalchemy import text
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
        args = parser.parse_args()
        id_prgrm = args.get('IDPRGRM')
        # level_keg = args.get('LEVELKEG')
        if args["LOOKUP"] == "KUA":
            sqlQuery = text(f'''
            SELECT m.id, m.IDPRGRM, m.KDPERSPEKTIF, m.NUKEG, m.NMKEGUNIT, m.LEVELKEG,
                   m.[TYPE], m.PARENT_ID, m.STAKTIF, m.STVALID, m.DATECREATE, m.DATEUPDATE
            FROM MKEGIATAN AS m
            WHERE m.IDPRGRM={id_prgrm}
            ORDER BY m.NUKEG
            ''')
        # elif level_keg == "2":
        #     parent = args.get('PARENT_ID')
        #     sqlQuery = text(f'''
        #     SELECT m.id, m.IDPRGRM, m.KDPERSPEKTIF, m.NUKEG, m.NMKEGUNIT, m.LEVELKEG,
        #            m.[TYPE], m.PARENT_ID, m.STAKTIF, m.STVALID, m.DATECREATE, m.DATEUPDATE
        #     FROM MKEGIATAN AS m
        #     WHERE m.LEVELKEG=2 AND m.IDPRGRM={id_prgrm} AND m.PARENT_ID={parent}
        #     ORDER BY m.NUKEG
        #     ''')
            data = db.engine.execute(sqlQuery)
            d, a = {}, []
            for rowproxy in data:
                for column, value in rowproxy.items():
                    if isinstance(value, datetime):
                        d = {**d, **{column: value.isoformat()}}
                    else:
                        d = {**d, **{column: value}}
                a.append(d)
            # print(a)
            resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
            resp['data'] = a
            return resp, 200
        if args.get("LEVELKEG") and args.get("parent_id"):
            parser.remove_argument("LEVELKEG")
        else:
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