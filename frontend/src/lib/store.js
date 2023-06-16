import { writable } from 'svelte/store';

export const module = writable();

export const filter = writable({});
export const total_page = writable(0);
export const nft_count = writable({});

export const page_no = writable(1);
export const page_no_temp = writable(1);
export const fk1 = writable("");
export const fv1 = writable("");
