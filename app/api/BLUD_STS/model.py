from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class STS(db.Model):
    __tablename__ = 'STS'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDUNIT = db.Column(db.BigInteger, db.ForeignKey("DAFTUNIT.id"), nullable=False)
    IDBEND = db.Column(db.BigInteger, db.ForeignKey("BEND.id"), nullable=False)
    KDSTATUS = db.Column(db.String(5), db.ForeignKey("STATTRS.KDSTATUS"), nullable=False)
    IDKAS = db.Column(db.BigInteger, db.ForeignKey("BKBKAS.id"), nullable=False)
    IDXKODE = db.Column(db.Integer, nullable=False)
    NOSTS = db.Column(db.String(100), nullable=True)
    TGLSTS = db.Column(db.DateTime, default=datetime.now, nullable=True)
    URAIAN = db.Column(db.String(100), nullable=True)
    TGLVALID = db.Column(db.DateTime, default=datetime.now, nullable=True)
    KDRILIS = db.Column(db.BigInteger,  nullable=True)
    STKIRIM = db.Column(db.Integer, nullable=True)
    STCAIR = db.Column(db.Integer, nullable=True)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    # STSD = db.relationship('STSD', backref=db.backref(f'{modelName}'), lazy="dynamic")

    @property
    def KDUNIT(self):
        return self.DAFTUNIT.KDUNIT if self.DAFTUNIT else ""

    @property
    def UNIT(self):
        return self.DAFTUNIT.NMUNIT if self.DAFTUNIT else ""

    # @property
    # def REKENING(self):
    #     return self.DAFTREKENING.NMPER if self.DAFTREKENING else ""

    # @property
    # def TAHAPAN(self):
    #     return self.TAHAP.URAIAN if self.TAHAP else ""

    @property
    def URAISTATUS(self):
        return self.STATTRS.URAIAN if self.STATTRS else ""

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, STS)


@event.listens_for(STS, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(STS, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(STS, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(STS, 'after_insert')
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