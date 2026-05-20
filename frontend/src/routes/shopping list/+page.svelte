<script lang="ts">
    import { isLoggedIn } from "$lib/api";

    //Fake-Daten bis Backend fertig ist
    let items = $state([
        { id: 1, name: 'Spaghetti', amount: '400', unit: 'g', checked: false },
        { id: 2, name: 'Hackfleisch', amount: '500', unit: 'g', checked: false },
        { id: 3, name: 'Tomaten', amount: '400', unit: 'g', checked: true },
    ]);

    function toggleItem(id: number) {
        items = items.map(item =>
            item.id === id ? { ...item, checked: !item.checked } : item
        );
    }

    function removeItem(id: number) {
        items = items.filter(item => item.id !== id);
    }

    function removeChecked() {
        items = items.filter(item => !item.checked);
    }
</script>

{#if !isLoggedIn()}
    <main>
        <p>Bitte einloggen um die Einkaufsliste zu sehen.</p>
        <a href="/login">Zum Login</a>
    </main>
{:else}
    <main>
        <div class="header">
            <h1>Einkaufsliste</h1>
            {#if items.some (i => i.checked)}
                <button class="remove-checked" onclick={removeChecked}>
                    Abgehakte entfernen
                </button>
            {/if}
        </div>

        {#if items.length === 0}
            <p class="leer">Deine Einkaufsliste ist leer. Füge Zutaten von Rezepten hinzu!</p>
        {:else}
            <ul class="liste"
                {#each items as item}
                    <li class:checked={item.checked}>
                        <label>
                            <input
                                type="checkbox"
                                checked={item.checked}
                                onchange={() => toggleItem(item.id)}
                            />
                            <span class="menge">{item.amount} {item.unit}</span>
                            <span class="name">{item.name}</span>
                        </label>
                        <button class="delete-btn" onclick={() => removeItem(item.id)}>x</button>
                    </li>
                {/each}
            </ul>
        {/if}
    </main>
{/if}

<style>
    main {
        max-width: 600px;
        margin: 2rem auto;
        padding: 0 1rem;
        font-family: sans-serif;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    .remove-checked {
        background: #e74c3c;
        color: white;
        border: none;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        cursor: pointer;
        font-family: sans-serif;
    }
    .leer {
        color: #888;
        text-align: center;
        margin-top: 2rem;
    }
    .liste {
        list-style: none;
        padding: 0;
    }
    .liste li {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.8rem;
        border-bottom: 1px solid #eee;
    }
    .liste li.checked {
        opacity: 0.5;
    }
    .liste li.checked .name {
        text-decoration: line-through;
    }
    label {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        cursor: pointer;
        flex: 1;
    }
    input[type="checkbox"] {
        width: 18px;
        height: 18px;
        cursor: pointer;
    }
    .menge {
        color: #04545b;
        font-weight: bold;
        min-width: 80px;
    }
    .delete-btn {
        background: none;
        border: none;
        color: #e74c3c;
        font-size: 1.2rem;
        cursor: pointer;
    }
</style>