from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """Benutzertabelle – hier könnt ihr weitere Felder ergänzen."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False) #Username max 100 Zeichen
    email = Column(String(200), unique=True, nullable=False) #Email max 200 zeichen
    hashed_password = Column(String(200), nullable=False) #Passwort max 200 Zeichen

    recipes = relationship("Recipe", back_populates="user")
    ratings = relationship("Rating", back_populates="user")
    shopping_list_items = relationship("ShoppingListItem", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False) #Name maximal 100 Zeichen
    description = Column(String(500)) # Beschreibung maximal 500 Zeichen

    recipes = relationship("Recipe", back_populates="category")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    steps = Column(Text)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="recipes")
    category = relationship("Category", back_populates="recipes")
    ingredients = relationship("Ingredient", back_populates="recipe", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="recipe", cascade="all, delete-orphan")


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    name = Column(String(200), nullable=False)
    amount = Column(String(50))
    unit = Column(String(50))

    recipe = relationship("Recipe", back_populates="ingredients")
    shopping_list_items = relationship("ShoppingListItem", back_populates="ingredient")


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    stars = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")


class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    checked = Column(Boolean, default=False)

    user = relationship("User", back_populates="shopping_list_items")
    ingredient = relationship("Ingredient", back_populates="shopping_list_items")