<script>
	import '$lib/css/var.css';
	import '$lib/css/main.css';
	import Nav from '$lib/nav.svelte';
	import Module from '$lib/module.svelte';

	let innerWidth;
	let scrollY;
</script>

<svelte:window bind:innerWidth bind:scrollY />
<main>
	<Nav />
	<Module />
	<slot />
</main>

<style>
</style>
