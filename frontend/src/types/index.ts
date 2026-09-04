export interface ITransaction {
  id: number;
  value: number;
  currency?: string;
  usd_to_currency_rate?: number;
  usd_value?: number;
  display_value?: number;
  display_currency?: string;
  description?: string;
  date: string;
  category?: ICategory | number;
  type: 'income' | 'outcome';
  user: IAccount;
  source?: string;
  wallet?: number;
}

export interface IAccount {
  id: string;
  name: string;
  username: string;
  first_name: string;
  last_name: string;
  language_code: string;
  photo_url: string;
}

export interface ICategory {
  id: number;
  name: string;
  icon: string;
  color: number;
  transaction_type: 'income' | 'outcome';
}

export interface Wallet {
  id: number;
  name: string;
  currency: string;
  default_currency: string;
  user_type: '';
  is_default?: boolean;
}

export interface Currency {
  code: string;
  name: string;
  symbol: string;
}
