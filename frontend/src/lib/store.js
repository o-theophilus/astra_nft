import { writable } from 'svelte/store';

export const backend = import.meta.env.VITE_BACKEND;
export const module = writable();

export const male_count = writable(0);
export const female_count = writable(0);
