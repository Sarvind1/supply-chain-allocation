"""Product and chunk data models."""

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date


class Product(BaseModel):
    """Product/SKU definition from Products.csv."""
    
    razin: str = Field(..., description="SKU identifier")
    asin: str = Field(..., description="Amazon ASIN")
    qty: int = Field(..., gt=0, description="Quantity to allocate")
    cm3: float = Field(..., description="Contribution margin")
    mc_volume: float = Field(..., gt=0, description="Master carton volume")
    is_oversize: int = Field(..., ge=0, le=1, description="Oversize flag")
    parcels_per_mc: int = Field(..., gt=0, description="Units per master carton")
    currency: str = Field(default="USD", description="Currency")
    
    @validator("razin", "asin")
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Cannot be empty")
        return v.strip()


class Chunk(BaseModel):
    """Processing chunk derived from Product."""
    
    chunk_id: str = Field(..., description="Unique chunk identifier")
    product: Product = Field(..., description="Source product")
    origin: str = Field(default="Supplier", description="Starting location")
    ready_date: Optional[date] = Field(None, description="Availability date")
    
    @property
    def razin(self) -> str:
        return self.product.razin
    
    @property
    def qty(self) -> int:
        return self.product.qty
    
    @property
    def cm3(self) -> float:
        return self.product.cm3