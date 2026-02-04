<template>
  <div id="app">
    <!-- 导航栏 -->
    <Navbar v-if="isLoggedIn" />
    
    <!-- 路由视图 -->
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'



import { useRoute } from 'vue-router'




import { getCurrentTheme, applyTheme } from './utils/theme'
import Navbar from './components/Navbar.vue'

const route = useRoute()
const isLoggedIn = ref(false)

// 检查用户是否已登录
const checkLoginStatus = () => {
  const token = localStorage.getItem('token')
  isLoggedIn.value = !!token
}

// 监听路由变化，检查登录状态
watch(
  () => route.path,
  () => {
    checkLoginStatus()
  }
)

// App.vue 根组件
onMounted(() => {
  // 检查登录状态
  checkLoginStatus()
  
  // 应用当前用户的主题
  const theme = getCurrentTheme()
  applyTheme(theme)
})
</script>

<style>
/* 全局样式 */
:root {
  --primary-color: #3498db;
}

#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
}

/* 导航栏样式 */
.navbar {
  background-color: var(--primary-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-nav .nav-link {
  color: white;
  font-size: 1rem;
  margin-right: 1rem;
}

.navbar-nav .nav-link:hover {
  color: #f0f0f0;
}

/* 按钮样式 */
.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

/* 卡片样式 */
.card-header {
  background-color: var(--primary-color);
  color: white;
  font-weight: bold;
  border-radius: 8px 8px 0 0;
}

/* 页面标题样式 */
.page-title {
  color: var(--primary-color);
  font-weight: bold;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid var(--primary-color);
  padding-bottom: 0.5rem;
}

/* 链接样式 */
.btn-link {
  color: var(--primary-color);
  text-decoration: none;
}

.btn-link:hover {
  color: #2980b9;
  text-decoration: underline;
}
</style>