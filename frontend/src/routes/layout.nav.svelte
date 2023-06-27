<script>
	import { nft_count } from '$lib/store.js';
</script>

<nav>
	<div class="block">
		<a href="/" data-sveltekit-reload>
			<img src="./image/logo.png" alt="Astra Logo" />
		</a>
		{($nft_count.male + $nft_count.female).toLocaleString()} NFTs
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
	img {
		height: 30px;
	}
</style>
