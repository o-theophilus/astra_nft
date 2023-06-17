<script>
	import { page } from '$app/stores';

	import Item from './page.item.svelte';
	import Pagination from './page.pagination.svelte';
	import Filter from './page.filter.svelte';

	export let data;
	let { metas } = data;
	let { total_page } = data;
	let { filter } = data;
	let pagination;

	const submit = async () => {
		let resp = await fetch(`${import.meta.env.VITE_BACKEND}/nft${$page.url.search}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		resp = await resp.json();
		metas = resp.metas;
		total_page = resp.total_page;

		window.scrollTo({ top: 0, behavior: 'smooth' });
	};
</script>

<Filter
	{filter}
	on:ok={() => {
		pagination.reset();
		submit();
	}}
/>

<div class="page">
	{#each metas as meta}
		<Item {meta} />
	{/each}
</div>

<Pagination
	{total_page}
	bind:this={pagination}
	on:ok={() => {
		submit();
	}}
/>

<style>
	.page {
		margin: var(--sp2);
		display: grid;

		grid-template-columns: 1fr;
		gap: var(--sp1);
	}

	@media screen and (min-width: 400px) {
		.page {
			grid-template-columns: repeat(2, 1fr);
		}
	}
	@media screen and (min-width: 800px) {
		.page {
			grid-template-columns: repeat(3, 1fr);
		}
	}
	@media screen and (min-width: 1000px) {
		.page {
			grid-template-columns: repeat(4, 1fr);
		}
	}
	@media screen and (min-width: 1400px) {
		.page {
			grid-template-columns: repeat(5, 1fr);
		}
	}
	@media screen and (min-width: 1600px) {
		.page {
			grid-template-columns: repeat(6, 1fr);
		}
	}
	@media screen and (min-width: 1800px) {
		.page {
			grid-template-columns: repeat(7, 1fr);
		}
	}
</style>
