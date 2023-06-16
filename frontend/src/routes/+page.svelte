<script>
	import { page_no, page_no_temp, fk1, fv1, total_page } from '$lib/store.js';

	import Item from './page.item.svelte';
	import Pagination from './page.pagination.svelte';
	import Filter from './page.filter.svelte';

	export let data;
	let { metas } = data;

	const submit = async (is_filter = false) => {
		let backend = new URL(`${import.meta.env.VITE_BACKEND}/nft`);

		if ($page_no && !is_filter) {
			backend.searchParams.append('page_no', $page_no);
		}
		if ($fk1 && $fv1) {
			backend.searchParams.append('fk1', $fk1);
			backend.searchParams.append('fv1', $fv1);
		}

		// window.history.pushState(history.state, '', `${window.location.pathname}${backend.search}`);
		window.history.replaceState(history.state, '', `${window.location.pathname}${backend.search}`);

		if (is_filter) {
			$page_no = 1;
			$page_no_temp = 1;
		}

		let resp = await fetch(backend, {
			method: 'get',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		resp = await resp.json();
		metas = resp.metas;
		$total_page = resp.total_page;

		window.scrollTo({ top: 0, behavior: 'smooth' });
	};
</script>

<Filter
	on:ok={() => {
		submit('filter');
	}}
/>

<div class="page">
	{#each metas as meta}
		<Item {meta} />
	{/each}
</div>

<Pagination
	on:ok={() => {
		submit();
	}}
/>

<style>
	.page {
		margin: var(--gap2);
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
