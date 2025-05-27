from datetime import datetime
from threading import Thread

from sqlalchemy import event
from sqlalchemy.dialects import mssql
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.sso_helper import check_unit_privilege_on_changes_db, insert_user_activity, current_user, \
    check_unit_and_employee_privilege_on_read_db
from app.utils import row2dict
from . import crudTitle, apiPath, modelName


class SPPDETR(db.Model):
    __tablename__ = 'SPPDETR'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    IDREK = db.Column(db.BigInteger, db.ForeignKey("DAFTREKENING.id"), nullable=False)
    IDKEG = db.Column(db.BigInteger, db.ForeignKey("KEGUNIT.id"), nullable=False)
    IDSPP = db.Column(db.BigInteger, nullable=False)
    IDNOJETRA = db.Column(db.Integer, default=21, nullable=False)
    NILAI = db.Column(mssql.MONEY, nullable=True)
    DATECREATE = db.Column(db.DateTime, default=datetime.now, nullable=True)
    DATEUPDATE = db.Column(db.DateTime, default=datetime.now, nullable=True)

    kegunit_rel = db.relationship(
        'KEGUNIT',
        primaryjoin='SPPDETR.IDKEG == KEGUNIT.id',
        backref='sppdetr_items',
        lazy='joined'  # Auto join saat query
    )
    @property
    def KDPER(self):
        return self.DAFTREKENING.KDPER if self.DAFTREKENING else ""

    @property
    def NMKEGUNIT(self):
        # Debugging langsung
        if not self.kegunit_rel:
            print(f"Debug: No KEGUNIT found for SPPDETR ID {self.id} with IDKEG {self.IDKEG}")
            return ""

        if not hasattr(self.kegunit_rel, 'mkegiatan'):
            print(f"Debug: KEGUNIT {self.kegunit_rel.id} has no mkegiatan relation")
            return ""

        return self.kegunit_rel.mkegiatan.NMKEGUNIT or ""

    @property
    def NMPER(self):
        return self.DAFTREKENING.NMPER if self.DAFTREKENING else ""

    @property
    def KDUNIT(self):
        return self.DAFTUNIT.KDUNIT if self.DAFTUNIT else ""

    @property
    def UNIT(self):
        return self.DAFTUNIT.NMUNIT if self.DAFTUNIT else ""


    # @property
    # def TAHAPAN(self):
    #     return self.TAHAP.URAIAN if self.TAHAP else ""

    # @property
    # def URAISTATUS(self):
    #     return self.STATTRS.URAIAN if self.STATTRS else ""

# BEFORE TRANSACTION: CHECK PRIVILEGE UNIT
@event.listens_for(db.session, "do_orm_execute")
def check_unit_privilege_read(orm_execute_state):
    check_unit_and_employee_privilege_on_read_db(orm_execute_state, SPPDETR)


@event.listens_for(SPPDETR, 'before_insert')
def check_unit_privilege_insert(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(SPPDETR, 'before_update')
def check_unit_privilege_delete(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


@event.listens_for(SPPDETR, 'before_delete')
def check_unit_privilege_update(mapper, connection, target):
    member_of_list = current_user['member_of_list']
    check_unit_privilege_on_changes_db(mapper, connection, target, member_of_list)


# AFTER TRANSACTION: INSERT TO TABLE LOG HISTORY
@event.listens_for(SPPDETR, 'after_insert')
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