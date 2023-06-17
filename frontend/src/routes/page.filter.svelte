<script>
	import { page } from '$app/stores';
	import { createEventDispatcher, onMount } from 'svelte';

	import SVG from '$lib/svg.svelte';

	let emit = createEventDispatcher();

	export let filter = {};
	let keys = Object.keys(filter);
	let values = [];
	let fk;
	let fv;

	onMount(() => {
		if ($page.url.searchParams.has('fk1') && $page.url.searchParams.has('fv1')) {
			fk = $page.url.searchParams.get('fk1');
			fv = $page.url.searchParams.get('fv1');
			values = filter[fk];
		} else {
			$page.url.searchParams.delete('fk1');
			$page.url.searchParams.delete('fv1');
		}
	});

	const submit = () => {
		if (fk && fv && fk != 'select trait' && fv != 'select variation') {
			$page.url.searchParams.set('fk1', fk);
			$page.url.searchParams.set('fv1', fv);
			$page.url.searchParams.delete('page_no');
			window.history.pushState(history.state, '', $page.url.href);
			emit('ok');
		}
	};

	const reset = () => {
		fk = 'select trait';
		fv = 'select variation';
		values = [];
		$page.url.searchParams.delete('fk1');
		$page.url.searchParams.delete('fv1');
		$page.url.searchParams.delete('page_no');
		window.history.pushState(history.state, '', $page.url.href);
		emit('ok');
	};
</script>

<section>
	<div>
		<select
			bind:value={fk}
			on:change={() => {
				values = filter[fk];
				fv = 'select variation';
			}}
		>
			<option disabled selected hidden>select trait</option>
			{#each keys as x}
				<option value={x}>
					{x.replace(/_/g, ' ')}
				</option>
			{/each}
		</select>
		<select bind:value={fv}>
			<option disabled selected hidden>select variation</option>
			{#each values as x}
				<option value={x}>
					{x.replace(/_/g, ' ')}
				</option>
			{/each}
		</select>
	</div>

	<button
		on:click={() => {
			submit();
		}}
	>
		Filter
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
