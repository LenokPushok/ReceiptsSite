from typing import Type, TypeVar, Any

ModelType = TypeVar("ModelType")


class FilterParser:
    OPERATOR_MAPPING = {
        "eq": lambda attr, value: attr == value,
        "neq": lambda attr, value: attr != value,
        "le": lambda attr, value: attr <= value,
        "ge": lambda attr, value: attr >= value,
        "in": lambda attr, value: attr.in_(value),
        "nin": lambda attr, value: attr.not_in(value),
    }

    def __init__(self, orm_model: Type[ModelType]):
        self.orm_model = orm_model

    def parse_filter(self, expression: str, value: Any):
        if "__" not in expression:
            orm_attr = getattr(self.orm_model, expression)
            return self.OPERATOR_MAPPING["eq"](orm_attr, value)
        attr, operator = expression.split("__")
        orm_attr = getattr(self.orm_model, attr)
        return self.OPERATOR_MAPPING[operator](orm_attr, value)
