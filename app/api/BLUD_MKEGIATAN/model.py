from datetime import datetime
from threading import Thread

from sqlalchemy import event, func
from sqlalchemy.dialects import mssql
from sqlalchemy.sql import expression

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class MKEGIATAN(db.Model):
    __tablename__ = 'MKEGIATAN'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDPRGRM = db.Column(db.BigInteger, nullable=False)
    KDPERSPEKTIF = db.Column(db.BigInteger, nullable=True)
    NUKEG = db.Column(db.String(30), nullable=False)
    NMKEGUNIT = db.Column(db.String(512), nullable=False)
    LEVELKEG = db.Column(db.Integer, nullable=False)
    TYPE = db.Column(db.String(5), nullable=False)
    parent_id = db.Column(db.BigInteger, nullable=True)
    STAKTIF = db.Column(db.Boolean, default=True, server_default=expression.true(), nullable=True)
    STVALID = db.Column(db.Boolean, default=True, server_default=expression.true(), nullable=True)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)


    # RKAR = db.relationship('RKAR', backref=db.backref(f'{modelName}'), lazy = "dynamic")
    BENDKEG = db.relationship('BENDKEG', backref=db.backref(f'{modelName}'), lazy="dynamic")

    @property
    def has_child(self):
        count = db.session.query(func.count(MKEGIATAN.id)).filter(MKEGIATAN.parent_id > self.id).scalar()
        return count > 0


# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, MKEGIATAN)


@event.listens_for(MKEGIATAN, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(MKEGIATAN, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(MKEGIATAN, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(MKEGIATAN, 'after_insert')
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