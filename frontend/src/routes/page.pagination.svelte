<script>
	import { page } from '$app/stores';
	import { createEventDispatcher, onMount } from 'svelte';

	let emit = createEventDispatcher();
	let page_no, page_no_temp, width1, width2;
	export let total_page = 1;

	onMount(() => {
		reset();
		let params = $page.url.searchParams;
		if (params.has('page_no')) {
			let temp = normalise(params.get('page_no'));
			page_no = page_no_temp = temp;
			params.set('page_no', temp);
			window.history.pushState(history.state, '', $page.url.href);
		}
	});

	const normalise = (value) => {
		if (value < 1) {
			value = 1;
		} else if (value > total_page) {
			value = total_page;
		}
		return value;
	};

	const submit = (value) => {
		let temp = normalise(value);
		page_no_temp = page_no = temp;
		$page.url.searchParams.set('page_no', temp);
		window.history.pushState(history.state, '', $page.url.href);
		emit('ok');
	};

	export const reset = () => {
		page_no = page_no_temp = 1;
	};
</script>

<section>
	{#if page_no > 1}
		<button
			on:click={() => {
				submit(page_no - 1);
			}}
		>
			❮ prev
		</button>
	{/if}

	<div class="input">
		<input
			style:width="calc({width1}px + {width2}px)"
			type="number"
			bind:value={page_no_temp}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					submit(page_no_temp);
				}
			}}
		/>
		<span class="helper" bind:clientWidth={width1}>
			{#if page_no_temp}
				{page_no_temp}
			{/if}
		</span>
		<div class="total" bind:clientWidth={width2}>
			/ {total_page}
		</div>
	</div>

	{#if page_no_temp != page_no}
		<button
			on:click={() => {
				submit(page_no_temp);
			}}
		>
			go ❯❯
		</button>
	{/if}

	{#if page_no < total_page}
		<button
			on:click={() => {
				submit(parseInt(page_no) + 1);
			}}
		>
			next ❯
		</button>
	{/if}
</section>

<style>
	section {
		display: flex;
		justify-content: center;
		gap: var(--sp1);

		margin: var(--sp2);
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
	}

	.helper {
		position: absolute;
		visibility: hidden;

		padding: calc(var(--sp1) + 5px);
	}
	.total {
		position: absolute;
		right: calc(var(--sp1) + 4px);
		pointer-events: none;
	}
</style>
