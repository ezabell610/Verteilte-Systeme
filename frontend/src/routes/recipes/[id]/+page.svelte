<script lang="ts">
    import StarRating from "$lib/StarRating.svelte";
    import { isLoggedIn } from "$lib/api";
    import { page } from '$app/stores';

    const API_BASE = 'http://localhost:8000';
    const id = Number($page.params.id);

    let recipe = $state(null);
    let loading = $state(true);
    let fehler = $state('');
    let loggedIn = $state(isLoggedIn());

    $effect(() => {
        async function loadRecipe() {
            try {
                const res = await fetch(`${API_BASE}/recipes/${id}`);
                if (!res.ok) throw new Error('Nicht gefunden');
                recipe = await res.json();
            } catch (e) {
                fehler = 'Rezept konnte nicht geladen werden.';
            } finally {
                loading = false;
            }
        }
        loadRecipe();
    });

    let kategorien = $state([]);

    $effect(() => {
        async function loadKategorien() {
            const res = await fetch(`${API_BASE}/categories`);
            kategorien = await res.json();
        }
        loadKategorien();
    });

    function getCategoryName(id: number): string {
        const kat = kategorien.find((k: any) => k.id === id);
        return kat ? kat.name : '';
    }

    async function addToShoppingList(ingredientID: number, name: string) {
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`${API_BASE}/shopping-list`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ ingredient_id: ingredientID })
            });
            if (!res.ok) throw new Error();
            alert(name + ' zur Einkaufsliste hinzugefügt!');
        } catch (e) {
            alert('Fehler beim Hinzufügen zur Einkaufsliste.');
        }
    }
</script>

{#if loading}
    <main><p>Wird geladen...</p></main>
{:else if fehler}
    <main>
        <p>{fehler}</p>
        <a href="/">Zurück zur Startseite</a>
    </main>
{:else if !recipe}
    <main>
        <p>Rezept nicht gefunden.</p>
        <a href="/">Zurück zur Startseite</a>
    </main>
{:else if !recipe.is_public && !loggedIn}
    <main>
        <p>Dieses Rezept ist privat. Bitte loggen Sie sich ein.</p>
        <a href="/login">Zum Login</a>
    </main>
{:else}
    <main>
        <a href="/" class="zurück">Zurück</a>

        <div class="header">
            <h1>{recipe.title}</h1>
            {#if loggedIn}
                <a href="/recipes/{recipe.id}/edit" class="edit-btn">Bearbeiten</a>
            {/if}
        </div>

        <span class="kategorie">{getCategoryName(recipe.category_id)}</span>
        <StarRating 
            rating={0}
            onRate={loggedIn ? async (stars) => {
                const token = localStorage.getItem('token');
                await fetch(`${API_BASE}/recipes/${id}/ratings`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({ stars })
                });
                alert('Bewertung gespeichert!');
            } : null}
        /> 
        <p class="beschreibung">{recipe.description}</p>

        <h2>Zutaten</h2>
        <ul class="zutaten">
            {#each recipe.ingredients as zutat}
                <li>
                    {zutat.amount} {zutat.unit} {zutat.name}
                    {#if loggedIn}
                        <button class="add-btn" onclick={() => addToShoppingList(zutat.id, zutat.name)}>
                            + Einkaufsliste
                        </button>
                    {/if}    
                </li>
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
    .zutaten li {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .add-btn {
        background: #04545b;
        color: white;
        border: none;
        padding: 0.3rem 0.6rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 0.8rem;
        font-family: sans-serif;
    }
    .schritte {
        line-height: 1.8;
        color: #333;
    }
</style>