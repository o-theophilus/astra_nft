<script>
	import { nft_count } from '$lib/store.js';
</script>

<nav>
	<b> Astra NFT - {$nft_count.male + $nft_count.female}</b>
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
		color: var(--ac5_);
		height: var(--headerHeight);
	}
	b {
		font-size: large;
	}
</style>
