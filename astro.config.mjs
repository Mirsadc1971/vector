import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://vectorbuildingservices.com',
  integrations: [tailwind(), sitemap()],
  trailingSlash: 'ignore',
  build: {
    format: 'directory'
  }
});