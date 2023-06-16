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
		<span class="helper" bind:clientWidth={width1}>
			{$page_no}
		</span>
		<input
			style:width="calc({width1}px + {width2}px)"
			size="0"
			type="number"
			bind:value={$page_no_temp}
			on:keypress={(e) => {
				if (e.key == 'Enter') {
					goto_page($page_no_temp);
				}
			}}
		/>
		<div class="total" bind:clientWidth={width2}>
			of {$total_page}
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

		border-radius: var(--br1);
		border: 2px solid var(--ac5);

		color: var(--ac1);
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
