from datetime import datetime
from threading import Thread

from sqlalchemy import event, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression

from app import db
from . import crudTitle, apiPath, modelName
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_privilege_on_read_db, check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from ..BLUD_JREK.model import JREK


class DAFTREKENING(db.Model):
    __tablename__ = 'DAFTREKENING'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    KDPER = db.Column(db.String(50), nullable=False)
    NMPER = db.Column(db.String(512), nullable=False)
    MTGLEVEL = db.Column(db.Integer, nullable=False)
    KDKHUSUS = db.Column(db.Integer, nullable=False)
    JNSREK = db.Column(db.Integer, db.ForeignKey("JREK.id"), nullable=False)
    IDJNSAKUN = db.Column(db.BigInteger, nullable=True)
    TYPE = db.Column(db.String(2), nullable=False)
    STAKTIF = db.Column(db.Integer, nullable=True)
    parent_id = db.Column(db.BigInteger, nullable=False)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    RKAB = db.relationship('RKAB', backref=db.backref(f'{modelName}'), lazy="dynamic")
    RKABDET = db.relationship('RKABDET', backref=db.backref(f'{modelName}'), lazy="dynamic")
    RKAD = db.relationship('RKAD', backref=db.backref(f'{modelName}'), lazy="dynamic")
    RKADDET = db.relationship('RKADDET', backref=db.backref(f'{modelName}'), lazy="dynamic")
    RKAR = db.relationship('RKAR', backref=db.backref(f'{modelName}'), lazy="dynamic")
    RKARDET = db.relationship('RKARDET', backref=db.backref(f'{modelName}'), lazy="dynamic")
    DPAD = db.relationship('DPAD', backref=db.backref(f'{modelName}'), lazy="dynamic")
    DPADETD = db.relationship('DPADETD', backref=db.backref(f'{modelName}'), lazy="dynamic")
    DPAB = db.relationship('DPAB', backref=db.backref(f'{modelName}'), lazy="dynamic")
    DPADETB = db.relationship('DPADETB', backref=db.backref(f'{modelName}'), lazy="dynamic")
    DPAR = db.relationship('DPAR', backref=db.backref(f'{modelName}'), lazy="dynamic")
    DPADETR = db.relationship('DPADETR', backref=db.backref(f'{modelName}'), lazy="dynamic")
    TBPDETD = db.relationship('TBPDETD', backref=db.backref(f'{modelName}'), lazy="dynamic")

    # @property
    # def NMREK(self):
    #     # print(self.Projects)
    #     return self.JREK.URAIAN if self.JREK else ""

    @property
    def has_child(self):
        count = db.session.query(func.count(DAFTREKENING.id)).filter(DAFTREKENING.parent_id > self.id).scalar()
        return count > 0


# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, DAFTREKENING)


@event.listens_for(DAFTREKENING, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(DAFTREKENING, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(DAFTREKENING, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(DAFTREKENING, 'after_insert')
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


@event.listens_for(DAFTREKENING, 'after_update')
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


@event.listens_for(DAFTREKENING, 'after_delete')
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
