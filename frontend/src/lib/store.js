import { writable } from 'svelte/store';

export const backend = import.meta.env.VITE_BACKEND;
export const module = writable();

export const count = writable({});
export const params_page = writable(1);
export const pagination_temp = writable(1);
export const params_filter = writable("");
