import vercel from '@sveltejs/adapter-vercel';

const config = {
	kit: {
		adapter: vercel(),

		files: {
			lib: 'src/lib'
		  }
	}
};

export default config;
