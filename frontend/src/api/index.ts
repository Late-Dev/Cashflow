import axios, { AxiosResponse } from 'axios';
import { useWebApp } from 'src/stores/webapp';
import { ICategory, ITransaction } from 'src/types';

export const API_URL = process.env.API_URL;
axios.defaults.baseURL = API_URL;

axios.interceptors.request.use((request) => {
  if (request.url == '/login') {
    return request;
  }
  const webappStore = useWebApp();

  if (request.headers && webappStore.token) {
    request.headers.Authorization = `Bearer ${webappStore.token}`;
  }

  return request;
});

export function login(hash_str: string, initData: string) {
  return axios.post('/login', { hash_str, initData });
}

export function getWallets() {
  return axios.get('/user_wallets');
}

export function deleteWalletRequest(id: number) {
  return axios.delete(`/wallet/${id}`);
}

export function getTransactions(wallet_id: number): Promise<
  AxiosResponse<{
    income: ITransaction[];
    outcome: ITransaction[];
  }>
> {
  return axios.get(`/wallet_transactions/${wallet_id}`);
}

export function deleteTransaction(transaction_id: number) {
  return axios.delete(`/transaction/${transaction_id}`);
}

export function getWallet(wallet_id: number) {
  return axios.get(`/wallet/${wallet_id}`);
}

export function getCategories(wallet_id: number) {
  return axios.get(`/wallet_categories/${wallet_id}`);
}

export function deleteCategoryRequest(category_id: number) {
  return axios.delete(`/category/${category_id}`);
}

export function editCategoryRequest(
  category_id: number,
  name: string,
  icon: string,
  color: number
) {
  return axios.patch(`/category/${category_id}`, {
    name,
    icon,
    color,
  });
}

export function addUser(id: number) {
  // not needed after authentication update
  return axios.post('/user', { id });
}

export function addWallet(name: string, currency = 'USD') {
  return axios.post('/wallet', { name, currency });
}

export function addCategory(
  name: string,
  wallet_id: number,
  transaction_type: string,
  icon: string,
  color: number
) {
  return axios.post('/category', {
    name,
    wallet_id,
    transaction_type,
    icon,
    color,
  });
}

export function addTransaction(payload: ITransaction) {
  return axios.post('/transaction', {
    description: payload.description,
    value: payload.value,
    date: new Date(payload.date).toISOString(),
    source: payload.source,
    category_id: (payload.category as ICategory)?.id,
    wallet_id: payload.wallet,
  });
}

export function editTransactionRequest(payload: ITransaction) {
  return axios.patch(`/transaction/${payload.id}`, {
    description: payload.description,
    value: payload.value,
    date: new Date(payload.date).toISOString(),
    source: payload.source,
    category_id: (payload.category as ICategory)?.id,
  });
}

export function getAllUsersInWallet(id: number) {
  return axios.get(`/wallet_users/${id}`);
}

export function generateWalletLink(id: number) {
  return axios.get(`/wallet_generate_link/${id}`);
}

export function verifyWalletLink(link: string) {
  return axios.post('/wallet_verify_link', {
    link,
  });
}
