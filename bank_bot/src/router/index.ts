import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Portal from '../views/Portal.vue'
import Sign from '../views/Sign.vue'
import { getToken } from '@/utils/auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Portal',
    meta: {
      login: true
    },
    component: Portal
  },
  {
    path: '/sign',
    name: 'Sign',
    component: Sign
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  let token = getToken()
  if (token === undefined) {
    token = ''
  }
  if (token.length > 0 && to.name == 'Sign') {
    next({
      name: 'Portal'
    })
  } else if (token.length > 0 || !to.meta.login) {
    next()
  } else {
    next({
      name: 'Sign',
      query: {
        redirect: to.fullPath //当前页面的地址
      }
    })
  }
})

export default router
