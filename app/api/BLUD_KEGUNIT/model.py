from datetime import datetime
from threading import Thread

from sqlalchemy import event, func
from sqlalchemy.dialects import mssql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression

from app import db
from . import crudTitle, apiPath, modelName
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_privilege_on_read_db, check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict


class KEGUNIT(db.Model):
    __tablename__ = 'KEGUNIT'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDUNIT = db.Column(db.BigInteger, nullable=False)
    IDKEG = db.Column(db.BigInteger, nullable=False)
    KDTAHAP = db.Column(db.String(5), nullable=False)
    IDPRGRM = db.Column(db.BigInteger, nullable=False)
    NOPRIOR = db.Column(db.Integer, nullable=True)
    IDSIFATKEG = db.Column(db.BigInteger, nullable=False)
    IDPEG = db.Column(db.BigInteger, nullable=True)
    TGLAKHIR = db.Column(db.DateTime, default=datetime.now, nullable=True)
    TGLAWAL = db.Column(db.DateTime, default=datetime.now, nullable=True)
    TARGETP = db.Column(mssql.MONEY, nullable=True)
    LOKASI = db.Column(db.String(512), nullable=True)
    JUMLAHMIN1 = db.Column(mssql.MONEY, nullable=True)
    PAGU = db.Column(mssql.MONEY, nullable=True)
    JUMLAHPLS1 = db.Column(mssql.MONEY, nullable=True)
    SASARAN = db.Column(db.String(512), nullable=True)
    KETKEG = db.Column(db.String(512), nullable=True)
    IDPRIODA = db.Column(db.String(36), nullable=True)
    IDSAS = db.Column(db.String(36), nullable=True)
    TARGET = db.Column(db.String(10), nullable=True)
    TARGETIF = db.Column(db.String(10), nullable=True)
    TARGETSEN = db.Column(db.String(10), nullable=True)
    VOLUME = db.Column(db.String(10), nullable=True)
    VOLUME1 = db.Column(db.String(10), nullable=True)
    SATUAN = db.Column(db.String(30), nullable=True)
    PAGUPLUS = db.Column(mssql.MONEY, nullable=True)
    PAGUTIF = db.Column(mssql.MONEY, nullable=True)
    TGLVALID = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    RKAR = db.relationship('RKAR', backref=db.backref(f'{modelName}'), lazy="dynamic")


# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, KEGUNIT)


@event.listens_for(KEGUNIT, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(KEGUNIT, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(KEGUNIT, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(KEGUNIT, 'after_insert')
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


@event.listens_for(KEGUNIT, 'after_update')
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


@event.listens_for(KEGUNIT, 'after_delete')
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
