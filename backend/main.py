from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import (DUMMY_HASH,create_access_token,get_current_user,get_password_hash,verify_password,)
from database import Base, engine, get_db
from models import User, Recipe, Ingredient, Rating, ShoppingListItem, Category
from schemas import Token, UserRegister, UserResponse, RecipeCreate, RecipeResponse, RecipeUpdate, RatingCreate, CategoryResponse, ShoppingListItemCreate, ShoppingListItemResponse

# Tabellen anlegen (falls noch nicht vorhanden)
Base.metadata.create_all(bind=engine)
# Beispieldaten einfügen (nur falls DB leer ist)
from seed import seed_database
from database import SessionLocal
_db = SessionLocal()
try:
    seed_database(_db)
finally:
    _db.close()

app = FastAPI(title="Mein Projekt", version="0.1.0")

# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------
@app.on_event("startup")
def seed_categories():
    db = next(get_db())
    try:
        if db.query(Category).count() == 0:
            for name in ["Vegan", "Italienisch", "Desserts", "Asiatisch", "Schnelle Küche"]:
                db.add(Category(name=name))
            db.commit()
    finally:
        db.close()


app.add_middleware (
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Authentifizierung
# ---------------------------------------------------------------------------

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """Neuen Benutzer anlegen. Passwort wird als Argon2-Hash gespeichert."""
    # TODO: Implementiert diese Funktion
    # 1. Prüft, ob username oder email bereits existieren (→ 400)
    existing_user = db.query(User).filter((User.username == data.username) | (User.email == data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Benutzername oder Email existiert bereits")
    # 2. Passwort hashen mit get_password_hash()
    hashed_password = get_password_hash(data.password)
    # 3. User-Objekt anlegen, in DB speichern, zurückgeben
    user = User(username=data.username,email=data.email,hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/token", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db: Session = Depends(get_db),):
    """
    OAuth2 Password Flow: Empfängt username + password als Formular-Daten.
    Gibt einen JWT zurück.
    """
    # TODO: Implementiert diese Funktion
    # 1. Benutzer anhand von form_data.username in der DB suchen
    user = db.query(User).filter(User.username == form_data.username).first()
    # 2. Passwort mit verify_password() prüfen (Timing-Schutz: DUMMY_HASH nutzen)
    hashed = user.hashed_password if user else DUMMY_HASH
    valid = verify_password(form_data.password,hashed)
    # 3. Bei Fehler: 401 zurückgeben (generische Meldung!)
    if not user or not valid:
        raise HTTPException(status_code=401,detail="Ungültige Anmeldedaten",headers={"WWW-Authenticate": "Bearer"},)
    # 4. JWT mit create_access_token() erzeugen und zurückgeben
    access_token = create_access_token(username=user.username)
    return {"access_token": access_token,"token_type": "bearer"}


@app.get("/my-profile", response_model=UserResponse)
def get_profile(current_username: Annotated[str, Depends(get_current_user)],db: Session = Depends(get_db),):
    """Gibt das Profil des eingeloggten Benutzers zurück (geschützter Endpoint)."""
    # TODO: Implementiert diese Funktion
    # Hinweis: current_username kommt bereits validiert aus dem JWT (via Depends)
    user = db.query(User).filter(User.username == current_username).first()
    if user is None:
        raise HTTPException(status_code=404,detail="Benutzer nicht gefunden")
    return user
    

# ---------------------------------------------------------------------------
# TODO: Eure eigenen Endpoints hier einfügen
# ---------------------------------------------------------------------------

# Beispiel:
# @app.get("/items")
# def get_items(db: Session = Depends(get_db)):
#     return db.query(Item).all()
#
# @app.post("/items", status_code=201)
# def create_item(data: ItemCreate, db: Session = Depends(get_db)):
#     item = Item(**data.model_dump())
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item
@app.get("/recipes", response_model=list[RecipeResponse]) #alle Rezepte laden
def get_recipes(search: str = "", category_id: int = 0, db: Session = Depends(get_db)):
    query = db.query(Recipe).filter(Recipe.is_public == True)
    if search:
        query = query.filter(Recipe.title.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(Recipe.category_id == category_id)
    return query.all()


@app.get("/recipes/{id}", response_model=RecipeResponse) #einzelne Rezepte laden
def get_recipe(id: int, db: Session = Depends(get_db)):
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if recipe is None:
        raise HTTPException(status_code=404,detail="Rezept nicht gefunden")
    if recipe.is_public:
        return recipe
    if not recipe.is_public:
        raise HTTPException(status_code=401,detail="Anmeldung erforderlich")
    return recipe


@app.post("/recipes",response_model=RecipeResponse,status_code=201) #Rezept erstellen
def create_recipe(data: RecipeCreate, current_username: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    recipe = Recipe(
        title = data.title, 
        description = data.description, 
        steps = data.steps, 
        category_id = data.category_id, 
        is_public = data.is_public, 
        user_id = user.id
    )
    db.add(recipe)
    db.flush()
    for ing in data.ingredients:
        db.add(Ingredient(recipe_id = recipe.id, name = ing.name, amount = ing.amount, unit = ing.unit))
    db.commit()
    db.refresh(recipe)
    return recipe

@app.get("/my-recipes", response_model=list[RecipeResponse])
def get_my_recipes(current_username: Annotated[str, Depends(get_current_user)],db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    return db.query(Recipe).filter(Recipe.user_id == user.id).all()


@app.put("/recipes/{id}",response_model=RecipeResponse) #Rezept verändern
def update_recipe( id: int,data: RecipeUpdate, current_username: Annotated[str, Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    recipe = db.query(Recipe).filter(Recipe.id == id,Recipe.user_id == user.id).first()
    if not recipe:
        raise HTTPException(status_code = 404, detail = "Rezept nicht gefunden")
    if data.title is not None:
        recipe.title = data.title
    if data.description is not None:
        recipe.description = data.description
    if data.steps is not None:
        recipe.steps = data.steps
    if data.category_id is not None:
        recipe.category_id = data.category_id
    if data.is_public is not None:
        recipe.is_public = data.is_public
    if data.ingredients is not None:
        db.query(Ingredient).filter(Ingredient.recipe_id == id).delete()
        for ing in data.ingredients:
            db.add(Ingredient(recipe_id = id, name = ing.name, amount= ing.amount, unit = ing.unit))
    db.commit()
    db.refresh(recipe)
    return recipe


@app.delete("/recipes/{id}") #Rezept löschen
def delete_recipe(id: int, current_username: Annotated[str, Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    recipe = db.query(Recipe).filter(Recipe.id == id, Recipe.user_id == user.id).first()
    if recipe is None:
        raise HTTPException(status_code=404,detail="Rezept nicht gefunden")
    db.delete(recipe)
    db.commit()
    return {"message": "Rezept gelöscht"}

@app.post("/recipes/{id}/ratings")
def add_rating(id: int,data: RatingCreate, current_username: Annotated[str, Depends(get_current_user)],db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    recipe = db.query(Recipe).filter(Recipe.id == id).first()
    if not recipe:
        raise HTTPException(status_code=404,detail="Rezept nicht gefunden")
    existing = db.query(Rating).filter(Rating.user_id == user.id, Rating.recipe_id == id).first()
    if existing:
        existing.stars = data.stars
    else:
        db.add(Rating(user_id = user.id, recipe_id = id, stars = data.stars))
    db.commit()
    db.refresh(recipe)
    return {"message": "Bewertung gespeichert"}

@app.get("/shopping-list", response_model=list[ShoppingListItemResponse])
def get_shopping_list(current_username: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    return db.query(ShoppingListItem).filter(ShoppingListItem.user_id == user.id).all()

@app.post("/shopping-list", response_model=ShoppingListItemResponse, status_code=201)
def add_to_shopping_list(data: ShoppingListItemCreate, current_username: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    item = ShoppingListItem(user_id=user.id, ingredient_id=data.ingredient_id, checked=False)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.put("/shopping-list/{id}")
def toggle_shopping_item(id: int, current_username: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    item = db.query(ShoppingListItem).filter(ShoppingListItem.id == id, ShoppingListItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    item.checked = not item.checked
    db.commit()
    return {"message": "Aktualisiert"}

@app.delete("/shopping-list/{id}")
def remove_from_shopping_list(id: int, current_username: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == current_username).first()
    item = db.query(ShoppingListItem).filter(ShoppingListItem.id == id, ShoppingListItem.user_id == user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Eintrag nicht gefunden")
    db.delete(item)
    db.commit()
    return {"message": "Entfernt"}

@app.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()