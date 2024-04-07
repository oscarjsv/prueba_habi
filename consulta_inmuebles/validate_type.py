from pydantic import BaseModel, ValidationError, validator
from typing import Optional


class QueryParams(BaseModel):

    year: Optional[int] = None
    city: Optional[str] = None
    state: Optional[str] = None

    @validator('state')
    def validate_status(cls, v):
        allowed_statuses = ["pre_venta", "en_venta", "vendido"]
        if v not in allowed_statuses:
            raise ValueError("Invalid status")
        return v


def validate_query_params(query_params):
    try:
        if not query_params:
            return
        else:
            query_params_cleaned = {key: value[0]
                                    for key, value in query_params.items()}
            validated_params = QueryParams(**query_params_cleaned)
            return validated_params
    except ValidationError as e:
        # If there are validation errors, we capture them and return a list of error messages
        error_messages = [
            f"{error['loc'][0]} - {error['msg']}" for error in e.errors()]
        return error_messages
