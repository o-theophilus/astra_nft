<script>
	import { count } from '$lib/store.js';
</script>

<nav>
	<b> Astra NFT - 5000
		 <!-- (m:{$count.male}, f:{$count.female})</b> -->
</nav>

<style>
	nav {
		display: flex;
		align-items: center;
		justify-content: center;

		position: sticky;
		top: 0;
		z-index: 2;

		padding: 0 var(--gap2);
		background-color: var(--color3);
		color: var(--light_color);
		height: var(--headerHeight);
	}
	b {
		font-size: large;
	}
</style>
