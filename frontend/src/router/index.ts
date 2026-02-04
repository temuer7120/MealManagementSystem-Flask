import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'



import { hasRoutePermission } from '../utils/permissions'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/dashboard'
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/auth/Login.vue')
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
      path: '/mother-baby',
      name: 'MotherBaby',
      component: () => import('../views/mother-baby/MotherBaby.vue'),
      children: [
        {
          path: 'confinement-meal',
          name: 'ConfinementMeal',
          component: () => import('../views/mother-baby/ConfinementMeal.vue')
        },
        {
          path: 'health',
          name: 'Health',
          component: () => import('../views/mother-baby/Health.vue')
        },
        {
          path: 'appointment',
          name: 'Appointment',
          component: () => import('../views/mother-baby/Appointment.vue')
        },
        {
          path: 'nutrition',
          name: 'Nutrition',
          component: () => import('../views/mother-baby/Nutrition.vue')
        }
      ]
    },
    {
      path: '/system',
      name: 'System',
      component: () => import('../views/system/System.vue')
    }
  ]
})

// 添加路由守卫以检查权限
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userStr = localStorage.getItem('user')
  const user = userStr ? JSON.parse(userStr) : null
  const role = user ? user.role : null
  
  // 未登录用户重定向到登录页
  if (!token && to.path !== '/login') {
    next('/login')
    return
  }
  
  // 登录页不需要权限检查
  if (to.path === '/login') {
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