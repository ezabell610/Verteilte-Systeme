<script lang="ts">
    import { isLoggedIn } from "$lib/api";

    const API_BASE = 'http://localhost:8000';

    let items = $state([]);
    let loading = $state(true);
    let loggedIn = $state(false);

    $effect(() => {
        loggedIn = isLoggedIn();
    });

    $effect(() => {
        if (!loggedIn) return;
        loadShoppingList();
    });

    async function loadShoppingList() {
        try {
            const token = localStorage.getItem('token');
            const res = await fetch(`${API_BASE}/shopping-list`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!res.ok) throw new Error();
            items = await res.json();
        } catch (e) {
            console.error('Fehler beim Laden');
        } finally {
            loading = false;
        }
    }

    async function toggleItem(id: number) {
        try {
            const token = localStorage.getItem('token');
            await fetch(`${API_BASE}/shopping-list/${id}`, {
                method: 'PUT',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            items = items.map((item: any) =>
                item.id === id ? { ...item, checked: !item.checked } : item
            );
        } catch (e) {
            console.error('Fehler beim Aktualisieren');
        }
    }

    async function removeItem(id: number) {
        try {
            const token = localStorage.getItem('token');
            await fetch(`${API_BASE}/shopping-list/${id}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            items = items.filter((item: any) => item.id !== id);
        } catch (e) {
            console.error('Fehler beim Löschen.');
        }
    }
       

    async function removeChecked() {
        const checkedItems = items.filter((item: any) => item.checked);
        for (const item of checkedItems) {
            await removeItem(item.id);
        }
    }
</script>

{#if !loggedIn}
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
            <ul class="liste">
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