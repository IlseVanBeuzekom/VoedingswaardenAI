import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import ProductAdd from '../views/ProductAdd.vue';
import ProductOverview from '../views/ProductOverview.vue';
import ProductEdit from '../views/ProductEdit.vue';
import RecipeAdd from '../views/RecipeAdd.vue';

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
  },
  {
    path: '/products/edit/:id',
    name: 'ProductEdit',
    component: ProductEdit
  },
  {
    path: '/recipes/add',
    name: 'RecipeAdd',
    component: RecipeAdd
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;