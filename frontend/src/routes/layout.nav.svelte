<script>
	import { nft_count } from '$lib/store.js';
</script>

<nav>
	<div class="block">
		<img src="./image/logo.png" alt="" />
		{($nft_count.male + $nft_count.female).toLocaleString()} NFT
	</div>
</nav>

<style>
	nav {
		position: sticky;
		top: 0;
		z-index: 2;

		background: linear-gradient(to top right, var(--cl0), var(--cl1));
		color: var(--ac5_);
	}
	.block {
		display: flex;
		align-items: center;
		gap: var(--sp2);
		justify-content: space-between;

		max-width: var(--headerWidth);
		height: var(--headerHeight);
		padding: 0 var(--sp2);
		margin: auto;
	}
</style>
