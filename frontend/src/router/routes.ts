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
    ],
  },
  {
    path: '/new',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: '',
        name: 'new',
        component: () => import('pages/NewTransactionPage.vue'),
      },
    ],
  },
  {
    path: '/category',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: '/category/new',
        name: 'newCategory',
        component: () => import('pages/EditCategory.vue'),
      },
      {
        path: '/category/edit/:id',
        name: 'editCategory',
        component: () => import('pages/EditCategory.vue'),
      },
    ],
  },
  {
    path: '/',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: '/select/:type',
        name: 'select',
        component: () => import('pages/SelectionsPage.vue'),
      },
      {
        path: '/explore/:id',
        name: 'explore',
        component: () => import('pages/TransactionExplorePage.vue'),
      },
      {
        path: 'edit',
        name: 'editTransaction',
        component: () => import('pages/EditTransactionPage.vue'),
      },
      {
        path: 'editWallet/id',
        name: 'editWallet',
        component: () => import('pages/WalletSettingsPage.vue'),
      },
    ],
  },
  {
    path: '/wallets',
    component: () => import('layouts/BlankLayout.vue'),
    children: [
      {
        path: '',
        name: 'wallets',
        component: () => import('pages/WalletsPage.vue'),
      },
      {
        path: 'add',
        name: 'addWallet',
        component: () => import('pages/AddWalletPage.vue'),
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
