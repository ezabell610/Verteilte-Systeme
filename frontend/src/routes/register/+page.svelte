<script lang="ts">
    import { register } from '$lib/api';

    let username = $state('');
    let email = $state('');
    let password = $state('');
    let fehler = $state('');
    let erfolg = $state('');
    let loading = $state(false);

    async function handleRegister() {
        loading = true;
        fehler = '';
        try {
            await register(username, email, password);
            erfolg = 'Konto erstellt! Sie können sich jetzt einloggen.';
            fehler = '';
        } catch (e) {
            fehler = 'Registrierung fehlgeschlagen.';
        } finally {
            loading = false;
        }
    }
</script>

<main>
    <h1>Registrieren</h1>

    {#if fehler}
        <p class="fehler">{fehler}</p>
    {/if}
    {#if erfolg}
        <p class="erfolg">{erfolg}</p>
    {/if}

    <input type="text" placeholder="Benutzername" bind:value={username} />
    <input type="email" placeholder="E-Mail" bind:value={email} />
    <input type="password" placeholder="Passwort" bind:value={password} />
    <button onclick={handleRegister} disabled={loading}>
        {loading ? 'Wird geladen...' : 'Konto erstellen'}
    </button>

    <p>Schon ein Konto? <a href="/login">Einloggen</a></p>
</main>

<style>
    main {
        max-width: 400px;
        margin: 4rem auto;
        font-family: sans-serif;
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
    }
    input {
        padding: 0.6rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 6px;
    }
    button {
        padding: 0.6rem;
        font-size: 1rem;
        background: #04545b;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
    }
    .fehler { color: red; }
    .erfolg { color: #2a6c4b; }
</style>