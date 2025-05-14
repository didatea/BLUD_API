from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression

from app import db
from . import crudTitle, apiPath, modelName
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_privilege_on_read_db, check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict


class KONTRAK(db.Model):
    __tablename__ = 'KONTRAK'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDUNIT = db.Column(db.BigInteger, nullable=False)
    NOKONTRAK = db.Column(db.String(100), nullable=False)
    IDPHK3 = db.Column(db.BigInteger, db.ForeignKey("DAFTPHK3.id"), nullable=False)
    IDKEG = db.Column(db.BigInteger, nullable=False)
    TGLKON = db.Column(db.DateTime, default=datetime.now, nullable=True)
    TGLAWALKONTRAK = db.Column(db.DateTime, default=datetime.now, nullable=True)
    TGLAKHIRKONTRAK = db.Column(db.DateTime, default=datetime.now, nullable=True)
    URAIAN = db.Column(db.String(512), nullable=True)
    NILAI = db.Column(mssql.MONEY, nullable=True)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    @property
    def NMPHK3(self):
        return f" {self.DAFTPHK3.NMPHK3}" if self.DAFTPHK3 else None

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, KONTRAK)


@event.listens_for(KONTRAK, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(KONTRAK, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(KONTRAK, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(KONTRAK, 'after_insert')
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


@event.listens_for(KONTRAK, 'after_update')
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


@event.listens_for(KONTRAK, 'after_delete')
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