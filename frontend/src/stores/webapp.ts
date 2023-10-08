import { defineStore } from 'pinia';
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

  return { webapp, showBack, hideBack, showMainButton, hideMainButton };
});
