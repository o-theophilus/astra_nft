<script context="module">
	import { backend } from '$lib/store.js';

	import Item from './_item.svelte';
	import Pagination from '$lib/pagination.svelte';

	export async function load({ fetch, url }) {
		let page = 1;
		if (url.searchParams.has('page')) {
			page = url.searchParams.get('page');
		}

		const _resp = await fetch(`${backend}/nft?page=${page}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			return {
				props: {
					metas: resp.data.metas,
					total_page: resp.data.total_page
				}
			};
		}
	}
</script>

<script>
	export let metas;
	export let total_page;

	const submit = async (page) => {
		const _resp = await fetch(`${backend}/nft?page=${page}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();
			metas = resp.data.metas;
			window.scrollTo({ top: 0, behavior: 'smooth' });
		}
	};
</script>

<div class="page">
	{#each metas as meta}
		<Item {meta} />
	{/each}
</div>

<div class="pagination">
	<Pagination
		{total_page}
		on:ok={(e) => {
			submit(e.detail);
		}}
	/>
</div>

<style>
	.page {
		display: grid;

		grid-template-columns: 1fr;
		gap: var(--gap2);
		padding: var(--gap2);
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
			grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr 1fr;
		}
	}

	.pagination {
		padding: var(--gap2);
	}
</style>
