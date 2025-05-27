from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class BPK(db.Model):
    __tablename__ = 'BPK'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDUNIT = db.Column(db.BigInteger, db.ForeignKey("DAFTUNIT.id"), nullable=False)
    IDPHK3 = db.Column(db.BigInteger, db.ForeignKey("DAFTPHK3.id"), nullable=True)
    NOBPK = db.Column(db.String(100), nullable=False)
    KDSTATUS = db.Column(db.String(3), db.ForeignKey("STATTRS.KDSTATUS"), nullable=False)
    IDJBAYAR = db.Column(db.Integer, db.ForeignKey("JBAYAR.id"), nullable=True)
    IDXKODE = db.Column(db.Integer, nullable=True, default=2)
    IDBEND = db.Column(db.BigInteger, nullable=False)
    TGLBPK = db.Column(db.DateTime, default=datetime.now, nullable=True)
    URAIBPK = db.Column(db.String(254), nullable=True)
    TGLVALID = db.Column(db.DateTime, nullable=True)
    IDBERITA = db.Column(db.BigInteger, nullable=False)
    KDRILIS = db.Column(db.BigInteger, nullable=False)
    STKIRIM = db.Column(db.Integer, nullable=True)
    STCAIR = db.Column(db.Integer, nullable=True)
    NOREF = db.Column(db.String(36), nullable=False)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    @property
    def UNIT(self):
        return self.DAFTUNIT.NMUNIT if self.DAFTUNIT else ""

    @property
    def PEMBAYARAN(self):
        return self.JBAYAR.URAIANBAYAR if self.JBAYAR else ""

    @property
    def PENERIMA(self):
        return self.DAFTPHK3.NMPHK3 if self.DAFTPHK3 else ""

    @property
    def STATUS(self):
        return self.STATTRS.LBLSTATUS if self.STATTRS else ""

    # @property
    # def KEGIATAN(self):
    #     return self.MKEGIATAN.NMKEGUNIT if self.MKEGIATAN else ""

    @property
    def KDREKENING(self):
        return self.DAFTREKENING.KDPER if self.DAFTREKENING else ""

    @property
    def REKENING(self):
        return self.DAFTREKENING.NMPER if self.DAFTREKENING else ""

    @property
    def TAHAPAN(self):
        return self.TAHAP.URAIAN if self.TAHAP else ""

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, BPK)


@event.listens_for(BPK, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(BPK, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(BPK, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(BPK, 'after_insert')
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