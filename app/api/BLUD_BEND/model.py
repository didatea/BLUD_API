from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class BEND(db.Model):
    __tablename__ = 'BEND'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    JNSBEND = db.Column(db.String(2), nullable=False)
    IDPEG = db.Column(db.BigInteger , db.ForeignKey("PEGAWAI.id"), nullable=False)
    IDUNIT = db.Column(db.BigInteger, nullable=False)
    IDBANK = db.Column(db.BigInteger, nullable=False)
    NMCABBANK = db.Column(db.String(100), nullable=True)
    REKBEND = db.Column(db.String(50), nullable=False)
    NPWPBEND = db.Column(db.String(50), nullable=False)
    JABBEND = db.Column(db.String(100), nullable=False)
    SALDOBEND = db.Column(mssql.MONEY, nullable=True)
    SALDOBENDT = db.Column(mssql.MONEY, nullable=True)
    TGLSTOPBEND = db.Column(db.DateTime,  nullable=True)
    WARGANEGARA = db.Column(db.String(100), nullable=True)
    STPENDUDUDUK = db.Column(db.String(100), nullable=True)
    STAKTIF = db.Column(db.Integer, nullable=True)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    BENDKEG = db.relationship('BENDKEG', backref=db.backref(f'{modelName}'), lazy="dynamic")

    @property
    def NIP(self):
        return f"{self.PEGAWAI.NIP} " if self.PEGAWAI else None

    @property
    def NAMA(self):
        return f" {self.PEGAWAI.NAMA}" if self.PEGAWAI else None


# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, BEND)


@event.listens_for(BEND, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(BEND, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(BEND, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(BEND, 'after_insert')
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


@event.listens_for(BEND, 'after_update')
def insert_activity_update(mapper, connection, target):
    access_token = current_user['access_token']
    origin = current_user['origin']
    data = {
        "type": 'put',
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


@event.listens_for(BEND, 'after_delete')
def insert_activity_delete(mapper, connection, target):
    access_token = current_user['access_token']
    origin = current_user['origin']
    data = {
        "type": 'delete',
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