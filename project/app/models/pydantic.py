from pydantic import BaseModel, HttpUrl


class SummaryPayloadSchema(BaseModel):
    url: HttpUrl


class SummaryResponseSchema(SummaryPayloadSchema):
    id: int


class SummaryUpdatePayloadSchema(SummaryPayloadSchema):
    summary: str
