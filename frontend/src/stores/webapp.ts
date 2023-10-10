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
  const token = ref();
  const walletsStore = useWallets();

  function enableCloseConfirm() {
    webapp.enableClosingConfirmation();
  }

  function disableCloseConfirm() {
    webapp.disableClosingConfirmation();
  }

  webapp.BackButton.onClick(() => {
    if (window.history.length) {
      router.go(-1);
    } else {
      router.push({ name: 'index' });
    }
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

  const hideMainButton = (fn: () => void) => {
    webapp.MainButton.hide();
    webapp.MainButton.offClick(fn);
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

  function confirm(fn: () => void) {
    webapp.showConfirm('Are you sure?', (agree: boolean) => {
      if (agree) {
        fn();
      }
    });
  }

  function showAlert(text: string) {
    webapp.showAlert(text);
  }

  return {
    webapp,
    showBack,
    hideBack,
    showMainButton,
    hideMainButton,
    auth,
    token,
    confirm,
    enableCloseConfirm,
    disableCloseConfirm,
    showAlert,
  };
});
