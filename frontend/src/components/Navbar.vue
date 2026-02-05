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
          
          <!-- 月子餐管理 -->
          <li class="nav-item" v-if="hasMenuPermission('Menu')">
            <el-dropdown>
              <span class="nav-link dropdown-toggle">
                <i class="fas fa-utensils"></i> 月子餐管理
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="navigateTo('/menu')" v-if="hasMenuPermission('Menu')">
                    <i class="fas fa-utensils"></i> 菜单管理
                  </el-dropdown-item>
                  <el-dropdown-item @click="navigateTo('/dish')" v-if="hasMenuPermission('Dish')">
                    <i class="fas fa-drumstick-bite"></i> 菜品管理
                  </el-dropdown-item>
                  <el-dropdown-item @click="navigateTo('/ingredient')" v-if="hasMenuPermission('Ingredient')">
                    <i class="fas fa-seedling"></i> 食材管理
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </li>
          
          <!-- 母婴服务 -->
          <li class="nav-item" v-if="hasMenuPermission('Order') || hasMenuPermission('ServiceBooking')">
            <el-dropdown>
              <span class="nav-link dropdown-toggle">
                <i class="fas fa-baby"></i> 母婴服务
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="navigateTo('/order')" v-if="hasMenuPermission('Order')">
                    <i class="fas fa-shopping-cart"></i> 订餐管理
                  </el-dropdown-item>
                  <el-dropdown-item @click="navigateTo('/service-booking')" v-if="hasMenuPermission('ServiceBooking')">
                    <i class="fas fa-calendar-check"></i> 服务预定
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </li>
          
          <!-- 管理功能 -->
          <li class="nav-item" v-if="hasMenuPermission('Customer') || hasMenuPermission('Employee') || hasMenuPermission('Finance') || hasMenuPermission('Report')">
            <el-dropdown>
              <span class="nav-link dropdown-toggle">
                <i class="fas fa-cogs"></i> 管理功能
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="navigateTo('/customer')" v-if="hasMenuPermission('Customer')">
                    <i class="fas fa-user-friends"></i> 客户管理
                  </el-dropdown-item>
                  <el-dropdown-item @click="navigateTo('/employee')" v-if="hasMenuPermission('Employee')">
                    <i class="fas fa-users"></i> 员工管理
                  </el-dropdown-item>
                  <el-dropdown-item @click="navigateTo('/finance')" v-if="hasMenuPermission('Finance')">
                    <i class="fas fa-money-bill-wave"></i> 财务管理
                  </el-dropdown-item>
                  <el-dropdown-item @click="navigateTo('/report')" v-if="hasMenuPermission('Report')">
                    <i class="fas fa-file-invoice"></i> 报表打印
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
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
import { getCurrentTheme, applyTheme } from '../utils/theme'

const { proxy } = getCurrentInstance()!
const currentUser = ref<any>(null)

// 检查用户是否有权限访问菜单项
const hasMenuPermission = (routeName: string) => {
  if (!currentUser.value) {
    // 未登录用户默认显示基本菜单项
    const defaultRoutes = ['Dashboard', 'ServiceBooking']
    return defaultRoutes.includes(routeName)
  }
  return hasRoutePermission(currentUser.value.role, routeName)
}

// 处理页面跳转
const navigateTo = (path: string) => {
  proxy?.$router.push(path)
}

// 处理退出登录
const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  proxy?.$router.push('/')
}

// 初始化用户信息和主题
onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    currentUser.value = JSON.parse(userStr)
  }
  
  // 应用当前用户的主题
  const theme = getCurrentTheme()
  applyTheme(theme)
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

/* Element Plus 下拉菜单样式 */
:deep(.el-dropdown-menu) {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 180px;
}

:deep(.el-dropdown-menu__item) {
  color: var(--primary-color);
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  line-height: 40px;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: rgba(52, 152, 219, 0.1);
  color: var(--primary-color);
}

/* 下拉菜单项样式 */
.dropdown-toggle {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
}

.dropdown-toggle:hover {
  color: #f0f0f0;
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
