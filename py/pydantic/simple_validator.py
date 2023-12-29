from pydantic import BaseModel, field_validator
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    @field_validator('price')
    def price_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError('Price must be positive')
        return value

    def total_price(self) -> float:
        return self.price + (self.tax if self.tax else 0)

# Create an Item object with validation.
# This will raise an error if price is not positive.
item = Item(name='Coffee', description='Hot beverage', price=3.5, tax=0.7)
print(item)
print(item.total_price())
print("--"*5)
item.price_must_be_positive(-4.5)

