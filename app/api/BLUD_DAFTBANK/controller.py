import json
import math

from args import args
from cloudinary import search
from flask import request, current_app
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import text

from app.utils import GeneralGetList, \
    GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, message, \
    generateDefaultResponse, error_response, logger, DateTimeEncoder
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
        return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)
        # args = parser.parse_args()
        # resultFinal = []
        # defaultPageResp = {
        #     "message": f'Get data {modelName} successfully',
        #     "status": True,
        #     "page": args['page'] or 1,
        #     "pages": args['page'] or 1,
        #     "per_page": args['length'] or 10,
        #     "total": 0,
        #     "data": resultFinal
        # }
        # try:
        #     page = f"{args['page'] if args.get('page') else 1}"
        #     length = f"{args['length'] if args.get('length') else 10}"
        #     sort = f"'d.{args.get('sort')}'" if args.get('sort') else "'d.id'"
        #     sort_dir = f"'{args.get('sort_dir')}'" if args.get('sort_dir') else "'asc'"
        #     sqlQuery = f"EXEC DAFTBANK_PAGE @page={page},"\
        #                f"@length={length},@sort={sort}," \
        #                f"@sort_dir={sort_dir},"\
        #                f"@search='{args['search'] or ''}'"
        #     select_query = db.engine.execute(sqlQuery)
        #     results = [dict(row) for row in select_query]
        #     resultStr = json.dumps(results, cls=DateTimeEncoder)
        #     result = json.loads(resultStr)
        #
        #     if len(result) > 0:
        #         defaultPageResp['total'] = result[0]['total']
        #         defaultPageResp['pages'] = math.floor((result[0]['total'] or 0) / (args['length'] or 1))
        #         for row in result:
        #             resultFinal.append({
        #                 'id': row['id'],
        #                 'KDPER': row['KDPER'] if row['KDPER'] else None,
        #                 'NMPER': row['NMPER'].rstrip() if row['NMPER'] else None,
        #                 'MTGLEVEL': row['MTGLEVEL'] if row['MTGLEVEL'] else None,
        #                 'KDKHUSUS': row['KDKHUSUS'] if row['KDKHUSUS'] else None,
        #                 'JNSREK': row['JNSREK'] if row['JNSREK'] else None,
        #                 'IDJNSAKUN': row['IDJNSAKUN'] if row['IDJNSAKUN'] else None,
        #                 'TYPE': row['TYPE'].rstrip() if row['TYPE'] else None,
        #                 'STAKTIF': row['STAKTIF'] if row['STAKTIF'] else None,
        #                 'DATECREATE': row['DATECREATE'] if row['DATECREATE'] else None,
        #                 'URAIAN': row['URAIAN'].rstrip() if row['URAIAN'] else None,
        #             })
        #         return defaultPageResp, 200
        # except Exception as e:
        #     defaultPageResp = {
        #         "message": f'Dapatkan data {modelName} gagal!',
        #         "status": False
        #     }
        #     logger.error(e)
        #     return defaultPageResp, 500

    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    @api.expect(doc.default_data_response, validate=True)
    @token_required
    def post(self):
        # request_post = request.get_json()
        # codeSupplier = self.codeSupplier()
        # request_post['KodeDAFTBANK'] = codeSupplier
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