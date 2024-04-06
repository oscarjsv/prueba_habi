from pydantic import BaseModel, ValidationError
from typing import List


class QueryParams(BaseModel):

    year: int
    city: str
    state: str

    # @validator('state')
    # def validate_status(cls, v):
    #     allowed_statuses = ["pre_venta", "en_venta", "vendido"]
    #     if v not in allowed_statuses:
    #         raise ValueError("Estado no válido")
    #     return v


def validate_query_params(query_params):
    try:
        query_params_cleaned = {key: value[0]
                                for key, value in query_params.items()}

        print(query_params_cleaned)
        validated_params = QueryParams(**query_params_cleaned)
        print(validated_params)
        return validated_params
    except ValidationError as e:
        # Si hay errores de validación, los capturamos y devolvemos una lista de mensajes de error
        error_messages = [
            f"{error['loc'][0]} - {error['msg']}" for error in e.errors()]
        print(error_messages)
        return error_messages
