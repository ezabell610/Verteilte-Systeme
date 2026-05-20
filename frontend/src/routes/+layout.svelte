<script lang="ts">
    import { isLoggedIn, logout } from '$lib/api';

    function handleLogout() {
        logout();
        window.location.href = '/login';
    }
</script>

<nav>
    <a href="/">🍳 Kochbuch</a>

    <div class="links">
        <a href="/">Rezepte</a>
        {#if isLoggedIn()}
            <a href="/recipes/neu">Rezept erstellen</a>
            <a href="/shopping-list">Einkaufsliste</a>
            <button onclick={handleLogout}>Logout</button>
        {:else}
            <a href="/login">Login</a>
            <a href="/register">Registrieren</a>
        {/if}
    </div>
</nav>

<slot />

<style>
    nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: #068691;
        color: white;
        font-family: sans-serif;
    }
    nav a {
        color: white;
        text-decoration: none;
        font-weight: bold;
    }
    .links {
        display: flex;
        gap: 1.5rem;
        align-items: center;
    }
    .links a {
        font-weight: normal;
    }
    button {
        background: white;
        color: #068691;
        border: none;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
    }
</style>