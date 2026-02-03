import { createRouter, createWebHistory } from 'vue-router'

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

export default router