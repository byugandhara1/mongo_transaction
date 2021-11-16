from crud import create
from fastapi import APIRouter, Depends
from crud import get_db, create
router = APIRouter()


@router.post("/api/create/", tags=["create"])
async def create_template(database: object = Depends(get_db)):
    print("inside roooooouuuuuuuueeeeeee")
    # try:
    await create()

    return "result"
    # except Exception as e:
    #     print(" hhg")
