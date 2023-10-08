import { defineStore } from 'pinia';
import { login } from 'src/api';
import { TelegramWebApps } from 'telegram-webapps-types-new';
import { useRouter } from 'vue-router';

declare global {
  interface Window {
    Telegram: TelegramWebApps.SDK;
  }
}

export const useWebApp = defineStore('webapp', () => {
  const webapp = window.Telegram.WebApp;
  const router = useRouter();
  // webapp.enableClosingConfirmation();

  webapp.BackButton.onClick(() => {
    router.go(-1);
  });

  const showBack = () => {
    webapp.BackButton.show();
  };

  const hideBack = () => {
    webapp.BackButton.hide();
  };

  const showMainButton = (text: string, fn: () => void) => {
    webapp.MainButton.setParams({ text, is_visible: true });
    webapp.MainButton.onClick(fn);
  };

  const hideMainButton = () => {
    webapp.MainButton.hide();
  };

  const auth = async () => {
    if (!webapp.initDataUnsafe.hash) return Promise.resolve('not logged in');
    const response = await login(webapp.initDataUnsafe.hash, webapp.initData);

    return response.data;
  };

  return { webapp, showBack, hideBack, showMainButton, hideMainButton, auth };
});
