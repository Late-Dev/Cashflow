import { defineStore } from 'pinia';
import { TelegramWebApps } from 'telegram-webapps-types-new';

declare global {
  interface Window {
    Telegram: TelegramWebApps.SDK;
  }
}

export const useWebApp = defineStore('webapp', () => {
  const webapp = window.Telegram.WebApp;

  return { webapp };
});
