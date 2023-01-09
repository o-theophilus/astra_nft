<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import Button from './button.svelte';
	import { params_filter } from '$lib/store.js';
	import Margin from '$lib/c_margin.svelte';

	let emit = createEventDispatcher();

	export let filter;

	let keys = [];
	let values = [];
	for (let x in filter) {
		keys.push(x);
	}

	let fk;
	let fv;

	const submit = () => {
		if (fk && fv && fk != 'select trait' && fv != 'select variation') {
			$params_filter = `${fk}700${fv}`;
			emit('ok');
		}
	};
	const reset = () => {
		fk = '';
		fv = '';
		$params_filter = '';
		values = [];
		emit('ok');
	};

	onMount(() => {
		if ($params_filter) {
			var init = $params_filter.split('700');
			fk = init[0];
			values = filter[fk];
			fv = init[1];
		}
	});
</script>

<Margin>
	<section>
		Trait:
		<select
			bind:value={fk}
			on:change={() => {
				values = filter[fk];
				fv = undefined;
			}}
		>
			<option disabled selected hidden>select trait</option>
			{#each keys as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>

		Variation:
		<select bind:value={fv}>
			<option disabled selected hidden>select variation</option>
			{#each values as x}
				<option value={x}>
					{x}
				</option>
			{/each}
		</select>

		<Button
			name="filter"
			color="var(--font2)"
			class="tiny"
			on:click={() => {
				submit();
			}}
		/>
		<Button
			name="reset"
			color="var(--font2)"
			class="tiny"
			on:click={() => {
				reset();
			}}
		/>
	</section>
</Margin>

<style>
	section {
		display: flex;
		justify-content: center;
		align-items: center;
		flex-wrap: wrap;
		gap: var(--gap1);
	}

	option{
		text-transform: capitalize;
	}
</style>
