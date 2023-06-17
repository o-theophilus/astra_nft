import { nft_count} from '$lib/store.js';

export const load = async ({ fetch, url }) => {
	let backend = new URL(`${import.meta.env.VITE_BACKEND}/nft`)
	
	if (url.searchParams.has('page_no')) {
		backend.searchParams.set('page_no', url.searchParams.get('page_no'));
	}
	if (url.searchParams.has('fk1') && url.searchParams.has('fv1')) {
		backend.searchParams.set('fk1', url.searchParams.get('fk1'));
		backend.searchParams.set('fv1', url.searchParams.get('fv1'));
	}

	let resp = await fetch(backend, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	resp = await resp.json();
	if (resp.status == 200) {
		nft_count.set(resp.nft_count);
		return {
			metas: resp.metas,
			filter: resp.filter,
			total_page: resp.total_page,
		}
    }
}
