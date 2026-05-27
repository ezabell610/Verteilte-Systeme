<script lang="ts">
    import { isLoggedIn } from "$lib/api";
    import StarRating from "$lib/StarRating.svelte";
    
    const API_BASE = 'http://localhost:8000';

    let recipes = $state([]);
    let loading = $state(true);
    let loggedIn = $state(false);

    $effect(() => {
        loggedIn = isLoggedIn()
    });

    $effect(() => {
        if (!loggedIn) return;
        async function loadMyRecipes() {
            try {
                const token = localStorage.getItem('token');
                const res = await fetch(`${API_BASE}/my-recipes`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (!res.ok) throw new Error();
                recipes = await res.json();
            } catch (e) {
                console.error('Fehler beim Laden');
            } finally {
                loading = false;
            }
        }
        loadMyRecipes();
    });

    async function deleteRecipe (id: number) {
        if (!confirm('Rezept wirklich löschen?')) return;
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`${API_BASE}/recipes/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization' : `Bearer ${token}` }
            });
            if (!res.ok) throw new Error();
            recipes = recipes.filter((r: any) => r.id !== id);
        } catch (e) {
            alert ('Fehler beim Löschen.');
        }
    }
</script>

{#if !isLoggedIn()}
    <main>
        <p>Bitte einloggen um deine Rezepte zu sehen.</p>
        <a href="/login">Zum Login</a>
    </main>
{:else}
    <main>
        <h1>Meine Rezepte</h1>
        <a href="/recipes/neu" class="neu-btn">+ Neues Rezept</a>

        {#if recipes.length === 0}
            <p class="leer">Du hast noch keine Rezepte erstellt.</p>
        {:else}
            <div class="karten">
                {#each recipes as recipe}
                    <div class="karte">
                        <div class="karte-header">
                            <h2>{recipe.title}</h2>
                            <span class="status" class:privat={!recipe.is_public}>
                                {recipe.is_public ? 'Öffentlich' : 'Privat'}
                            </span>
                        </div>
                        <span class="kategorie">{recipe.category}</span>
                        <p>{recipe.description}</p>
                        <StarRating rating={recipe.stars} />
                        <div class="aktionen">
                            <a href="/recipes/{recipe.id}">Ansehen</a>
                            <a href="/recipes/{recipe.id}/edit">Bearbeiten</a>
                            <button onclick={() => deleteRecipe(recipe.id)}>Löschen</button>
                        </div>
                    </div>
                {/each}
            </div>
        {/if}
    </main>
{/if}

<style>
    main {
        max-width: 900px;
        margin: 2rem auto;
        padding: 0.1rem;
        font-family: sans-serif;
    }
    h1 {
        margin-bottom: 0.5rem;
    }
    .neu-btn {
        display: inline-block;
        background: #04545b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-decoration: none;
        margin-bottom: 1.5rem;
        font-family: sans-serif;
    }
    .leer {
        color: #888;
        text-align: center;
        margin-top: 2rem;
    }
    .karten {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
    }
    .karte {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 2px 6px rgba(0,0, 0, 0.08)
    }
    .karte-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .karte h2 {
        margin: 0;
        font-size: 1.1rem;
        color: #04545b;
    }
    .status {
        font-size: 0.75rem;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        background: #2a6c4b;
        color: white;
    }
    .status.privat {
        background: #e74c3c;
    }
    .kategorie {
        background: #04545b;
        color: white;
        padding: 0.15rem 0.5rem;
        border-radius: 10px;
        font-size: 0.75rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .aktionen {
        display: flex;
        gap: 0.8rem;
        margin-top: 1rem;
        padding-top: 0.8rem;
        border-top: 1px solid #eee;
    }
    .aktionen a {
        color: #04545b;
        text-decoration: none;
        font-size: 0.9rem;
    }
    .aktionen button {
        background: none;
        border: none;
        color: #e74c3c;
        cursor: pointer;
        font-size: 0.9rem;
        font-family: sans-serif;
        padding: 0;
    }
</style>