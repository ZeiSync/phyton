import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm

import database as _database

#create class for table

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)

    patients = _orm.relationship("Patient", back_populates="owner")


class Patient(_database.Base):
    __tablename__ = "patients"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    age = _sql.Column(_sql.Integer, index=True)
    temp= _sql.Column(_sql.DECIMAL, index=True)

    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    owner = _orm.relationship("User", back_populates="patients")