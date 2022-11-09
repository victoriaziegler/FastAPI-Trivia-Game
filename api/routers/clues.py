from .categories import CategoryOut
from fastapi import APIRouter, status, Response
from pydantic import BaseModel
import psycopg


router = APIRouter()


class ClueOut(BaseModel):
    id: int
    answer: str
    question: str
    value: int
    invalid_count: int
    category: CategoryOut
    canon: bool


class Clues(BaseModel):
    page_count: int
    clues: list[ClueOut]


class Message(BaseModel):
    message: str


@router.get("/api/clues/{clue_id}", response_model=ClueOut, responses={404: {"model": Message}})
def get_clue(clue_id: int, response: Response):
    with psycopg.connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT clues.id as clue_id, clues.answer, clues.question, clues.value, clues.invalid_count, clues.canon as clue_canon,
                        categories.id as cat_id, categories.title, categories.canon as cat_canon
                FROM categories
                JOIN clues ON (clues.category_id = categories.id)
                WHERE clues.id = %s
                """,
                [clue_id],
            )
            record = None
            row = cur.fetchone()
            if row:
                record = {}
                clue_fields = [
                    "clue_id",
                    "answer",
                    "question",
                    "value",
                    "invalid_count",
                    "clue_canon",
                ]
                for i, column in enumerate(cur.description):
                    if column.name in clue_fields:
                        record[column.name] = row[i]
                record["id"] = record["clue_id"]
                record["canon"] = record["clue_canon"]
                category = {}
                category_fields = [
                    "cat_id",
                    "title",
                    "cat_canon",
                ]
                for i, column in enumerate(cur.description):
                    if column.name in category_fields:
                        category[column.name] = row[i]
                category["id"] = category["cat_id"]
                category["canon"] = category["cat_canon"]
                record["category"] = category
            if record is None:
                response.status_code = status.HTTP_404_NOT_FOUND
            return record
