import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'index',
        component: () => import('pages/IndexPage.vue'),
      },
      {
        path: '/explore/:id',
        name: 'explore',
        component: () => import('pages/TransactionExplorePage.vue'),
      },
    ],
  },
  {
    path: '/new',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'new',
        component: () => import('pages/NewTransactionPage.vue'),
      },
    ],
  },
  {
    path: '/select',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: '/:type',
        name: 'select',
        component: () => import('pages/NewTransactionPage.vue'),
      },
    ],
  },
  {
    path: '/settings',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: '',
        name: 'settings',
        component: () => import('pages/SettingsPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
