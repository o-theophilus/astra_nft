<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import { fk1, fv1, filter } from '$lib/store.js';

	import SVG from '$lib/svg.svelte';

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
	<div>
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
					{x.replace(/_/g, " ")}
				</option>
			{/each}
		</select>
		<select bind:value={fv}>
			<option disabled selected hidden>select variation</option>
			{#each values as x}
				<option value={x}>
					{x.replace(/_/g, " ")}
				</option>
			{/each}
		</select>
	</div>

	<button
		on:click={() => {
			submit();
		}}
	>
		filter
	</button>
	<button
		class="clear"
		on:click={() => {
			reset();
		}}
	>
		<SVG type="close" size="8" />
	</button>
</section>

<style>
	section {
		display: flex;
		justify-content: end;
		align-items: center;
		flex-wrap: wrap;
		gap: var(--sp1);

		max-width: var(--headerWidth);
		margin: var(--sp2) auto;
		padding: 0 var(--sp2);
	}

	select,
	option {
		text-transform: capitalize;
	}

	.clear {
		--size: 30px;

		display: flex;
		justify-content: center;
		align-items: center;

		width: var(--size);
		height: var(--size);
		border-radius: 50%;

		fill: var(--ac2);
	}
	.clear:hover {
		fill: var(--ac5_);
		background-color: var(--cl4);
	}
</style>
