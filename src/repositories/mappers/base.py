#  Базовый маппер паттерна Data Mapper
from typing import TypeVar

from pydantic import BaseModel

from src.database import Base


DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    db_model: type[DBModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, db_model_data):  # Ф-я для превращения sqlalc модели в pydantic схему
        return cls.schema.model_validate(db_model_data, from_attributes=True)
    
    @classmethod
    def map_to_persistence_entity(cls, schema_data):  # Ф-я для превращения pydantic схему в sqlalc модель
        return cls.db_model(**schema_data.model_dump())
