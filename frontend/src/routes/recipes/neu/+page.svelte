<script lang="ts">
    import { isLoggedIn } from "$lib/api";

    const kategorien = ['Vegan', 'Italienisch', 'Desserts', 'Asiatisch', 'Schnelle Küche'];

    let title = $state('');
    let description = $state('');
    let category = $state('Vegan');
    let steps = $state('');
    let is_public = $state(true);
    let ingredients = $state([
        { name: '', amount: '', unit: '' }
    ]);

    let fehler = $state('');
    let erfolg = $state('');

    function addIngredient() {
        ingredients = [...ingredients, { name: '', amount: '', unit: ''}];
    }

    function removeIngredient(index: number) {
        ingredients = ingredients.filter((_, i) => i !== index);
    }

    async function handleSubmit() {
        console.log('Button geklickt!');
        console.log('Title:', title);
        console.log ('Description:', description);
        console.log('Steps:', steps);

        if (!title || !description || !steps) {
            fehler = 'Bitte alle Felder ausfüllen!';
            console.log('Felder fehlen');
            return;
        }
        // TODO: Später durch echten API-Call ersetzen
        // await createRecipe({ title, description, category, steps, is_public, ingredients });

        erfolg = 'Rezept erfolgreich erstellt!';
        fehler = '';
    }
</script>

{#if !isLoggedIn()}
    <main>
        <p>Bitte loggen Sie sich ein, um ein Rezept zu erstellen.</p>
        <a href="/login">Zum Login</a>
    </main>
{:else}
    <main>
        <a href="/" class="zurück">Zurück</a>
        <h1> Neues Rezept erstellen</h1>

        {#if fehler}
            <p class="fehler">{fehler}</p>
        {/if}
        {#if erfolg}
            <p class="erfolg">{erfolg}</p>
        {/if}

        <label>Titel</label>
        <input type="text" placeholder="z.B. Spaghetti Bolognese" bind:value={title} />

        <label>Beschreibung</label>
        <textarea placeholder="Kurze Beschreibung des Rezepts" bind:value={description}></textarea>

        <label>Kategorie</label>
        <select bind:value={category}>
            {#each kategorien as kat}
                <option value={kat}>{kat}</option>
            {/each}
        </select>

        <label>Zubereitung</label>
        <textarea placeholder="Schritt für Schritt Anleitung..." bind:value={steps} rows="5"></textarea>

        <label>
            <input type="checkbox" bind:checked={is_public} />
            Rezept öffentlich sichtbar
        </label>

        <h2>Zutaten</h2>
        {#each ingredients as zutat, i}
            <div class="zutat-row">
                <input type="text" placeholder="Menge" bind:value={zutat.amount} />
                <input type="text" placeholder="Einheit" bind:value={zutat.unit} />
                <input type="text" placeholder="Zutat" bind:value={zutat.name} />
                <button class="remove-btn" onclick={() => removeIngredient(i)}>x</button>
            </div>
        {/each}
        <button class="add-btn" onclick={addIngredient}>+ Zutat hinzufügen</button>

        <button class="submit-btn" onclick={() => handleSubmit()}>Rezept erstellen</button>
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
    h1 {
        margin: 1rem 0;
    }
    h2 {
        color: #04545b;
        margin-top: 1.5rem;
    }
    label {
        display: block;
        margin-top: 1rem;
        font-weight: bold;
        font-size: 0.95rem;
    }
    input[type="text"], textarea, select {
        width: 100%;
        padding: 0.6rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 6px;
        margin-top: 0.3rem;
        box-sizing: border-box;
        font-family: sans-serif;
    }
    textarea {
        resize: vertical;
        min-height: 80px;
    }
    .zutat-row {
        display: flex;
        gap: 0.5rem;
        margin-top: 0.5rem;
    }
    .zutat-row input:nth-child(1) { width: 80px; }
    .zutat-row input:nth-child(2) { width: 80px; }
    .zutat-row input:nth-child(3) { flex: 1; }
    .remove-btn {
        background: #921406;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.4rem 0.6rem;
        cursor: pointer;
    }
    .submit-btn {
        margin-top: 2rem;
        width: 100%;
        padding: 0.8rem;
        background: #04545b;
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 1.1rem;
        cursor: pointer;
        font-family: sans-serif;
    }
    .fehler { color: #921406 }
    .erfolg { color: #2a6c4b }
</style>