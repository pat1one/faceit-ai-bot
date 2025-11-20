const esbuild = require('esbuild');

async function main() {
  try {
    await esbuild.build({
      entryPoints: ['extension/src/popup.tsx'],
      bundle: true,
      outfile: 'extension/popup.js',
      format: 'iife',
      target: ['chrome115', 'edge115'],
      sourcemap: false,
      minify: true,
      define: {
        'process.env.NODE_ENV': '"production"',
      },
      loader: {
        '.ts': 'ts',
        '.tsx': 'tsx',
      },
    });
    console.log('✅ Extension popup built to extension/popup.js');
  } catch (e) {
    console.error('Failed to build extension popup', e);
    process.exit(1);
  }
}

main();
