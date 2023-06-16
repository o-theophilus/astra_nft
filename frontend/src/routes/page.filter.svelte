<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import { fk1, fv1, filter } from '$lib/store.js';

	let emit = createEventDispatcher();

	let keys = Object.keys($filter);
	let values = [];
	let fk;
	let fv;

	const submit = () => {
		if (fk && fv && fk != 'select trait' && fv != 'select variation') {
			$fk1 = fk;
			$fv1 = fv;
			emit('ok');
		}
	};

	const reset = () => {
		fk = 'select trait';
		fv = 'select variation';
		$fk1 = '';
		$fv1 = '';
		values = [];
		emit('ok');
	};

	onMount(() => {
		if ($fk1 && $fv1) {
			fk = $fk1;
			fv = $fv1;
			values = $filter[fk];
		}
	});
</script>

<section>
	<select
		bind:value={fk}
		on:change={() => {
			values = $filter[fk];
			fv = 'select variation';
		}}
	>
		<option disabled selected hidden>select trait</option>
		{#each keys as x}
			<option value={x}>
				{x}
			</option>
		{/each}
	</select>
	<select bind:value={fv}>
		<option disabled selected hidden>select variation</option>
		{#each values as x}
			<option value={x}>
				{x}
			</option>
		{/each}
	</select>

	<button
		on:click={() => {
			submit();
		}}
	>
		filter
	</button>
	<button
		on:click={() => {
			reset();
		}}
	>
		x
	</button>
</section>

<style>
	section {
		display: flex;
		justify-content: end;
		align-items: center;
		flex-wrap: wrap;
		gap: var(--sp1);

		margin: var(--sp2);
	}

	option {
		text-transform: capitalize;
	}
</style>
