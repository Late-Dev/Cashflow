import axios, { AxiosResponse } from 'axios';

export const API_URL = process.env.API_URL;
axios.defaults.baseURL = API_URL;

axios.interceptors.request.use((request) => {
  // if (request.url == '/login/') {
  //   return request;
  // }
  // const jwt = useJWT();
  // if (request.headers && jwt.jwt) {
  //   request.headers.Authorization = `Bearer ${jwt.jwt}`;
  // }

  return request;
});

// export function login(){
//   return axios.post('/login')
// }


export function getWallets(user_id: number){ // not needed after authentication update
  return axios.get(`/user_wallets/${user_id}`)
}

export function getTransactions(wallet_id: number){
  return axios.get(`/wallet_transactions/${wallet_id}`)
}

export function getCategories(wallet_id:number){
  return axios.get(`/wallet_categories/${wallet_id}`)
}


export function addUser(id: number){ // not needed after authentication update
  return axios.post('/user', {id})
}

export function addWallet(user_id: number, name: string, currency='USD'){
  return axios.post('/wallet', {user_id, name,currency})
}

export function addCategory(name: string, wallet_id: number, transaction_type: string){
  return axios.post('/category', {
    name,
    wallet_id,
    transaction_type
  })
}

export function addTransaction(description: string, value: number, date: string, source: string, category_id: number, wallet_id: number){
  return axios.post('/transaction', {
    description,
    value,
    date,
    source,
    category_id,
    wallet_id
  })
}

