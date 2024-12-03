from pydantic import BaseModel, Field


class NoteIn(BaseModel):
    title: str = Field(max_length=100)
    content: str = Field(max_length=1000)

class NoteOut(NoteIn):
    id: int