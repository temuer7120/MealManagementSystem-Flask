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
    }
  ]
})

// 添加路由守卫以检查权限
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null
  const role = user ? user.role : null
  
  // 未登录用户重定向到登录页
  if (!token && to.path !== '/' && to.path !== '/login') {
    next('/')
    return
  }
  
  // 登录页不需要权限检查
  if (to.path === '/' || to.path === '/login') {
    next()
    return
  }
  
  // 检查用户是否有权限访问该路由
  if (to.name && !hasRoutePermission(role, to.name)) {
    next('/dashboard')
    return
  }
  
  // 检查子路由权限
  if (to.matched.length > 1) {
    const childRoute = to.matched[to.matched.length - 1]
    if (childRoute.name && !hasRoutePermission(role, childRoute.name)) {
      next('/dashboard')
      return
    }
  }
  
  next()
})

export default router