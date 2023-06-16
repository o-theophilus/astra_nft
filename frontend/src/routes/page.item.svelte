<script>
	import { module } from '$lib/store.js';
	export let meta;

	let url = import.meta.env.VITE_BACKEND;
</script>

<section
	on:keypress
	on:click={() => {
		$module = meta;
	}}
>
	<img src="{url}/photo/{meta.id}/thumbnail" alt={meta.id} />
	Astra <b>#{meta.id}</b>
</section>

<style>
	section {
		padding: var(--gap2);
		border-radius: var(--br1);

		background-color: var(--ac4);
		cursor: pointer;
		transition: var(--trans1);
	}

	section:hover {
		transform: scale(1.02);
	}

	img {
		border-radius: var(--br1);
		width: 100%;
	}
</style>
