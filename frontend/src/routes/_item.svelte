<script>
	import { backend, module } from '$lib/store.js';
	export let meta;
</script>

<section
	on:click={() => {
		$module = meta;
	}}
>
	<img src="{backend}/photo/{meta.id}/thumbnail" alt={meta.id} />
	<div class="details">
		id: <b>{meta.id}</b>
	</div>
</section>

<style>
	section,
	.details {
		display: flex;
	}

	section {
		gap: var(--gap2);
		background-color: var(--background);
		border-radius: var(--brad1);

		padding: var(--gap2);
		transition: var(--trans1);

		cursor: pointer;
	}

	section:hover {
		transform: scale(1.02);
		border-color: var(--color1);
	}

	img {
		border-radius: var(--brad1);
		width: 100%;
	}

	.details {
		gap: var(--gap1);
		justify-content: center;
		align-items: center;
	}

	section {
		flex-direction: column;
	}
</style>
