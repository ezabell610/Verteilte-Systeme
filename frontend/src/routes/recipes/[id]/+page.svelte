<script lang="ts">
    import StarRating from "$lib/StarRating.svelte";
    import { isLoggedIn } from "$lib/api";
    import { page } from '$app/stores';

    //Die daten hier muss man noch anpassen wenn isabell fertig ist
    const recipes = [
        {
            id: 1,
            title: 'Spaghetti Bolognese',
            description: 'Klassisches italienisches Nudelgericht',
            category: 'Italienisch',
            stars: 4,
            is_public: true,
            ingredients: [
                { name: 'Spaghetti', amount: '400', unit: 'g' },
                { name: '(Veganes) Hackfleisch', amount: '500', unit: 'g' },
                { name: 'Tomaten', amount: '400', unit: 'g' },
                { name: 'Zwiebel', amount: '1', unit: 'Stück' }
            ],
            steps: 'Zwiebeln anbraten. Hack dazugeben. Tomaten hinzufügen. 20 min köcheln lassen. Mit Spaghetti servieren.'
        },
        {
            id: 2,
            title: 'Vegane Bowl',
            description: 'Gesunde Bowl mit Quinoa und Avocado',
            category: 'Vegan',
            stars: 5,
            is_public: true,
            ingredients: [
                { name: 'Quinoa', amount: '200', unit: 'g' },
                { name: 'Kichererbsen', amount: '150', unit: 'g' },
                { name: 'Spinat', amount: '100', unit: 'g' },
                { name: 'Avocado', amount: '1', unit: 'Stück' }
            ],
            steps: 'Quinoa kochen. Kichererbsen rösten. Avocado schneiden. Alles in einer Bowl anrichten.'
        },
        {
            id: 3,
            title: 'Geheimes Rezept',
            description: 'Loggen Sie sich ein, um dieses Rezept zu sehen.',
            category: 'Desserts',
            stars: 4,
            is_public: false,
            ingredients: [
                { name: 'Zucker', amount: '200', unit: 'g' },
                { name: 'Mehl', amount: '300', unit: 'g' }
            ],
            steps: 'Loggen Sie sich ein, um die Schritte zu sehen.'
        },
        {
            id: 4,
			title: 'Gebratener Reis',
			description: 'Schnelles asiatisches Reisgericht',
			category: 'Asiatisch',
			stars: 3,
			is_public: true,
            ingredients: [
                { name: 'Reis', amount: '300', unit: 'g' },
                { name: 'Sojasauce', amount: '3', unit: 'EL' },
                { name: 'Ei', amount: '2', unit: 'Stück' }
            ],
            steps: 'Reis kochen. Ei anbraten. Reis dazugeben. Sojasauce hinzufügen.'
        },
        {
            id: 5,
			title: 'Tomatensuppe',
			description: 'Loggen Sie sich ein, um dieses Rezept zu sehen.',
			category: 'Schnelle Küche',
			stars: 4,
			is_public: false,
            ingredients: [
                { name: 'Tomaten', amount: '500', unit: 'g' },
                { name: 'Sahne', amount: '100', unit: 'ml' },
                { name: 'Zwiebel', amount: '1', unit: 'Stück' }
            ],
            steps: 'Loggen Sie sich ein, um die Schritte zu sehen.'
        }
    ];

    const id = Number($page.params.id);
    const recipe = recipes.find(r => r.id === id);
</script>

{#if !recipe}
    <main>
        <p>Rezept nicht gefunden.</p>
        <a href="/">Zurück zur Startseite</a>
    </main>
{:else if !recipe.is_public && !isLoggedIn()}
    <main>
        <p>Dieses Rezept ist privat. Bitte loggen Sie sich ein.</p>
        <a href="/login">Zum Login</a>
    </main>
{:else}
    <main>
        <a href="/" class="zurück">Zurück</a>

        <div class="header">
            <h1>{recipe.title}</h1>
            {#if isLoggedIn()}
                <a href="/recipes/{recipes.id}/edit" class="edit-btn">Bearbeiten</a>
            {/if}
        </div>

        <span class="kategorie">{recipe.category}</span>
        <StarRating 
            rating={recipe.stars}
            onRate={isLoggedIn() ? (stars) => { alert('Du hast ' + stars + ' Sterne vergeben!') } : null} 
        /> 
        <p class="beschreibung">{recipe.description}</p>

        <h2>Zutaten</h2>
        <ul class="zutaten">
            {#each recipe.ingredients as zutat}
                <li>{zutat.amount} {zutat.unit} {zutat.name}</li>
            {/each}
        </ul>

        <h2>Zubereitung</h2>
        <p class="schritte">{recipe.steps}</p>
    </main>
{/if}

<style>
    main {
        max-width: 700px;
        margin: 2rem auto;
        padding: 0 1rem;
        font-family: sans-serif;
    }
    .zurück {
        color: #04545b;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0 0.5rem 0;
    }
    h1 {
        margin: 0;
    }
    .edit-btn {
        background-color: #04545b;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .kategorie {
        background: #04545b;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.8rem;
    }
    .sterne {
        margin: 0.8rem 0;
    }
    .beschreibung {
        color: #555;
        margin-bottom: 1.5rem;
    }
    h2 {
        color: #04545b;
        border-bottom: 2px solid #04545b;
        padding-bottom: 0.3rem;
    }
    .zutaten {
        line-height: 2;
    }
    .schritte {
        line-height: 1.8;
        color: #333;
    }
</style>