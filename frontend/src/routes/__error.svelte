<script context="module">
	export function load({ error, status }) {
		return {
			props: {
				status,
				error
			}
		};
	}
</script>

<script>
	export let status;
	export let error;
</script>

<svelte:head>
	<title>{status} Error | Meji</title>
</svelte:head>

{@html error.message}
{status}
