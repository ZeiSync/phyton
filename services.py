import sqlalchemy.orm as _orm

import models as _models, schemas as _schemas, database as _database


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(db: _orm.Session, user_id: int):
    return db.query(_models.User).filter(_models.User.id == user_id).first()


def get_user_by_email(db: _orm.Session, email: str):
    return db.query(_models.User).filter(_models.User.email == email).first()


def get_users(db: _orm.Session, skip: int = 0, limit: int = 100):
    return db.query(_models.User).offset(skip).limit(limit).all()


def create_user(db: _orm.Session, user: _schemas.UserCreate):
    fake_hashed_password = user.password + "thisisnotsecure"
    db_user = _models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_patients(db: _orm.Session, skip: int = 0, limit: int = 10):
    return db.query(_models.Patient).offset(skip).limit(limit).all()


def create_patient(db: _orm.Session, patient: _schemas.PatientCreate, user_id: int):
    patient = _models.Patient(**patient.dict(), owner_id=user_id)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient(db: _orm.Session, patient_id: int):
    return db.query(_models.Patient).filter(_models.Patient.id == patient_id).first()


def delete_patient(db: _orm.Session, patient_id: int):
    db.query(_models.Patient).filter(_models.Patient.id == patient_id).delete()
    db.commit()


def update_patient(db: _orm.Session, patient_id: int, patient: _schemas.PatientCreate):
    db_patient = get_patient(db=db, patient_id=patient_id)
    db_patient.first_name = patient.first_name
    db_patient.last_name = patient.last_name
    db_patient.age = patient.age
    db_patient.temp = patient.temp
    db.commit()
    db.refresh(db_patient)
    return db_patient