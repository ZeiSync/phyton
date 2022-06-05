from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

app = _fastapi.FastAPI(
    title= 'Temperature of patients', 
    description= 'Data of patients'
)

_services.create_database()

@app.get("/",tags = ["Home"])
def Home():
    return { "Message":"Application connected!"}


@app.post("/users/", response_model=_schemas.User, tags=["User"])
def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User], tags=["User"])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User, tags=["User"])
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return db_user


@app.post("/patients/{patient_id}/patients/", response_model=_schemas.Patient, tags= ["Patient"])
def create_patient(
    user_id: int,
    patient: _schemas.PatientCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this patient does not exist"
        )
    return _services.create_patient(db=db, patient=patient, user_id=user_id)


@app.get("/patients/", response_model=List[_schemas.Patient], tags= ["Patient"])
def read_patient(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    patients = _services.get_patients(db=db, skip=skip, limit=limit)
    return patients


@app.get("/patients/{patient_id}", response_model=_schemas.Patient, tags= ["Patient"])
def read_patient(patient_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    patient = _services.get_patient(db=db, patient_id=patient_id)
    if patient is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this patient does not exist"
        )
    return patient


@app.delete("/patients/{patient_id}", tags= ["Patient"])
def delete_patient(patient_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_patient(db=db, patient_id=patient_id)
    return {"message": f"successfully deleted patient with id: {patient_id}"}


@app.put("/patients/{patient_id}", response_model=_schemas.Patient, tags= ["Patient"])
def update_patient(
    patient_id: int,
    patient: _schemas.PatientCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.update_patient(db=db, patient=patient, patient_id=patient_id)