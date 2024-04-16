import { defineConfig } from 'vite';

// ----------------------------------------------------------------

import vue from '@vitejs/plugin-vue';

const build = {
  rollupOptions: {
    output: {
      chunkFileNames: 'chunk/[hash:16].js', // use randomized filenames
      entryFileNames: 'index/[hash:16].js', // use randomized filenames
      hashCharacters: 'base36',
      assetFileNames: ({ name }) => {
        if (name.includes('index') && name.includes('.css')) {
          return 'index/[hash:16][extname]';
        } /* images */ else if (name.includes('.jpg') || name.includes('.png')) {
          return 'images/[hash:16][extname]';
        } /* images */ else if (name.includes('.gif') || name.includes('.svg')) {
          return 'images/[hash:16][extname]';
        } /* assets by default */ else {
          return 'assets/[hash:16][extname]';
        }
      }
    }
  }
};

// ----------------------------------------------------------------

import obfuscator from 'rollup-plugin-obfuscator';

const plugins = [
  vue(), // vue converter
  // vue(), // https://cn.vitejs.dev/guide/features.html, @vitejs/plugin-vue2
  // vueJsx(), // https://cn.vitejs.dev/guide/features.html, @vitejs/plugin-vue2-jsx
  // vue(), // https://cn.vitejs.dev/guide/features.html, @vitejs/plugin-vue
  // vueJsx(), // https://cn.vitejs.dev/guide/features.html, @vitejs/plugin-vue-jsx
  obfuscator({
    global: true,
    options: {
      // seed: 996,
      // seed: 997,
      seed: 23333,
      optionsPreset: 'high-obfuscation'
    }
  })
];

// ----------------------------------------------------------------

export default defineConfig({ plugins, build });
