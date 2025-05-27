from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class SPPDETP(db.Model):
    __tablename__ = 'SPPDETP'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDSPP = db.Column(db.BigInteger, nullable=False)
    IDPAJAK = db.Column(db.BigInteger, db.ForeignKey("PAJAK.id"), nullable=False)
    NILAI = db.Column(mssql.MONEY, nullable=True)
    KETERANGAN = db.Column(db.String(512), nullable=False)
    IDBILLING = db.Column(db.String(20), nullable=False)
    TGLBILLING = db.Column(db.DateTime, default=datetime.now, nullable=True)
    NTPN = db.Column(db.String(100), nullable=False)
    NTB = db.Column(db.String(100), nullable=False)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    # kegunit_rel = db.relationship(
    #     'KEGUNIT',
    #     primaryjoin='SPPDETP.IDKEG == KEGUNIT.id',
    #     backref='SPPDETP_items',
    #     lazy='joined'  # Auto join saat query
    # )
    @property
    def KDPAJAK(self):
        return self.PAJAK.KDPAJAK if self.PAJAK else ""

    @property
    def NMPAJAK(self):
        return self.PAJAK.NMPAJAK if self.PAJAK else ""

    @property
    def NMKEGUNIT(self):
        # Debugging langsung
        if not self.kegunit_rel:
            print(f"Debug: No KEGUNIT found for SPPDETP ID {self.id} with IDKEG {self.IDKEG}")
            return ""

        if not hasattr(self.kegunit_rel, 'mkegiatan'):
            print(f"Debug: KEGUNIT {self.kegunit_rel.id} has no mkegiatan relation")
            return ""

        return self.kegunit_rel.mkegiatan.NMKEGUNIT or ""

    @property
    def NMPER(self):
        return self.DAFTREKENING.NMPER if self.DAFTREKENING else ""

    @property
    def KDUNIT(self):
        return self.DAFTUNIT.KDUNIT if self.DAFTUNIT else ""

    @property
    def UNIT(self):
        return self.DAFTUNIT.NMUNIT if self.DAFTUNIT else ""


    # @property
    # def TAHAPAN(self):
    #     return self.TAHAP.URAIAN if self.TAHAP else ""

    # @property
    # def URAISTATUS(self):
    #     return self.STATTRS.URAIAN if self.STATTRS else ""

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, SPPDETP)


@event.listens_for(SPPDETP, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(SPPDETP, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(SPPDETP, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(SPPDETP, 'after_insert')
def insert_activity_insert(mapper, connection, target):
    access_token = current_user['access_token']
    origin = current_user['origin']
    data = {
        "type": 'post',
        'endpoint_path': f'{apiPath}',
        'data_id': target.id,
        'subject': crudTitle,
        'origin': origin,
        "attributes": {
            'data': row2dict(target)
        }
    }
    thread = Thread(target=insert_user_activity, args=(data, access_token,))
    thread.start()
    thread.join()