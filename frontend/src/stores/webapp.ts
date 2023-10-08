import { defineStore } from 'pinia';
import { login } from 'src/api';
import { TelegramWebApps } from 'telegram-webapps-types-new';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useWallets } from './wallets';
declare global {
  interface Window {
    Telegram: TelegramWebApps.SDK;
  }
}

export const useWebApp = defineStore('webapp', () => {
  const webapp = window.Telegram.WebApp;
  const router = useRouter();

  const walletsStore = useWallets();
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
  async function auth() {
    if (!webapp.initDataUnsafe.hash) {
      webapp.showAlert('no hash!');
      return;
    }
    await login(webapp.initDataUnsafe.hash, webapp.initData).then(
      (response) => {
        token.value = response.data.jwt_token;
      }
    );
    await walletsStore.loadWallets();
  }

  const token = ref();

  return {
    webapp,
    showBack,
    hideBack,
    showMainButton,
    hideMainButton,
    auth,
    token,
  };
});
