<script>
	import './layout.var.css';
	import './layout.main.css';

	import Nav from './layout.nav.svelte';
	import Module from './layout.module.svelte';
</script>

<main class:dark={true}>
	<Nav />
	<Module />
	<slot />
	<br /> <br />
	<footer>&copy Astra</footer>
	<br /> <br />
</main>

<style>
	main {
		background-color: var(--ac5);
		color: var(--ac2);
		min-height: 100vh;
	}

	footer {
		text-align: center;
	}
</style>
