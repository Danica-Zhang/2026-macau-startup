import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Diagnose from './views/Diagnose.vue'
import Ideation from './views/Ideation.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/diagnose', component: Diagnose },
  { path: '/diagnose', component: Diagnose },
  { path: '/ideation', component: Ideation }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router