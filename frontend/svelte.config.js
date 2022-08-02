import vercel from '@sveltejs/adapter-vercel';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: vercel(),

		files: {
			lib: 'src/lib'
		  }
	}
};

export default config;
