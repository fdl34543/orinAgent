from fastapi import APIRouter
from app.core.job_service import (
    list_jobs,
    apply_job,
    resign_job,
    pay_salary
)

router = APIRouter(prefix="/job")


@router.get("/list")
def job_list():
    return list_jobs()


@router.post("/apply")
def job_apply(agent_id: str, location: str, job: str):
    return apply_job(agent_id, location, job)


@router.post("/resign")
def job_resign(agent_id: str):
    return resign_job(agent_id)


@router.post("/salary/claim")
def salary_claim(agent_id: str):
    return pay_salary(agent_id)
