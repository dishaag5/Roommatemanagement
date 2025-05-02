from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, database
from app.auth import get_current_user
household_router = APIRouter()




def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@household_router.post("/households", response_model=schemas.HouseholdOut)
def create_household(household: schemas.HouseholdCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_household = models.Household(name=household.name, owner_id=current_user.id)
    db.add(new_household)
    db.commit()
    db.refresh(new_household)

    new_household.members.append(current_user)

    # owner = db.query(models.User).get(current_user.id)
    # if owner:
    #     new_household.members.append(current_user)
    #     db.commit()

    return new_household


@household_router.post("/households/join")
def join_household(
    token: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    household = db.query(models.Household).filter(models.Household.invite_token == token).first()

    if not household:
        raise HTTPException(status_code=404, detail="Invalid invite token")

    if current_user in household.members:
        raise HTTPException(status_code=400, detail="User already in household")

    household.members.append(current_user)
    db.commit()

    return {"message": f"Joined household '{household.name}'"}

