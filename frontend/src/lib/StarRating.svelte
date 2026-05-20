<script lang="ts">
    let { rating = 0, onRate = null }: { rating: number, onRate: ((stars: number) => void) | null} = $props();
    let hovered = $state(0);
</script>

<div class="sterne">
    {#each [1, 2, 3, 4, 5] as star}
        <span
            class="stern"
            class:aktiv={star <= (hovered || rating)}
            class:klickbar={onRate !== null}
            onmouseenter={() => { if (onRate) hovered = star }}
            onmouseleave={() => hovered = 0}
            onclick={() => {if (onRate) onRate(star) }}
        >
            ★
        </span>
    {/each}
</div>

<style>
    .sterne {
        display: inline-flex;
        gap: 2px;
    }
    .stern {
        font-size: 1.5rem;
        color: #ddd;
        transition: color 0.15s;
    }
    .stern.aktiv {
        color: #f5a623;
    }
    .stern.klickbar {
        cursor: pointer;
    }
    .stern.klickbar:hover {
        transform: scale(1.2);
    }
</style>