<script>
	import { createEventDispatcher } from 'svelte';
	import { params_page, pagination_temp } from '$lib/store.js';
	import Button from './button.svelte';
	import Margin from '$lib/c_margin.svelte';

	let emit = createEventDispatcher();

	export let total_page = 1;

	const goto_page = async (p) => {
		if (p < 1) {
			p = 1;
		} else if (p > total_page) {
			p = total_page;
		}

		$params_page = p;
		$pagination_temp = p;

		emit('ok');
	};

	let width;
	let width2;
</script>

<Margin>
	<section>
		{#if $params_page > 1}
			<Button
				name="❮ prev"
				class="link"
				color="var(--font2)"
				on:click={() => {
					goto_page($params_page - 1);
				}}
			/>
		{/if}

		<div class="input">
			<span class="helper" bind:clientWidth={width}>
				{$params_page}
			</span>
			<input
				style:width="calc({width}px + {width2}px)"
				size="0"
				type="number"
				bind:value={$pagination_temp}
				on:keypress={(e) => {
					if (e.key == 'Enter') {
						goto_page($pagination_temp);
					}
				}}
			/>
			<div class="total" bind:clientWidth={width2}>
				of {total_page}
			</div>
		</div>

		{#if $pagination_temp != $params_page}
			<Button
				name="go ❯❯"
				class="link"
				color="var(--font2)"
				on:click={() => {
					goto_page($pagination_temp);
				}}
			/>
		{/if}

		{#if $params_page < total_page}
			<Button
				name="next ❯"
				class="link"
				color="var(--font2)"
				on:click={() => {
					goto_page(parseInt($params_page) + 1);
				}}
			/>
		{/if}
	</section>
</Margin>

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
