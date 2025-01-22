from datetime import datetime

from flask import request, current_app
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import text

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, message, \
    generateDefaultResponse, error_response
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
    # @token_required
    def get(self):
        args = parser.parse_args()
        if args["semester"] == "1":
            sqlQuery = text(f'''
                            select *
                            from (
                                select 1 id, 'Semester I' nama, 1 semester, 1 triwulan
                                union all
                                select 2 id, 'Semester II' nama, 2 semester, 2 triwulan
                                union all
                                select 0 id, 'Akhir Tahun' nama, 3 semester, 0 triwulan
                            ) a order by a.semester
                                  ''')

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
        elif args["periode"] == "1":
            sqlQuery = text(f'''
                                select *
                                from (
                                    select id, nama, semester, triwulan from asetBulan
                                    union all 
                                    select 13, 'Semester I', 1, 13 
                                    union all
                                    select 14, 'Semester II', 2, 14
                                    union all
                                    select 15, 'Akhir Tahun', 0, 15
                                ) a order by a.id
                                  ''')

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
        elif args["tahun"] == "1":
            sqlQuery = text(f'''
                                select x.nama id, x.nama
                                from(
                                    select a.[value]-1 nama from asetSetup a where a.id = 1
                                    union all
                                    select a.[value] from asetSetup a where a.id = 1
                                    union all
                                    select a.[value]+1 from asetSetup a where a.id = 1
                                ) x
                                order by x.nama
                                  ''')

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
        return GeneralPutById(id, doc, crudTitle, Service, request, modelName, current_user, fileFields, internalApi_byUrl)

    #### DELETE
    @doc.deleteRespDoc
    @token_required
    def delete(self, id):
        return GeneralDeleteById(id, doc, crudTitle, Service, request, modelName, current_user, fileFields, internalApi_byUrl)


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
            resp['data'] = resultData
            return resp, 200
        except Exception as e:
            current_app.logger.error(e)
            return error_response(generateDefaultResponse(crudTitle, 'get-sum', 500), 500)