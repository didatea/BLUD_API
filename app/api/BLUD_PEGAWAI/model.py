from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql
from sqlalchemy.sql import expression

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName
from ..BLUD_DAFTUNIT.model import DAFTUNIT


class PEGAWAI(db.Model):
    __tablename__ = 'PEGAWAI'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    NIP = db.Column(db.String(50), nullable=False)
    IDUNIT = db.Column(db.BigInteger, nullable=False)
    KDGOL = db.Column(db.String(10), nullable=False)
    NAMA = db.Column(db.String(200), nullable=True)
    ALAMAT = db.Column(db.String(512), nullable=True)
    JABATAN = db.Column(db.String(512), nullable=True)
    PDDK = db.Column(db.String(30), nullable=True)
    NPWP = db.Column(db.String(50), nullable=True)
    STAKTIF = db.Column(db.Boolean, default=True, server_default=expression.true(), nullable=True)
    STVALID = db.Column(db.Boolean, default=True, server_default=expression.true(), nullable=True)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    @property
    def NMUNIT(self):
        nama_unit = DAFTUNIT.query.filter_by(id=self.IDUNIT).first()
        if nama_unit:
            return nama_unit.NMUNIT
        else:
            return None

    BEND = db.relationship("BEND", backref=modelName, lazy="dynamic")


# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, PEGAWAI)


@event.listens_for(PEGAWAI, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(PEGAWAI, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(PEGAWAI, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(PEGAWAI, 'after_insert')
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