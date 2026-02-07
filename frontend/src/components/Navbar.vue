<template>
  <nav class="navbar navbar-expand-lg navbar-dark" :style="{ backgroundColor: '#FF99A8' }">
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
          
          <!-- 月子餐管理 -->
          <li class="nav-item position-relative" v-if="hasMenuPermission('Menu')">
            <a class="nav-link cursor-pointer" @click="toggleDropdown('meal')">
              <i class="fas fa-utensils"></i> 月子餐管理 <i class="fas fa-chevron-down ml-1"></i>
            </a>
            <div class="custom-dropdown-menu" v-if="openDropdown === 'meal'">
              <ul>
                <li v-if="hasMenuPermission('Menu')">
                  <a class="custom-dropdown-item" @click="navigateTo('/menu')">
                    <i class="fas fa-utensils"></i> 菜单管理
                  </a>
                </li>
                <li v-if="hasMenuPermission('Dish')">
                  <a class="custom-dropdown-item" @click="navigateTo('/dish')">
                    <i class="fas fa-drumstick-bite"></i> 菜品管理
                  </a>
                </li>
                <li v-if="hasMenuPermission('Ingredient')">
                  <a class="custom-dropdown-item" @click="navigateTo('/ingredient')">
                    <i class="fas fa-seedling"></i> 食材管理
                  </a>
                </li>
                <li v-if="hasMenuPermission('Menu')" class="dropdown-divider"></li>
                <li v-if="hasMenuPermission('Menu')">
                  <a class="custom-dropdown-item" @click="navigateTo('/menu/calendar')">
                    <i class="fas fa-calendar-alt"></i> 餐单日历
                  </a>
                </li>
              </ul>
            </div>
          </li>
          
          <!-- 母婴服务 -->
          <li class="nav-item position-relative" v-if="hasMenuPermission('Order') || hasMenuPermission('ServiceBooking')">
            <a class="nav-link cursor-pointer" @click="toggleDropdown('service')">
              <i class="fas fa-baby"></i> 母婴服务 <i class="fas fa-chevron-down ml-1"></i>
            </a>
            <div class="custom-dropdown-menu" v-if="openDropdown === 'service'">
              <ul>
                <li v-if="hasMenuPermission('Order')">
                  <a class="custom-dropdown-item" @click="navigateTo('/order')">
                    <i class="fas fa-shopping-cart"></i> 订餐管理
                  </a>
                </li>
                <li v-if="hasMenuPermission('ServiceBooking')">
                  <a class="custom-dropdown-item" @click="navigateTo('/service-booking')">
                    <i class="fas fa-calendar-check"></i> 服务预定
                  </a>
                </li>
              </ul>
            </div>
          </li>
          
          <!-- 管理功能 -->
          <li class="nav-item position-relative" v-if="hasMenuPermission('Customer') || hasMenuPermission('Employee') || hasMenuPermission('Finance') || hasMenuPermission('Report') || hasMenuPermission('DataEntry')">
            <a class="nav-link cursor-pointer" @click="toggleDropdown('management')">
              <i class="fas fa-cogs"></i> 管理功能 <i class="fas fa-chevron-down ml-1"></i>
            </a>
            <div class="custom-dropdown-menu" v-if="openDropdown === 'management'">
              <ul>
                <li v-if="hasMenuPermission('Customer')">
                  <a class="custom-dropdown-item" @click="navigateTo('/customer')">
                    <i class="fas fa-user-friends"></i> 客户管理
                  </a>
                </li>
                <li v-if="hasMenuPermission('Employee')">
                  <a class="custom-dropdown-item" @click="navigateTo('/employee')">
                    <i class="fas fa-users"></i> 员工管理
                  </a>
                </li>
                <li v-if="hasMenuPermission('Finance')">
                  <a class="custom-dropdown-item" @click="navigateTo('/finance')">
                    <i class="fas fa-money-bill-wave"></i> 财务管理
                  </a>
                </li>
                <li v-if="hasMenuPermission('Report')">
                  <a class="custom-dropdown-item" @click="navigateTo('/report')">
                    <i class="fas fa-file-invoice"></i> 报表打印
                  </a>
                </li>
                <li v-if="hasMenuPermission('DataEntry')">
                  <a class="custom-dropdown-item" @click="navigateTo('/data-entry')">
                    <i class="fas fa-database"></i> 数据录入
                  </a>
                </li>
              </ul>
            </div>
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

import { hasRoutePermission } from '../utils/permissions'
import { getCurrentTheme, applyTheme } from '../utils/theme'

const router = useRouter()
const currentUser = ref<any>(null)
const openDropdown = ref<string | null>(null)

// 检查用户是否有权限访问菜单项
const hasMenuPermission = (routeName: string) => {
  if (!currentUser.value) {
    // 未登录用户默认显示基本菜单项
    const defaultRoutes = ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'Customer', 'Employee', 'Finance', 'Report', 'DataEntry']
    return defaultRoutes.includes(routeName)
  }
  return hasRoutePermission(currentUser.value.role, routeName)
}

// 处理下拉菜单切换
const toggleDropdown = (dropdown: string) => {
  if (openDropdown.value === dropdown) {
    openDropdown.value = null
  } else {
    openDropdown.value = dropdown
  }
}

// 处理页面跳转
const navigateTo = (path: string) => {
  router.push(path)
  openDropdown.value = null // 跳转到新页面后关闭下拉菜单
}

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/')
}

// 点击页面其他地方关闭下拉菜单
const handleClickOutside = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (!target.closest('.nav-item')) {
    openDropdown.value = null
  }
}

// 初始化用户信息和主题
onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    currentUser.value = JSON.parse(userStr)
  }

  const theme = getCurrentTheme()
  applyTheme(theme)
  
  // 添加全局点击事件监听器
  document.addEventListener('click', handleClickOutside)
})

// 清理全局点击事件监听器
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style>
/* 导航栏样式 */
.navbar {
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

.cursor-pointer {
  cursor: pointer;
}

.ml-1 {
  margin-left: 0.25rem;
}

/* 自定义下拉菜单样式 */
.custom-dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 0.125rem;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  z-index: 1000;
}

.custom-dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.custom-dropdown-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--primary-color);
  padding: 0.5rem 1rem;
  text-decoration: none;
  transition: background-color 0.2s;
}

.custom-dropdown-item:hover {
  background-color: rgba(var(--primary-color-rgb), 0.1);
}

/* 下拉菜单分隔线 */
.dropdown-divider {
  height: 1px;
  margin: 0.5rem 0;
  background-color: rgba(0, 0, 0, 0.1);
}

.btn-outline-light {
  border-color: white;
  color: white;
}

.btn-outline-light:hover {
  background-color: white;
  color: #FF99A8;
}
</style>
