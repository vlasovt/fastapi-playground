from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_company_name():
    return {"company_name": "Company Ltd"}

@router.get("/employees")
async def get_number_of_employees():
    return 234