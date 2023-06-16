<script>
	import { createEventDispatcher } from 'svelte';
	import { page_no, page_no_temp, total_page } from '$lib/store.js';

	let emit = createEventDispatcher();

	const goto_page = async (p) => {
		if (p < 1) {
			p = 1;
		} else if (p > $total_page) {
			p = $total_page;
		}

		$page_no_temp = p;
		$page_no = p;

		emit('ok');
	};

	let width1;
	let width2;

	let test;
</script>

<section>
	{#if $page_no > 1}
		<button
			on:click={() => {
				goto_page($page_no - 1);
			}}
		>
			❮ prev
		</button>
	{/if}

	<div class="input">
		<!-- size="0" -->
		<input
			style:width="calc({width1}px + {width2}px)"
			type="number"
			bind:value={$page_no_temp}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					goto_page($page_no_temp);
				}
			}}
		/>
		<span class="helper" bind:clientWidth={width1}>
			{#if $page_no_temp}
				{$page_no_temp}
			{/if}
		</span>
		<div class="total" bind:clientWidth={width2}>
			/ {$total_page}
		</div>
	</div>

	{#if $page_no_temp != $page_no}
		<button
			on:click={() => {
				goto_page($page_no_temp);
			}}
		>
			go ❯❯
		</button>
	{/if}

	{#if $page_no < $total_page}
		<button
			on:click={() => {
				goto_page(parseInt($page_no) + 1);
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

		padding: var(--sp2);
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
