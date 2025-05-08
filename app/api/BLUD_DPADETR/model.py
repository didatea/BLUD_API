from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class DPADETR(db.Model):
    __tablename__ = 'DPADETR'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDUNIT = db.Column(db.BigInteger, db.ForeignKey("DAFTUNIT.id"), nullable=False)
    IDKEG = db.Column(db.BigInteger, db.ForeignKey("KEGUNIT.id"), nullable=False)
    KDTAHAP = db.Column(db.String(5), db.ForeignKey("TAHAP.KDTAHAP"), nullable=False)
    IDREK = db.Column(db.BigInteger, db.ForeignKey("DAFTREKENING.id"), nullable=False)
    IDDPAR = db.Column(db.BigInteger, nullable=False)
    KDJABAR = db.Column(db.String(5), nullable=False)
    URAIAN = db.Column(db.String(512), nullable=False)
    JUMBYEK = db.Column(mssql.MONEY, nullable=True)
    SATUAN = db.Column(db.String(30), nullable=False)
    TARIF = db.Column(mssql.MONEY, nullable=True)
    SUBTOTAL = db.Column(mssql.MONEY, nullable=True)
    EKSPRESI = db.Column(db.String(254), nullable=False)
    INCLSUBTOTAL = db.Column(db.Boolean, nullable=False)
    TYPE = db.Column(db.String(2), nullable=False)
    IDSTDHARGA = db.Column(db.String(10), nullable=False)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)


    @property
    def UNIT(self):
        return self.DAFTUNIT.NMUNIT if self.DAFTUNIT else ""

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
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, DPADETR)


@event.listens_for(DPADETR, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(DPADETR, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(DPADETR, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(DPADETR, 'after_insert')
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