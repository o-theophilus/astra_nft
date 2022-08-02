<script>
	import { createEventDispatcher, onMount } from 'svelte';
	import { page } from '$app/stores';
	import Button from './button.svelte';

	let emit = createEventDispatcher();

	export let total_page = 1;
	let value = 1;
	let _value = 1;

	const goto_page = async (p) => {
		if (p < 1) {
			p = 1;
		} else if (p > total_page) {
			p = total_page;
		}

		value = p;
		_value = p;
		window.history.pushState('', '', `/?page=${value}`);
		emit('ok', value);
	};

	onMount(() => {
		if ($page.url.searchParams.has('page')) {
			let init = parseInt($page.url.searchParams.get('page'));
			value = init;
			_value = init;
		}
	});

	let width;
	let width2;
</script>

<section>
	{#if value > 1}
		<Button
			name="❮ prev"
			class="link"
			color="var(--font2)"
			on:click={() => {
				goto_page(value - 1);
			}}
		/>
	{/if}

	<div class="input">
		<span class="helper" bind:clientWidth={width}>
			{value}
		</span>
		<input
			style:width="calc({width}px + {width2}px)"
			size="0"
			type="number"
			bind:value={_value}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					goto_page(_value);
				}
			}}
		/>
		<div class="total" bind:clientWidth={width2}>
			of {total_page}
		</div>
	</div>

	{#if _value != value}
		<Button
			name="go ❯❯"
			class="link"
			color="var(--font2)"
			on:click={() => {
				goto_page(_value);
			}}
		/>
	{/if}

	{#if value < total_page}
		<Button
			name="next ❯"
			class="link"
			color="var(--font2)"
			on:click={() => {
				goto_page(value + 1);
			}}
		/>
	{/if}
</section>

<style>
	section {
		display: flex;
		justify-content: center;
		gap: var(--gap1);
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
	}

	input {
		padding: var(--gap1);

		background: transparent;
		font-weight: 500;
		margin-right: 2px;

		border-radius: var(--brad1);
		border: 2px solid var(--background);

		color: var(--font1);
	}

	input:hover {
		border-color: var(--midtone);
	}
	input:focus {
		border-color: var(--color1);
	}
	.total {
		position: absolute;
		right: calc(var(--gap1) + 4px);
		pointer-events: none;
		font-size: small;
	}

	.helper {
		position: absolute;
		visibility: hidden;

		padding: calc(var(--gap1) + 4px);
	}
</style>
