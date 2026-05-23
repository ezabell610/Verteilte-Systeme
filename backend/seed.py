"""
Seed-Script: Füllt die Datenbank beim ersten Start mit Beispieldaten.
Wird automatisch in main.py aufgerufen, nachdem die Tabellen erstellt wurden.

Wenn die DB bereits Daten enthält, wird nichts gemacht (idempotent).
"""

from sqlalchemy.orm import Session
from auth import get_password_hash
from models import User, Category, Recipe, Ingredient, Rating


def seed_database(db: Session) -> None:
    """Befüllt die Datenbank mit Beispieldaten, falls sie leer ist."""
    
    # Wenn schon User existieren, davon ausgehen dass Seed schon gelaufen ist
    if db.query(User).count() > 0:
        print("[seed] DB enthält bereits Daten, Seed übersprungen.")
        return

    print("[seed] DB ist leer, starte Seeding...")

    # --- Kategorien ---
    categories_data = [
        {"name": "Frühstück", "description": "Rezepte für den Start in den Tag"},
        {"name": "Mittagessen", "description": "Herzhafte Hauptgerichte für mittags"},
        {"name": "Abendessen", "description": "Leichte oder deftige Abendgerichte"},
        {"name": "Snack", "description": "Kleine Leckereien für zwischendurch"},
        {"name": "Dessert", "description": "Süßes für nach dem Essen"},
    ]
    categories = {}
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)
        categories[cat_data["name"]] = category
    db.commit()
    print(f"[seed] {len(categories)} Kategorien angelegt.")

    # --- Test-User ---
    users_data = [
        {"username": "selina", "email": "selina@test.de", "password": "test1234"},
        {"username": "anna", "email": "anna@test.de", "password": "test1234"},
    ]
    users = {}
    for user_data in users_data:
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
        )
        db.add(user)
        users[user_data["username"]] = user
    db.commit()
    print(f"[seed] {len(users)} Test-User angelegt.")

    # --- Rezepte ---
    recipes_data = [
        {
            "title": "Pancakes mit Ahornsirup",
            "description": "Klassische amerikanische Pancakes – fluffig und lecker.",
            "steps": "1. Mehl, Milch, Ei und Zucker zu einem Teig verrühren.\n2. Butter in einer Pfanne erhitzen.\n3. Pro Pancake einen Schöpfer Teig in die Pfanne geben.\n4. Beidseitig goldbraun backen.\n5. Mit Ahornsirup servieren.",
            "category": "Frühstück",
            "user": "selina",
            "is_public": True,
            "ingredients": [
                {"name": "Mehl", "amount": "200", "unit": "g"},
                {"name": "Milch", "amount": "300", "unit": "ml"},
                {"name": "Ei", "amount": "2", "unit": "Stück"},
                {"name": "Zucker", "amount": "2", "unit": "EL"},
                {"name": "Butter", "amount": "30", "unit": "g"},
                {"name": "Ahornsirup", "amount": "nach Belieben", "unit": ""},
            ],
        },
        {
            "title": "Spaghetti Carbonara",
            "description": "Original italienische Carbonara mit Speck und Ei.",
            "steps": "1. Spaghetti in Salzwasser al dente kochen.\n2. Speck in einer Pfanne knusprig braten.\n3. Eier mit Parmesan und Pfeffer verquirlen.\n4. Spaghetti abgießen, sofort mit Ei-Mischung und Speck vermengen.\n5. Mit extra Parmesan servieren.",
            "category": "Mittagessen",
            "user": "anna",
            "is_public": True,
            "ingredients": [
                {"name": "Spaghetti", "amount": "400", "unit": "g"},
                {"name": "Speck", "amount": "150", "unit": "g"},
                {"name": "Eier", "amount": "3", "unit": "Stück"},
                {"name": "Parmesan", "amount": "80", "unit": "g"},
                {"name": "Pfeffer", "amount": "nach Geschmack", "unit": ""},
            ],
        },
        {
            "title": "Caesar Salad",
            "description": "Frischer Salat mit knusprigen Croutons.",
            "steps": "1. Römersalat waschen und in mundgerechte Stücke schneiden.\n2. Brot würfeln und in Öl mit Knoblauch goldbraun rösten.\n3. Dressing aus Mayonnaise, Senf, Zitrone und Parmesan anrühren.\n4. Salat mit Dressing vermengen, Croutons und Parmesan darüberstreuen.",
            "category": "Mittagessen",
            "user": "selina",
            "is_public": True,
            "ingredients": [
                {"name": "Römersalat", "amount": "1", "unit": "Kopf"},
                {"name": "Brot", "amount": "100", "unit": "g"},
                {"name": "Mayonnaise", "amount": "3", "unit": "EL"},
                {"name": "Zitrone", "amount": "1/2", "unit": "Stück"},
                {"name": "Parmesan", "amount": "50", "unit": "g"},
                {"name": "Knoblauch", "amount": "1", "unit": "Zehe"},
            ],
        },
        {
            "title": "Gemüse-Curry",
            "description": "Schnelles veganes Curry mit Kokosmilch.",
            "steps": "1. Zwiebel und Knoblauch fein hacken und in Öl anbraten.\n2. Currypaste hinzufügen und kurz mitbraten.\n3. Gemüse zugeben, kurz anschwitzen.\n4. Mit Kokosmilch ablöschen und 15 Minuten köcheln lassen.\n5. Mit Reis servieren.",
            "category": "Abendessen",
            "user": "anna",
            "is_public": True,
            "ingredients": [
                {"name": "Zwiebel", "amount": "1", "unit": "Stück"},
                {"name": "Knoblauch", "amount": "2", "unit": "Zehen"},
                {"name": "Currypaste", "amount": "2", "unit": "EL"},
                {"name": "Gemüse-Mix", "amount": "500", "unit": "g"},
                {"name": "Kokosmilch", "amount": "400", "unit": "ml"},
                {"name": "Reis", "amount": "200", "unit": "g"},
            ],
        },
        {
            "title": "Bananen-Schoko-Smoothie",
            "description": "Schneller Snack für unterwegs.",
            "steps": "1. Banane schälen und in Stücke schneiden.\n2. Mit Milch, Kakao und Honig in den Mixer geben.\n3. Glatt pürieren.\n4. In ein hohes Glas füllen und sofort genießen.",
            "category": "Snack",
            "user": "selina",
            "is_public": True,
            "ingredients": [
                {"name": "Banane", "amount": "1", "unit": "Stück"},
                {"name": "Milch", "amount": "200", "unit": "ml"},
                {"name": "Kakaopulver", "amount": "1", "unit": "EL"},
                {"name": "Honig", "amount": "1", "unit": "TL"},
            ],
        },
        {
            "title": "Schoko-Mousse",
            "description": "Klassisches Dessert, schön cremig.",
            "steps": "1. Schokolade über einem Wasserbad schmelzen.\n2. Eigelb mit Zucker schaumig schlagen.\n3. Geschmolzene Schokolade unterheben.\n4. Eiweiß steif schlagen und vorsichtig unterheben.\n5. Mindestens 2 Stunden kühlen.",
            "category": "Dessert",
            "user": "anna",
            "is_public": True,
            "ingredients": [
                {"name": "Zartbitterschokolade", "amount": "200", "unit": "g"},
                {"name": "Eier", "amount": "4", "unit": "Stück"},
                {"name": "Zucker", "amount": "50", "unit": "g"},
            ],
        },
    ]

    recipe_objects = []
    for recipe_data in recipes_data:
        recipe = Recipe(
            title=recipe_data["title"],
            description=recipe_data["description"],
            steps=recipe_data["steps"],
            is_public=recipe_data["is_public"],
            user_id=users[recipe_data["user"]].id,
            category_id=categories[recipe_data["category"]].id,
        )
        db.add(recipe)
        db.flush()  # damit recipe.id verfügbar ist
        
        for ing in recipe_data["ingredients"]:
            ingredient = Ingredient(
                recipe_id=recipe.id,
                name=ing["name"],
                amount=ing["amount"],
                unit=ing["unit"],
            )
            db.add(ingredient)
        recipe_objects.append(recipe)
    db.commit()
    print(f"[seed] {len(recipe_objects)} Rezepte mit Zutaten angelegt.")

    # --- Beispielbewertungen ---
    ratings_data = [
        {"user": "anna", "recipe_index": 0, "stars": 5},  # Anna bewertet Pancakes
        {"user": "selina", "recipe_index": 1, "stars": 4},  # Selina bewertet Carbonara
        {"user": "anna", "recipe_index": 2, "stars": 5},  # Anna bewertet Caesar Salad
        {"user": "selina", "recipe_index": 3, "stars": 4},  # Selina bewertet Curry
        {"user": "anna", "recipe_index": 5, "stars": 5},  # Anna bewertet Schoko-Mousse
    ]
    for r in ratings_data:
        rating = Rating(
            user_id=users[r["user"]].id,
            recipe_id=recipe_objects[r["recipe_index"]].id,
            stars=r["stars"],
        )
        db.add(rating)
    db.commit()
    print(f"[seed] {len(ratings_data)} Bewertungen angelegt.")

    print("[seed] Seeding erfolgreich abgeschlossen.")