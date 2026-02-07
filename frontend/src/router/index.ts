import { createRouter, createWebHistory } from 'vue-router'

import { hasRoutePermission } from '../utils/permissions'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Login',
      component: () => import('../views/auth/Login.vue')
    },
    {
      path: '/login',
      redirect: '/'
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: () => import('../views/dashboard/Dashboard.vue')
    },
    {
      path: '/menu',
      name: 'Menu',
      component: () => import('../views/menu/Menu.vue')
    },
    {
      path: '/menu/calendar',
      name: 'MealCalendar',
      component: () => import('../views/menu/MealCalendar.vue')
    },
    {
      path: '/dish',
      name: 'Dish',
      component: () => import('../views/dish/Dish.vue')
    },
    {
      path: '/customer',
      name: 'Customer',
      component: () => import('../views/customer/Customer.vue')
    },
    {
      path: '/order',
      name: 'Order',
      component: () => import('../views/order/Order.vue')
    },
    {
      path: '/ingredient',
      name: 'Ingredient',
      component: () => import('../views/ingredient/Ingredient.vue')
    },
    {
      path: '/service-booking',
      name: 'ServiceBooking',
      component: () => import('../views/service-booking/ServiceBooking.vue')
    },
    {
      path: '/employee',
      name: 'Employee',
      component: () => import('../views/employee/Employee.vue')
    },
    {
      path: '/finance',
      name: 'Finance',
      component: () => import('../views/finance/Finance.vue')
    },
    {
      path: '/report',
      name: 'Report',
      component: () => import('../views/report/Report.vue')
    },
    {
      path: '/data-entry',
      name: 'DataEntry',
      component: () => import('../views/system/DataEntry.vue')
    }
  ]
})

// 添加路由守卫以检查权限
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null
  const role = user ? user.role : null
  
  // 未登录用户可以访问基本管理界面
  if (!token) {
    const allowedRoutes = ['/', '/login', '/dashboard', '/service-booking', '/menu', '/menu/calendar', '/dish', '/ingredient', '/order', '/customer', '/employee', '/finance', '/report', '/data-entry']
    if (!allowedRoutes.includes(to.path)) {
      next('/')
      return
    }
  }
  
  // 登录页不需要权限检查
  if (to.path === '/' || to.path === '/login') {
    next()
    return
  }
  
  // 已登录用户检查权限
  if (token && role) {
    // 检查用户是否有权限访问该路由
    if (to.name) {
      // 对于子路由，使用父路由的权限检查
      let routeNameToCheck = to.name as string
      
      // 处理餐单日历等子路由
      if (routeNameToCheck === 'MealCalendar') {
        routeNameToCheck = 'Menu'
      }
      
      if (!hasRoutePermission(role, routeNameToCheck)) {
        next('/dashboard')
        return
      }
    }
  }
  
  next()
})

export default router