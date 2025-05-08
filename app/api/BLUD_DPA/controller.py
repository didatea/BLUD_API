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
from ..BLUD_DAFTUNIT.model import DAFTUNIT
from ..BLUD_DPAB.model import DPAB
from ..BLUD_DPAD.model import DPAD
from ..BLUD_DPADETB.model import DPADETB
from ..BLUD_DPADETD.model import DPADETD
from ..BLUD_DPADETR.model import DPADETR
from ..BLUD_DPAR.model import DPAR
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
        request_post = request.get_json()
        user = current_user['username']
        IDUNIT = int(request_post.get("IDUNIT", 0))  # Konversi ke integer
        KDTAHAP_ROW = USERTAHAP.query.with_entities(USERTAHAP.KDTAHAP).filter_by(USERID=user).first()
        if not KDTAHAP_ROW:
            return {"message": "KDTAHAP tidak ditemukan untuk user ini"}, 400
        KDTAHAP = KDTAHAP_ROW[0]
        KDUNIT_ROW = DAFTUNIT.query.with_entities(DAFTUNIT.KDUNIT).filter_by(id=IDUNIT).first()
        if not KDUNIT_ROW:
            return {"message": "KDUNIT tidak ditemukan untuk IDUNIT ini"}, 400
        KDUNIT = KDUNIT_ROW[0]
        NOMOR = ".".join(KDUNIT.split(".")[:3] + ["01", "02", "0"] + KDUNIT.split(".")[3:])
        request_post['NODPA'] = NOMOR
        request_post['NOSAH'] = NOMOR
        request_post['KDTAHAP'] = KDTAHAP[0]
        request_post['TGLDPA'] = request_post['TGLVALID']
        IDXKODE = request_post['IDXKODE']

        # Simpan data utama ke DPA
        dpa_entry = GeneralPost(doc, crudTitle, Service, request)
        IDDPA = dpa_entry[0]['data']['id']
        print(dpa_entry)
        print(int(IDDPA))
        if not IDDPA:
            return {"message": "Gagal menyimpan data DPA"}, 400

        data_added = False

        if IDXKODE == 1:
            rkad_data = db.session.query(RKAD).filter_by(IDUNIT=IDUNIT, KDTAHAP=KDTAHAP[0]).all()
            if not rkad_data:
                return {"message": "Data RKAD tidak ditemukan, penyimpanan dibatalkan"}, 400

            for data in rkad_data:
                new_entry = DPAD(
                    IDUNIT=int(data["IDUNIT"]) if isinstance(data, dict) else int(data.IDUNIT),
                    IDDPA=IDDPA,
                    KDTAHAP=str(data["KDTAHAP"]) if isinstance(data, dict) else str(data.KDTAHAP),
                    IDREK=str(data["IDREK"]) if isinstance(data, dict) else str(data.IDREK),
                    NILAI=float(data["NILAI"]) if isinstance(data, dict) else float(data.NILAI),
                    DATECREATE=data["DATECREATE"] if isinstance(data, dict) else data.DATECREATE,
                    DATEUPDATE=data["DATEUPDATE"] if isinstance(data, dict) else data.DATEUPDATE
                )
                db.session.add(new_entry)
                db.session.flush()  # Flush untuk mendapatkan IDDPAD

                # Ambil IDDPAD yang baru saja dibuat
                IDDPAD = new_entry.id

                # Ambil semua data RKADDET yang berelasi dengan RKAD
                # Cek apakah sudah ada data DPADETD dengan IDDPAD ini
                existing_dpadetd = db.session.query(DPADETD).filter_by(IDDPAD=IDDPAD).first()

                if not existing_dpadetd:  # Hanya insert jika belum ada data terkait
                    rkad_det_data = db.session.query(RKADDET).filter_by(IDRKAD=data.id).all()

                    for det in rkad_det_data:
                        new_det_entry = DPADETD(
                            IDDPAD=IDDPAD,
                            IDUNIT=det.IDUNIT,
                            KDTAHAP=det.KDTAHAP,
                            IDREK=det.IDREK,
                            KDJABAR=det.KDJABAR,
                            URAIAN=det.URAIAN,
                            JUMBYEK=det.JUMBYEK,
                            SATUAN=det.SATUAN,
                            TARIF=det.TARIF,
                            SUBTOTAL=det.SUBTOTAL,
                            EKSPRESI=det.EKSPRESI,
                            INCLSUBTOTAL=det.INCLSUBTOTAL,
                            TYPE=det.TYPE,
                            IDSTDHARGA=det.IDSTDHARGA,
                            DATECREATE=det.DATECREATE,
                            DATEUPDATE=det.DATEUPDATE
                        )
                        db.session.add(new_det_entry)
                data_added = True

        elif IDXKODE == 2:
            rkar_data = db.session.query(RKAR).filter_by(IDUNIT=IDUNIT, KDTAHAP=KDTAHAP[0]).all()
            if not rkar_data:
                return {"message": "Data RKAR tidak ditemukan, penyimpanan dibatalkan"}, 400

            for data in rkar_data:
                new_entry = DPAR(
                    IDUNIT=int(data["IDUNIT"]) if isinstance(data, dict) else int(data.IDUNIT),
                    IDDPA=IDDPA,
                    KDTAHAP=str(data["KDTAHAP"]) if isinstance(data, dict) else str(data.KDTAHAP),
                    IDKEG=str(data["IDREK"]) if isinstance(data, dict) else str(data.IDKEG),
                    IDREK=str(data["IDREK"]) if isinstance(data, dict) else str(data.IDREK),
                    NILAI=float(data["NILAI"]) if isinstance(data, dict) else float(data.NILAI),
                    DATECREATE=data["DATECREATE"] if isinstance(data, dict) else data.DATECREATE,
                    DATEUPDATE=data["DATEUPDATE"] if isinstance(data, dict) else data.DATEUPDATE
                )
                db.session.add(new_entry)
                db.session.flush()  # Flush untuk mendapatkan IDDPAD

                # Ambil IDDPAD yang baru saja dibuat
                IDDPAR = new_entry.id

                # Ambil semua data RKADDET yang berelasi dengan RKAD
                # Cek apakah sudah ada data DPADETD dengan IDDPAD ini
                existing_dpadetr = db.session.query(DPADETR).filter_by(IDDPAR=IDDPAR).first()

                if not existing_dpadetr:  # Hanya insert jika belum ada data terkait
                    rkar_det_data = db.session.query(RKARDET).filter_by(IDRKAR=data.id).all()

                    for det in rkar_det_data:
                        new_det_entry = DPADETR(
                            IDDPAR=IDDPAR,
                            IDUNIT=det.IDUNIT,
                            KDTAHAP=det.KDTAHAP,
                            IDREK=det.IDREK,
                            IDKEG=det.IDKEG,
                            KDJABAR=det.KDJABAR,
                            URAIAN=det.URAIAN,
                            JUMBYEK=det.JUMBYEK,
                            SATUAN=det.SATUAN,
                            TARIF=det.TARIF,
                            SUBTOTAL=det.SUBTOTAL,
                            EKSPRESI=det.EKSPRESI,
                            INCLSUBTOTAL=det.INCLSUBTOTAL,
                            TYPE=det.TYPE,
                            IDSTDHARGA=det.IDSTDHARGA,
                            DATECREATE=det.DATECREATE,
                            DATEUPDATE=det.DATEUPDATE
                        )
                        db.session.add(new_det_entry)
                data_added = True

        elif IDXKODE == 5:
            rkab_data = db.session.query(RKAB).filter_by(IDUNIT=IDUNIT, KDTAHAP=KDTAHAP[0]).all()
            if not rkab_data:
                return {"message": "Data RKAB tidak ditemukan, penyimpanan dibatalkan"}, 400

            for data in rkab_data:
                new_entry = DPAB(
                    IDUNIT=int(data["IDUNIT"]) if isinstance(data, dict) else int(data.IDUNIT),
                    IDDPA=IDDPA,
                    KDTAHAP=str(data["KDTAHAP"]) if isinstance(data, dict) else str(data.KDTAHAP),
                    IDREK=str(data["IDREK"]) if isinstance(data, dict) else str(data.IDREK),
                    NILAI=float(data["NILAI"]) if isinstance(data, dict) else float(data.NILAI),
                    DATECREATE=data["DATECREATE"] if isinstance(data, dict) else data.DATECREATE,
                    DATEUPDATE=data["DATEUPDATE"] if isinstance(data, dict) else data.DATEUPDATE
                )
                db.session.add(new_entry)
                db.session.flush()  # Flush untuk mendapatkan IDDPAD

                # Ambil IDDPAD yang baru saja dibuat
                IDDPAB = new_entry.id

                # Ambil semua data RKADDET yang berelasi dengan RKAD
                # Cek apakah sudah ada data DPADETD dengan IDDPAD ini
                existing_dpadetb = db.session.query(DPADETB).filter_by(IDDPAB=IDDPAB).first()

                if not existing_dpadetb:  # Hanya insert jika belum ada data terkait
                    rkab_det_data = db.session.query(RKABDET).filter_by(IDRKAB=data.id).all()

                    for det in rkab_det_data:
                        new_det_entry = DPADETB(
                            IDDPAB=IDDPAB,
                            IDUNIT=det.IDUNIT,
                            KDTAHAP=det.KDTAHAP,
                            IDREK=det.IDREK,
                            KDJABAR=det.KDJABAR,
                            URAIAN=det.URAIAN,
                            JUMBYEK=det.JUMBYEK,
                            SATUAN=det.SATUAN,
                            TARIF=det.TARIF,
                            SUBTOTAL=det.SUBTOTAL,
                            EKSPRESI=det.EKSPRESI,
                            INCLSUBTOTAL=det.INCLSUBTOTAL,
                            TYPE=det.TYPE,
                            IDSTDHARGA=det.IDSTDHARGA,
                            DATECREATE=det.DATECREATE,
                            DATEUPDATE=det.DATEUPDATE
                        )
                        db.session.add(new_det_entry)
                data_added = True

        if data_added:
            db.session.commit()
            return dpa_entry
        else:
            return {"message": "Tidak ada perubahan data yang disimpan"}, 400
        # return dpa_entry

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