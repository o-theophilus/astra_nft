import { filter, total_page, nft_count, page_no, fk1, fv1 } from '$lib/store.js';

export const load = async ({ fetch, url }) => {

	let backend = new URL(`${import.meta.env.VITE_BACKEND}/nft`)
	
	if (url.searchParams.has('page_no')) {
		let temp = url.searchParams.get('page_no');
		backend.searchParams.set('page_no', temp);
		page_no.set(temp);
	}
	if (url.searchParams.has('fk1') && url.searchParams.has('fv1')) {
		let _fk1 = url.searchParams.get('fk1');
		backend.searchParams.set('fk1', _fk1);
		fk1.set(_fk1);
		let _fv1 = url.searchParams.get('fv1');
		backend.searchParams.set('fv1', _fv1);
		fv1.set(_fv1);
	}

	let resp = await fetch(backend, {
		method: 'get',
		headers: {
			'Content-Type': 'application/json'
		}
	});

	resp = await resp.json();
	if (resp.status == 200) {
		filter.set(resp.filter);
		total_page.set(resp.total_page);
		nft_count.set(resp.nft_count);
		return {
			metas: resp.metas
		}
    }
}
