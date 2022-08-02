import { writable } from 'svelte/store';

export const backend = import.meta.env.VITE_BACKEND;

export const showHeader = writable(true);
export const openMobileMenu = writable(false);
export const isMobile = writable(true);

export const module = writable();



export const loading = writable(false);



export const _tick = writable("");
export const tick = (data)=> {
	_tick.set(data);
}
