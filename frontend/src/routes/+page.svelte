<script lang="ts">
    import { isLoggedIn } from "$lib/api";

	//Probe-Daten bis Isabells Backend fertig ist --> Das dann ändern! zwecks todos
	let recipes = [
		{
			id: 1,
			title: 'Spaghetti Bolognese',
			description: 'Klassisches italienisches Nudelgericht',
			category: 'Italienisch',
			stars: 4,
			is_public: true
		},
		{
			id: 2,
			title: 'Vegane Bowl',
			description: 'Gesunde Bowl mit Quinoa und Avocado',
			category: 'Vegan',
			stars: 5,
			is_public: true
		},
		{
			id: 3,
			title: 'Apfelkuchen',
			description: 'Leckerer Kuchen mit frischen Äpfeln',
			category: 'Desserts',
			stars: 4,
			is_public: false
		},
		{
			id: 4,
			title: 'Gebratener Reis',
			description: 'Schnelles asiatisches Reisgericht',
			category: 'Asiatisch',
			stars: 3,
			is_public: true
		},
		{
			id: 5,
			title: 'Tomatensuppe',
			description: 'Leckere Suppe für schnelle Küche',
			category: 'Schnelle Küche',
			stars: 4,
			is_public: false
		}
	];

	const kategorien = ['Alle', 'Vegan', 'Italienisch', 'Desserts', 'Asiatisch', 'Schnelle Küche'];

	let selectedKategorie = $state('Alle');
	let searchText = $state('');

	let filteredRecipes = $derived(recipes.filter (r => {
		const matchesKategorie = selectedKategorie === 'Alle' || r.category === selectedKategorie;
		const matchesSearch = r.title.toLowerCase().includes(searchText.toLowerCase());
		const matchesAuth = isLoggedIn() || r.is_public;
		return matchesKategorie && matchesSearch && matchesAuth;
	}));
	// TODO: Importiert und nutzt die Funktionen aus $lib/api
	// import { login, logout, isLoggedIn, fetchProtected } from '$lib/api';

	// TODO: Definiert eure Variablen (z. B. State für eingeloggt, Fehlermeldungen, Daten)

	// TODO: Implementiert eure Event-Handler-Funktionen
</script>

<main>
	<div class="header">
		<h1>Rezepte</h1>
		{#if isLoggedIn()}
			<a href="/recipes/new" class="erstellen-btn">+ Rezept erstellen</a>
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
				class:aktiv={selectedKategorie === kat}
				onclick={() => selectedKategorie = kat}
			>
				{kat}
			</button>
		{/each}
	</div>

	<!--Rezepte-->
	<div class="karten">
		{#each filteredRecipes as recipe}
			<a href="/recipes/{recipe.id}" class="karte">
				<h2>{recipe.title}</h2>
				<p class="kategorie">{recipe.category}</p>
				<p>{recipe.description}</p>
				<p class="sterne">{'★'.repeat(recipe.stars)}</p>
			</a>
		{:else}
			<p>Keine Rezepte gefunden.</p>
		{/each}
	</div>
	<!-- TODO: Baut hier eure Oberfläche auf -->
	<!-- Tipp: Nutzt {#if loggedIn} ... {:else} ... {/if} für konditionelle Anzeige -->
	
</main>

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
		border: 1px solid #ddd;
		border-radius: 10px;
		padding: 1.2rem;
		text-decoration: none;
		color: black;
		box-shadow: 0 2px 6px rgba(0,0, 0, 0.08);
		transition: box-shadow 0.2s;
	}
	.karte:hover {
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}
	.karte h2 {
		margin: 0 0 0.3rem 0;
		font-size: 1.1rem;
		color: #04545b;
	}
	.kategorie {
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
</style>
