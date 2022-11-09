from pydantic import BaseModel
from fastapi import APIRouter, Depends, Response

from db import CategoryQueries

router = APIRouter()


class CategoryIn(BaseModel):
    title: str
    canon: bool


class CategoryOut(BaseModel):
    id: int
    title: str
    canon: bool


class CategoriesOut(BaseModel):
    categories: list[CategoryOut]


@router.get("/api/categories", response_model=CategoriesOut)
def categories_list(queries: CategoryQueries = Depends()):
    return {
        "categories": queries.get_all_categories()
    }


@router.get("/api/categories/{category_id}", response_model=CategoryOut)
def get_category(
    category_id: int,
    response: Response,
    queries: CategoryQueries = Depends(),
):
    record = queries.get_category(category_id)
    if record is None:
        response.status_code = 404
    else:
        return record


@router.post("/api/categories", response_model=CategoryOut)
def create_category(category_in: CategoryIn, queries: CategoryQueries = Depends()):
    return queries.create_category(category_in)


@router.put("/api/categories/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    category_in: CategoryIn,
    response: Response,
    queries: CategoryQueries = Depends(),
):
    record = queries.update_category(category_id, category_in)
    if record is None:
        response.status_code = 404
    else:
        return record


@router.delete("/api/categories/{category_id}", response_model=bool)
def delete_category(category_id: int, queries: CategoryQueries = Depends()):
    queries.delete_category(category_id)
    return True
