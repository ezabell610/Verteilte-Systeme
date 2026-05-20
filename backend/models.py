from sqlalchemy import Column, Integer, String, Table, ForeignKey, Text, relationship
from database import Base


class User(Base):
    """Benutzertabelle – hier könnt ihr weitere Felder ergänzen."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)


# TODO: Fügt hier eure eigenen Modelle hinzu
# class Item(Base):
#     __tablename__ = "items"
#     id    = Column(Integer, primary_key=True, index=True)
#     name  = Column(String(100), nullable=False)
#     ...
recipe_tags = Table("recipe_tags",Base.metadata,Column("recipe_id",ForeignKey("recipes.id"),primary_key=True),
    Column("tag_id",ForeignKey("tags.id"),primary_key=True))

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    tags = relationship("Tag",secondary=recipe_tags,back_populates="recipes")
    ratings = relationship("Rating",back_populates="recipe")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    recipe_id = Column(Integer,ForeignKey("recipes.id"))
    recipe = relationship("Recipe",back_populates="ratings")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String,unique=True)
    recipes = relationship("Recipe",secondary=recipe_tags,back_populates="tags")