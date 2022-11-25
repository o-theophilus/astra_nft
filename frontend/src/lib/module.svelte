<script>
	import { scale } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { module, backend, count } from '$lib/store.js';
	import Button from './button.svelte';
</script>

{#if $module}
	<section
		on:click|self={() => {
			$module = '';
		}}
	>
		<div class="block" transition:scale|local={{ delay: 0, duration: 200, easing: backInOut }}>
			<div
				class="close"
				on:click={() => {
					$module = '';
				}}
			>
				<Button
					icon="close"
					icon_size="12"
					class="hover_red"
					on:click={() => {
						$module = '';
					}}
				/>
			</div>
			<div class="content">
				<img src="{backend}/photo/{$module.id}" alt={$module.id} />
				<div class="details">
					<span>id: <b>{$module.id}</b></span>
					<span>rarity rank: <b>{$module.rarity} / {$count.male + $count.female}</b></span>
					<br />

					<b>Traits</b>
					<span>gender: <b>{$module.gender}</b></span>
					<span>skin tone: <b>{$module.skin_tone}</b></span>
					<span>attire: <b>{$module.attire}</b></span>
					<span>accessory: <b>{$module.accessory}</b></span>
					<span>headgear: <b>{$module.headgear}</b></span>
					<span>hairstyle: <b>{$module.hairstyle}</b></span>
					<span>back accessory: <b>{$module.back_accessory}</b></span>
					<span>background: <b>{$module.background}</b></span>
				</div>
			</div>
		</div>
	</section>
{/if}

<style>
	section {
		display: grid;
		align-items: center;
		justify-content: center;

		position: fixed;
		inset: 0;
		top: var(--headerHeight);
		z-index: 1;

		padding: var(--gap3);
		overflow-y: auto;

		background-color: var(--overlay);
	}

	.block {
		position: relative;
	}

	.close {
		position: absolute;
		top: -10px;
		right: -10px;
	}

	.content,
	.details {
		flex-direction: column;
		display: flex;
	}

	.content {
		gap: var(--gap2);

		width: 100%;
		padding: var(--gap2);
		border-radius: var(--brad1);
		overflow: hidden;

		background-color: var(--foreground);
		box-shadow: var(--shad1);

		transition: var(--trans1);
	}

	img {
		border-radius: var(--brad1);
		max-width: 500px;
		width: 100%;
	}

	.details {
		font-size: small;
		align-items: center;

		text-transform: capitalize;
	}
</style>
