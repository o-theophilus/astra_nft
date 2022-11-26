<script context="module">
	import { backend, count, params_page, pagination_temp, params_filter } from '$lib/store.js';

	import Item from './_item.svelte';
	import Pagination from '$lib/pagination.svelte';
	import Filter from '$lib/filter.svelte';
	import Margin from '$lib/c_margin.svelte';

	export async function load({ fetch, url }) {
		let params = '';
		if (url.searchParams.has('page')) {
			let page = url.searchParams.get('page');
			params_page.set(page);
			pagination_temp.set(page);
			params = `page=${page}`;
		}
		if (url.searchParams.has('filter')) {
			let filter = url.searchParams.get('filter');
			params_filter.set(filter);
			params = `${params}&filter=${filter}`;
		}
		if (params) {
			params = `?${params}`;
		}

		const _resp = await fetch(`${backend}/nft${params}`, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (_resp.ok) {
			let resp = await _resp.json();

			count.set(resp.data.count);
			return {
				props: {
					metas: resp.data.metas,
					total_page: resp.data.total_page,
					filter: resp.data.filter
				}
			};
		}
	}
</script>

<script>
	export let metas;
	export let total_page;
	export let filter;

	const submit = async () => {
		let params = '';
		if ($params_page) {
			params = `page=${$params_page}`;
		}
		if ($params_filter) {
			params = `${params}&filter=${$params_filter}`;
		}
		if (params) {
			params = `?${params}`;
		}

		window.history.pushState('', '', params);

		const _resp = await fetch(`${backend}/nft${params}`, {
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

<Filter
	{filter}
	on:ok={() => {
		$params_page = 1;
		$pagination_temp = 1;
		submit();
	}}
/>

<Margin>
	<div class="page">
		{#each metas as meta}
			<Item {meta} />
		{/each}
	</div>
</Margin>

<Pagination
	{total_page}
	on:ok={() => {
		submit();
	}}
/>

<style>
	.page {
		display: grid;

		grid-template-columns: 1fr;
		gap: var(--gap2);
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
</style>
