import axios, { AxiosResponse } from 'axios';
import { useWebApp } from 'src/stores/webapp';
import { ITransaction } from 'src/types';

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
  // not needed after authentication update
  return axios.get('/user_wallets');
}

export function getTransactions(wallet_id: number): Promise<
  AxiosResponse<{
    income: ITransaction;
    outcome: ITransaction;
  }>
> {
  return axios.get(`/wallet_transactions/${wallet_id}`);
}

export function getCategories(wallet_id: number) {
  return axios.get(`/wallet_categories/${wallet_id}`);
}

export function addUser(id: number) {
  // not needed after authentication update
  return axios.post('/user', { id });
}

export function addWallet(user_id: number, name: string, currency = 'USD') {
  return axios.post('/wallet', { user_id, name, currency });
}

export function addCategory(
  name: string,
  wallet_id: number,
  transaction_type: string
) {
  return axios.post('/category', {
    name,
    wallet_id,
    transaction_type,
  });
}

export function addTransaction(payload: Omit<ITransaction, 'id' | 'user' >) {
  return axios.post('/transaction', {
    description: payload.description,
    value: payload.value,
    date: payload.date,
    source: payload.source,
    category_id: payload.category,
    wallet_id: payload.wallet,
  });
}
