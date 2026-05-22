<script lang="ts">
    import { login } from '$lib/api';
    
    let username = $state('');
    let password = $state('');
    let fehler = $state('');
    let loading = $state(false);

    async function handleLogin() {
        loading = true;
        fehler = '';
        try {
            await login(username, password);
            window.location.href = '/';
        } catch (e) {
            fehler = 'Benutzername oder Passwort falsch';
        } finally {
            loading = false;
        }
    }
</script>

<main>
    <h1>Login</h1>

    {#if fehler}
        <p class="fehler">{fehler}</p>
    {/if}

    <input type="text" placeholder="Benutzername" bind:value={username} />
    <input type="password" placeholder="Passwort" bind:value={password} />
    <button onclick={handleLogin} disabled={loading}>
        {loading ? 'Wird geladen...' : 'Einloggen'}
    </button>

    <p>Sie haben noch kein Konto? <a href="/register">Registrieren</a></p>
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
    .fehler {
        color: red;
    }
</style>
