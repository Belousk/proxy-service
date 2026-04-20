/**
 * router/index.ts
 *
 * Manual routes for ./src/pages/*.vue
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import Index from '@/pages/index.vue'
import Users from '@/pages/users.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Index,
    },
    {
      path: '/users',
      component: Users,
    },
    { 
      path: '/register', 
      component: () => import('@/pages/register.vue') 
    },
    { 
      path: '/login', 
      component: () => import('@/pages/login.vue') 
    },
    { 
      path: '/profile', 
      component: () => import('@/pages/profile.vue') 
    },
  ],
})

export default router
