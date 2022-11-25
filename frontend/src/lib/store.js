import { writable } from 'svelte/store';

export const backend = import.meta.env.VITE_BACKEND;
export const module = writable();

export const count = writable({});
