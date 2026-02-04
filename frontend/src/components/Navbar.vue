<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#/dashboard">
        <i class="fas fa-hotel"></i> 上海巍阁公司管理系统
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-nav" aria-controls="navbar-nav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbar-nav">
        <ul class="navbar-nav me-auto">
          <!-- 首页 -->
          <li class="nav-item">
            <router-link to="/dashboard" class="nav-link" active-class="active">
              <i class="fas fa-home"></i> 首页
            </router-link>
          </li>
          
          <!-- 菜单管理 -->
          <li v-if="hasMenuPermission('Menu')" class="nav-item">
            <router-link to="/menu" class="nav-link" active-class="active">
              <i class="fas fa-utensils"></i> 菜单管理
            </router-link>
          </li>
          
          <!-- 菜品管理 -->
          <li v-if="hasMenuPermission('Dish')" class="nav-item">
            <router-link to="/dish" class="nav-link" active-class="active">
              <i class="fas fa-drumstick-bite"></i> 菜品管理
            </router-link>
          </li>
          
          <!-- 客户管理 -->
          <li v-if="hasMenuPermission('Customer')" class="nav-item">
            <router-link to="/customer" class="nav-link" active-class="active">
              <i class="fas fa-user-friends"></i> 客户管理
            </router-link>
          </li>
          
          <!-- 订单管理 -->
          <li v-if="hasMenuPermission('Order')" class="nav-item">
            <router-link to="/order" class="nav-link" active-class="active">
              <i class="fas fa-shopping-cart"></i> 订单管理
            </router-link>
          </li>
          
          <!-- 母婴管理 -->
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="mother-baby-dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              <i class="fas fa-baby"></i> 母婴管理
            </a>
            <ul class="dropdown-menu" aria-labelledby="mother-baby-dropdown">
              <li>
                <router-link to="/mother-baby/confinement-meal" class="dropdown-item">
                  <i class="fas fa-utensil-spoon"></i> 月子餐
                </router-link>
              </li>
              <li>
                <router-link to="/mother-baby/health" class="dropdown-item">
                  <i class="fas fa-heartbeat"></i> 健康管理
                </router-link>
              </li>
              <li>
                <router-link to="/mother-baby/appointment" class="dropdown-item">
                  <i class="fas fa-calendar-alt"></i> 预约管理
                </router-link>
              </li>
              <li>
                <router-link to="/mother-baby/nutrition" class="dropdown-item">
                  <i class="fas fa-apple-alt"></i> 营养管理
                </router-link>
              </li>
            </ul>
          </li>
          
          <!-- 系统管理 -->
          <li v-if="hasMenuPermission('System')" class="nav-item">
            <router-link to="/system" class="nav-link" active-class="active">
              <i class="fas fa-cogs"></i> 系统管理
            </router-link>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <span class="nav-link">
              <i class="fas fa-user"></i> 欢迎，{{ currentUser?.username || '用户' }}
            </span>
          </li>
          <li class="nav-item">
            <button class="btn btn-outline-light" @click="handleLogout">
              <i class="fas fa-sign-out-alt"></i> 退出登录
            </button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue' // 若IDE仍报错，可尝试重启Volar或检查tsconfig.json是否包含"vue"类型声明
// 仅移除显式的 Router 类型导入，实际使用时由 Vue 自动注入
import { getCurrentInstance } from 'vue'

import { hasRoutePermission } from '../utils/permissions'

const { proxy } = getCurrentInstance()!
const router = proxy?.$router
const currentUser = ref<any>(null)

// 检查用户是否有权限访问菜单项
const hasMenuPermission = (routeName: string) => {
  if (!currentUser.value) return false
  return hasRoutePermission(currentUser.value.role, routeName)
}

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  proxy?.$router.push('/login')
}

// 初始化用户信息
onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    currentUser.value = JSON.parse(userStr)
  }
})
</script>

<style scoped>
/* 导航栏样式 */
.navbar {
  background-color: var(--primary-color);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
}

.navbar-nav .nav-link {
  color: white;
  font-size: 1rem;
  margin-right: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.navbar-nav .nav-link:hover {
  color: #f0f0f0;
}

.navbar-nav .nav-link.active {
  font-weight: bold;
  border-bottom: 2px solid white;
}

.dropdown-menu {
  background-color: var(--primary-color);
  border: none;
  border-radius: 0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dropdown-item {
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dropdown-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.btn-outline-light {
  border-color: white;
  color: white;
}

.btn-outline-light:hover {
  background-color: white;
  color: var(--primary-color);
}
</style>
