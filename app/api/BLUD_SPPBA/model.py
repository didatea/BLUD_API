from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class SPPBA(db.Model):
    __tablename__ = 'SPPBA'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDSPP = db.Column(db.BigInteger, nullable=False)
    IDBERITA = db.Column(db.BigInteger, db.ForeignKey("BERITA.id"), nullable=False)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    @property
    def NOBERITA(self):
        return self.BERITA.NOBERITA if self.BERITA else ""

    # @property
    # def TAHAPAN(self):
    #     return self.TAHAP.URAIAN if self.TAHAP else ""

    # @property
    # def URAISTATUS(self):
    #     return self.STATTRS.URAIAN if self.STATTRS else ""

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, SPPBA)


@event.listens_for(SPPBA, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(SPPBA, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(SPPBA, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(SPPBA, 'after_insert')
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