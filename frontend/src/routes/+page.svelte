<script lang="ts">
	import StarRating from "$lib/StarRating.svelte";
    import { isLoggedIn } from "$lib/api";

	const API_BASE = 'http://localhost:8000';

	let recipes = $state([]);
	let kategorien = $state([{ id: 0, name: 'Alle' }]);
	let selectedKategorie = $state(0);
	let searchText = $state('');
	let loading = $state(true);

	async function loadKategorien() {
		try {
			const res = await fetch (`${API_BASE}/categories`);
			const data = await res.json();
			kategorien = [{ id: 0, name: 'Alle' }, ...data];
		} catch (e) {
			console.error ('Kategorien laden fehlgeschlagen');
		}	
	}

	async function loadRecipes() {
		loading = true;
		try {
			let url = `${API_BASE}/recipes?`;
			if (searchText) url += `search=${searchText}&`;
			if (selectedKategorie) url += `category_id=${selectedKategorie}`;
			const res = await fetch(url);
			let data = await res.json();

			// Eigene Private Rezepte hinzufügen wenn eingeloggt
			if (isLoggedIn()) {
				const token = localStorage.getItem('token');
				const myRes = await fetch(`${API_BASE}/my-recipes`, {
					headers: { 'Authorization': `Bearer ${token}` }
				});
				const myRecipes = await myRes.json();
				const privateOwn = myRecipes.filter((r: any) => !r.is_public);

				const existingIds = new Set(data.map((r: any) => r.id));
				for (const r of privateOwn) {
					if (!existingIds.has(r.id)) data.push(r);
				}
			}
			recipes = data;
		} catch (e) {
			console.error('Rezepte laden fehlgeschlagen');
		} finally {
			loading = false;
		}
	}

	$effect(() => {
		loadKategorien();
		loadRecipes();
	});

	$effect(() => {
		selectedKategorie;
		searchText;
		loadRecipes();
	});
	
	function scrollToContent () {
		document.getElementById('content')?.scrollIntoView({ behavior: 'smooth' });
	}

	function getCategoryName(id: number): string {
		const kat = kategorien.find((k: any) => k.id === id);
		return kat ? kat.name: 'Unbekannt';
	}
	// TODO: Importiert und nutzt die Funktionen aus $lib/api
	// import { login, logout, isLoggedIn, fetchProtected } from '$lib/api';

	// TODO: Definiert eure Variablen (z. B. State für eingeloggt, Fehlermeldungen, Daten)

	// TODO: Implementiert eure Event-Handler-Funktionen
</script>

<section class="splash">
	<div class="splash-inner">
		<div class="logo-kreis">🥘</div>
		<h1 class="splash-titel">ESI's Kitchen</h1>
		<p class="splash-sub">Entdecke, erstelle und teile deine Lieblingsrezepte</p>
		<button class="scroll-btn" onclick={scrollToContent}>
			V
		</button>
	</div>
</section>

