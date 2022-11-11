from pydantic import BaseModel
from fastapi import APIRouter, Response, Depends

from db import CategoryQueries

router = APIRouter()


class CategoryIn(BaseModel):
    title: str


class CategoryOut(BaseModel):
    id: int
    title: str
    canon: bool


class CategoriesOut(BaseModel):
    categories: list[CategoryOut]


@router.get("/api/categories", response_model=CategoriesOut)
def list_all_categories(queries: CategoryQueries = Depends()):
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


@router.put("/api/categories/{cat_id}", response_model=CategoryOut)
def update_category(category_id: int, category_in: CategoryIn, queries: CategoryQueries = Depends()):
    return queries.update_category(category_in, category_id)


@router.delete("/api/categories/{cat_id}", response_model=bool)
def delete_category(cat_id: int, queries: CategoryQueries = Depends()):
    return queries.delete_category(cat_id)
