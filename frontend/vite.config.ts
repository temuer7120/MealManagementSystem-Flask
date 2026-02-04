import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import * as path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },
  // 优化解析配置，处理大小写敏感性问题
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    },
    // 确保路径解析使用一致的大小写
    conditions: ['development', 'production'],
    extensions: ['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json', '.vue']
  },
  // 构建配置
  build: {
    // 确保构建过程使用一致的路径处理
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    // 优化构建性能
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  }
})