<div id="content">

	<main>
		<div class="header">
			<h1>Rezepte</h1>
			{#if isLoggedIn()}
				<a href="/recipes/neu" class="erstellen-btn">+ Rezept erstellen</a>
				{/if}
		</div>
		<!--Suchleiste-->
		<input
			type="text"
			placeholder="Rezept suchen..."
			bind:value={searchText}
		/>

		<!--Kategorien Filter-->
		<div class="kategorien">
			{#each kategorien as kat}
				<button
					class:aktiv={selectedKategorie === kat.id}
					onclick={() => selectedKategorie = kat.id}
				>
					{kat.name}
				</button>
			{/each}
		</div>

		<!--Rezepte-->
		{#if loading}
			<p class="laden">Rezepte werden geladen...</p>
		{:else}
			<div class="karten">
				{#each recipes as recipe}
					<a href="/recipes/{recipe.id}" class="karte">
						<h2>{recipe.title}</h2>
						<p class="kategorie-badge">{getCategoryName(recipe.category_id)}</p>
						<p>{recipe.description}</p>
						<StarRating rating={recipe.average_rating} />
					</a>
			{:else}
				<p>Keine Rezepte gefunden.</p>
			{/each}
		</div>
	{/if}
		<!-- TODO: Baut hier eure Oberfläche auf -->
		<!-- Tipp: Nutzt {#if loggedIn} ... {:else} ... {/if} für konditionelle Anzeige -->
		
	</main>
</div>

<style>
	main {
		max-width: 900px;
		margin: 2rem auto;
		padding: 0.1rem;
		font-family: sans-serif;
	}
	input {
		width: 100%;
		padding: 0.6rem;
		font-size: 1rem;
		border: 1px solid #ccc;
		border-radius: 6px;
		margin-bottom: 1rem;
		box-sizing: border-box;
	}
	.header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-bottom: 1.5rem;
	}
	.erstellen-btn {
		background: #04545b;
		color: white;
		padding: 0.5rem 1.2rem;
		border-radius: 20px;
		text-decoration: none;
		font-size: 0.95rem;
		font-weight: 500;
		letter-spacing: 0.3px;
		box-shadow: 0 2px 8px rgba(4, 84, 91, 0.3);
		transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
	}
	.erstellen-btn:hover {
		background-color: #033d43;
		transform: scale(1.03);
		box-shadow: 0 4px 14px rgba(4, 84, 91, 0.4);
	}
	input {
		width: 100%;
		padding: 0.75rem 1rem;
		font-size: 1rem;
		border: 1px #e0e0e0;
		border-radius: 12px;
		margin-bottom: 1rem;
		box-sizing: border-box;
		background: #f9f9f9;
		outline: none;
		transition: border 0.2s, box-shadow 0.2s;
	}
	input:focus {
		border-color: #04545b;
		background: white;
		box-shadow: 0 0 0 3px rgba(4, 84, 91, 0.1);
	}
	.kategorien {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		margin-bottom: 1.5rem;
	}
	.kategorien button {
		padding: 0.4rem 1rem;
		border: 2px solid #04545b;
		background: white;
		color: #04545b;
		border-radius: 20px;
		cursor: pointer;
		font-family: sans-serif;
	}
	.kategorien button.aktiv {
		background: #04545b;
		color: white;
	}
	.karten {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
		gap: 1.5rem;
	}
	.karte {
		background: white;
		border: 1px solid #e0e0e0;
		border-radius: 12px;
		padding: 1.2rem;
		text-decoration: none;
		color: black;
		box-shadow: 0 2px 8px rgba(0,0, 0, 0.06);
		transition: transform 0.2s, box-shadow 0.2s;
	}
	.karte:hover {
		transform: translateY(-3px);
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
	}
	.karte h2 {
		margin: 0 0 0.3rem 0;
		font-size: 1.1rem;
		color: #04545b;
	}
	.kategorie-badge {
		font-size: 0.8rem;
		color: white;
		background: #04545b;
		display: inline-block;
		padding: 0.2rem 0.6rem;
		border-radius: 10px;
		margin-bottom: 0.5rem;
	}
	.sterne {
		margin-top: 0.5rem;
	}
	.laden {
		text-align: center;
		color: #888;
		margin-top: 2rem;
	}
	.splash {
		height: 100vh;
		display: flex;
		align-items: center;
		justify-content: center;
		background: linear-gradient(135deg, #04545b 0%, #068691 50%, #0aa8b5 100%);
		text-align: center;
	}
	.splash-inner {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
		color: white;
	}
	.logo-kreis {
		font-size: 5rem;
		background: rgba(255,255,255, 0.15);
		border-radius: 50%;
		width: 120px;
		height: 120px;
		display: flex;
		align-items: center;
		justify-content: center;
		backdrop-filter: blur(10px);
		border: 2px solid rgba(255,255,255,0.3);
		animation: float 3s ease-in-out infinite;
	}
	@keyframes float {
		0%, 100% { transform: translateY(0px); }
		50% { transform: translateY(-10px); }
	}
	.splash-titel {
		font-size: 3.5rem;
		font-weight: bold;
		margin: 0;
		text-shadow: 0 2px 10px rgba(0,0,0, 0.2);
		letter-spacing: 2px;
	}
	.splash-sub {
		font-size: 1.1rem;
		opacity: 0.85;
		margin: 0;
		max-width: 400px;
	}
	.scroll-btn {
		background: rgba(255, 255, 255, 0.2);
		border: 2px solid rgba(255,255, 255,0.5);
		color: white;
		font-size: 1.8rem;
		width: 55px;
		height: 55px;
		border-radius: 50%;
		cursor: pointer;
		margin-top: 1rem;
		transition: background 0.3s, transform 0.3s;
		animation: bounce 2s ease-in-out infinite;
	}
	.scroll-btn:hover {
		background: rgba(255, 255, 255, 0.35);
		transform: scale(1.1);
	}
	@keyframes bounce {
		0%, 100% { transform: translateY(0); }
		50% { transform: translateY(8px); }
	}
</style>
