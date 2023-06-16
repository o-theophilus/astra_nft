<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { module, nft_count } from '$lib/store.js';
	import SVG from '$lib/svg.svelte';
</script>

{#if $module}
	<section
		on:keypress
		on:click|self={() => {
			$module = '';
		}}
	>
		<div class="content" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<button
				on:keypress
				on:click={() => {
					$module = '';
				}}
			>
				<SVG type="close" size="12" />
			</button>
			<img src="{import.meta.env.VITE_BACKEND}/photo/{$module.id}" alt={$module.id} />
			<br />
			<span>Astra: <b>#{$module.id}</b></span>
			<span>rarity rank: <b>{$module.rarity} / {$nft_count.male + $nft_count.female}</b></span>
			<br />

			<b>Traits</b>
			<span>gender: <b>{$module.gender}</b></span>
			<span>skin tone: <b>{$module.skin_tone}</b></span>
			<span>attire: <b>{$module.attire}</b></span>
			<span>accessory: <b>{$module.accessory}</b></span>
			<span>headgear: <b>{$module.headgear}</b></span>
			<span>hairstyle: <b>{$module.hairstyle}</b></span>
			<span>back accessory: <b>{$module.back_accessory}</b></span>
			<span>frame: <b>{$module.frame}</b></span>
			<span>background: <b>{$module.background}</b></span>
		</div>
	</section>
{/if}

<style>
	button {
		--size: 40px;

		position: absolute;
		top: -10px;
		right: -10px;

		display: flex;
		justify-content: center;
		align-items: center;

		border: none;
		border-radius: 50%;
		width: var(--size);
		height: var(--size);

		background-color: var(--ac3);
		cursor: pointer;
	}

	button:hover {
		fill: var(--ac5_);
		background-color: var(--cl4);
	}

	section {
		display: flex;

		position: fixed;
		inset: 0;
		top: var(--headerHeight);
		height: (100vh - var(--headerHeight));
		z-index: 1;

		padding: var(--sp3);

		overflow-y: auto;
		background-color: var(--overlay);
	}

	.content {
		display: flex;
		flex-direction: column;

		position: relative;

		width: 100%;
		max-width: 500px;
		padding: var(--sp2);
		border-radius: var(--br1);
		margin: auto;

		background-color: var(--ac4);
		box-shadow: var(--shad1);

		font-size: small;
		align-items: center;
		text-transform: capitalize;
	}

	img {
		border-radius: var(--br1);
		width: 100%;
		aspect-ratio: 1/1;

		background-image: url('/image/loading.png');
		background-size: cover;
	}
</style>
