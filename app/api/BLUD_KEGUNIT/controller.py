from datetime import datetime
from decimal import Decimal

from flask import request, current_app
from flask_restx import Resource, reqparse, inputs
from sqlalchemy import text

from app.utils import GeneralGetList, GeneralPost, GeneralDelete, GeneralGetById, GeneralPutById, GeneralDeleteById, message, \
    generateDefaultResponse, error_response, logger, DateTimeEncoder
from . import crudTitle, enabledPagination, respAndPayloadFields, fileFields, modelName, filterField
from .doc import doc
from .model import KEGUNIT
from .service import Service
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


    # Tentukan parser
    # parser = reqparse.RequestParser()
    #### GET
    @doc.getRespDoc
    @api.expect(parser)
    @token_required
    def get(self):
        args = parser.parse_args()

        if args["kegUnit"] == "1":
            id_unit = args.get("IDUNIT")  # Ambil parameter IDUNIT dari request
            id_prgrm = args.get("IDPRGRM")  # Ambil parameter IDPRGRM dari request

            sqlQuery = text("""
                    EXEC get_kegUnit :id_unit, :id_prgrm;
                """)

            try:
                # Execute the query with parameters
                data = db.engine.execute(sqlQuery, {"id_unit": id_unit, "id_prgrm": id_prgrm})
                a = []

                # Process the rows from the query
                for rowproxy in data:
                    row_dict = {}
                    for column, value in rowproxy.items():
                        # Handle datetime and Decimal types
                        if isinstance(value, datetime):
                            row_dict[column] = value.isoformat()
                        elif isinstance(value, Decimal):
                            row_dict[column] = float(value)  # Convert Decimal to float
                        else:
                            row_dict[column] = value
                    a.append(row_dict)

                # Create a response
                resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
                resp['data'] = a
                return resp, 200

            except Exception as e:
                # Handle exceptions and return error message
                return {"status": False, "message": str(e)}, 500

        if args["kegUnit"] == "2":
            id_unit = args.get("IDUNIT")

            sqlQuery = text("""
                    SELECT KU.id, KU.IDUNIT, KU.IDPRGRM, KU.IDKEG, m4.NUKEG, m4.NMKEGUNIT, KU.KDTAHAP, KU.NOPRIOR, KU.IDSIFATKEG, KU.IDPEG, KU.TGLAKHIR, KU.TGLAWAL, KU.TARGETP, KU.LOKASI, KU.JUMLAHMIN1, KU.PAGU, KU.JUMLAHPLS1, KU.SASARAN, KU.KETKEG, KU.IDPRIODA, KU.IDSAS, KU.TARGET, KU.TARGETIF, 
                    KU.TARGETSEN, KU.VOLUME, KU.VOLUME1, KU.SATUAN, KU.PAGUPLUS, KU.PAGUTIF, KU.TGLVALID
                    FROM KEGUNIT AS KU
                    JOIN MKEGIATAN AS m4
                        ON m4.id = KU.IDKEG
                    WHERE KU.IDUNIT = :id_unit
                """)

            try:
                # Execute the query with parameters
                data = db.engine.execute(sqlQuery, {"id_unit": id_unit})
                a = []

                # Process the rows from the query
                for rowproxy in data:
                    row_dict = {}
                    for column, value in rowproxy.items():
                        # Handle datetime and Decimal types
                        if isinstance(value, datetime):
                            row_dict[column] = value.isoformat()
                        elif isinstance(value, Decimal):
                            row_dict[column] = float(value)  # Convert Decimal to float
                        else:
                            row_dict[column] = value
                    a.append(row_dict)

                # Create a response
                resp = message(True, generateDefaultResponse(crudTitle, 'get-list', 200))
                resp['data'] = a
                return resp, 200

            except Exception as e:
                # Handle exceptions and return error message
                return {"status": False, "message": str(e)}, 500

        else:
            # Handle the other branch of the logic
            return GeneralGetList(doc, crudTitle, enabledPagination, respAndPayloadFields, Service, parser)

    #### POST SINGLE/MULTIPLE
    @doc.postRespDoc
    @api.expect(doc.default_data_response, validate=False)
    @token_required
    def post(self):
        request_post = request.get_json()
        user = current_user['username']
        KDTAHAP = USERTAHAP.query.with_entities(USERTAHAP.KDTAHAP).filter_by(USERID=user).first()
        request_post['KDTAHAP'] = KDTAHAP[0]
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