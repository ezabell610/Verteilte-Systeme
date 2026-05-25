<script lang="ts">
    let { children } = $props();
    import { isLoggedIn, logout } from '$lib/api';

    let menuOpen = $state(false);

    function handleLogout() {
        logout();
        window.location.href = '/login';
    }
</script>

<nav>
    <a href="/" class="logo">🍳 Kochbuch</a>

    <button class="hamburger" onclick={() => menuOpen = !menuOpen}>
        {menuOpen ? 'x' : '=='}
    </button>

    <div class="links" class:open={menuOpen}>
        <a href="/" onclick={() => menuOpen = false}>Rezepte</a>
        {#if isLoggedIn()}
            <a href="/recipes/neu" onclick={() => menuOpen = false}>Rezept erstellen</a>
            <a href="/my-recipes" onclick={() => menuOpen = false}>Meine Rezepte</a>
            <a href="/shopping-list" onclick={() => menuOpen = false}>Einkaufsliste</a>
            <button class="logout-btn" onclick={handleLogout}>Logout</button>
        {:else}
            <a href="/login" onclick={() => menuOpen = false}>Login</a>
            <a href="/register" onclick={() => menuOpen = false}>Registrieren</a>
        {/if}
    </div>
</nav>

{@render children()}

<style>
    nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: #04545b;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }
    .logo {
        color: white;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .hamburger {
        display: none;
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
    }
    .links {
        display: flex;
        gap: 1.5rem;
        align-items: center;
    }
    .links a {
        color: white;
        text-decoration: none;
        font-size: 0.95rem;
        transition: opacity 0.2s;
    }
    .links a:hover {
        opacity: 0.8;
    }
    .logout-btn {
        background: white;
        color: #04545b;
        border: none;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        cursor: pointer;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
    }

    @media (max-width: 768px) {
        .hamburger {
            display: block;
        }
        .links {
            display: none;
            flex-direction: column;
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: #04545b;
            padding: 1rem 2rem;
            gap: 1rem;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
        }
        .links.open {
            display: flex;
        }
    }
</style>