from pydantic import BaseModel
from typing import List

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
class Ingredient(BaseModel): #Zutat
    name: str


class Step(BaseModel): #Schritt
    text: str


# Rezept erstellen
class RecipeCreate(BaseModel): #Rezept erstllen mit den Schritten und Zutaten
    title: str
    description: str
    ingredients: List[Ingredient]
    steps: List[Step]

class RecipeUpdate(BaseModel): #Rezept ändern
    title: str | None = None
    description: str | None = None
    ingredients: List[Ingredient] | None = None
    steps: List[Step] | None = None

class RecipeResponse(BaseModel): #
    id: int
    title: str
    description: str
    ingredients: List[Ingredient]
    steps: List[Step]

    class Config:
        from_attributes = True
    