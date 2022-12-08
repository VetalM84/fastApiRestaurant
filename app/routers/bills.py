"""GET endpoints for bill."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_bill, crud_waiter
from app.db.database import get_db
from app.schemas import BillBase, BillIn

router = APIRouter(prefix="/bills", tags=["bills"])


@router.post("/", response_model=BillBase, status_code=status.HTTP_201_CREATED)
async def create_bill(bill: BillIn, db: Session = Depends(get_db)):
    """Create a new bill."""
    db_waiter = crud_waiter.get_waiter(db, waiter_id=bill.waiter_id)
    if not db_waiter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Waiter not found"
        )
    return crud_bill.create_bill(db=db, bill=bill)


@router.get("/{bill_id}", response_model=BillBase, status_code=status.HTTP_200_OK)
async def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get a bill by id with a list of the ordered dishes."""
    db_bill = crud_bill.get_bill(db, bill_id=bill_id)
    if not db_bill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Bill id {bill_id} not found"
        )
    return db_bill
