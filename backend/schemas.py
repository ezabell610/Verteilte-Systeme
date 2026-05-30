from pydantic import BaseModel, Field
from typing import List, Optional

# --- Auth-Schemas ---

class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str


# TODO: Fügt hier eure eigenen Schemas hinzu
# class ItemCreate(BaseModel):
#     name: str
#     price: int
#
# class ItemResponse(BaseModel):
#     id: int
#     name: str
#     price: int
#     model_config = {"from_attributes": True}
class IngredientCreate(BaseModel): #Zutat
    name: str
    amount: str =""
    unit:str = ""
    
class IngedientResponse(BaseModel):
    id: int
    name: str
    amount: str
    unit: str
    model_config = {"from_attributes": True}


class Step(BaseModel): #Schritt
    text: str


# Rezept erstellen
class RecipeCreate(BaseModel): #Rezept erstllen mit den Schritten und Zutaten
    title: str
    description: str
    steps: str
    category_id: int
    is_public: bool = True
    ingredients: List[IngredientCreate]

class RecipeUpdate(BaseModel): #Rezept ändern
    title: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[str] = None
    category_id: Optional[int] = None
    is_public: Optional[bool] = None
    ingredients: Optional[List[IngredientCreate]] = None

class RecipeResponse(BaseModel): #
    id: int
    title: str
    description: str
    steps: str
    is_public: bool
    category_id: int
    user_id: int
    ingredients: List[IngedientResponse]
    model_config = {"from_attributes":True}
    
        
class RatingCreate(BaseModel):
    stars: int = Field(ge=1,le=5)
    
    
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    model_config = {"from_attributes" : True}
    
    
class ShoppingListItemCreate(BaseModel):
    ingredient_id: int
    
    
class ShoppingListItemResponse(BaseModel):
    id: int
    ingredient_id: int
    checked: bool
    ingredient: IngedientResponse
    model_config = {"from_attributes" : True}
    
class RecipeResponse(BaseModel):
    id: int
    title: str
    description: str
    steps: str
    is_public: bool
    category_id: int
    user_id: int
    ingredients: List[IngedientResponse]
    average_rating: float = 0.0
    model_config = {"from_attributes": True}
    