export interface ITransaction{
  id: string;
  amount: number;
  description: string;
  date: string;
  category: string;
  type: string;
  user: IAccount;
}

export interface IAccount{
  id: string;
  name: string;
  username: string;
  first_name: string;
  last_name: string;
  language_code: string;
  photo_url: string;
}

export interface ICategory{
  id: string;
  name: string;
}


