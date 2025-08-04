import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import ProductAdd from '../views/ProductAdd.vue';
import ProductOverview from '../views/ProductOverview.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/products/add',
    name: 'ProductAdd',
    component: ProductAdd
  },
  {
    path: '/products',
    name: 'ProductOverview',
    component: ProductOverview
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;