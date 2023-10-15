import { defineStore } from 'pinia';
import { login, verifyWalletLink } from 'src/api';
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

  webapp.expand();
  webapp.ready();
  const router = useRouter();
  const token = ref();
  const walletsStore = useWallets();

  function shareWallet(walletName: string) {
    webapp.switchInlineQuery(walletName, ['users']);
  }

  const inviteToken = webapp.initDataUnsafe.start_param;

  const mainButton = ref({
    text: '',
    onClick: () => {
      return;
    },
    isVisible: false,
    disabled: false,
  });

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
    mainButton.value.disabled = false;
    mainButton.value.isVisible = true;
    mainButton.value.text = text;
    mainButton.value.onClick = fn;
  };

  const disableMainButton = () => {
    mainButton.value.disabled = true;
  };

  const hideMainButton = () => {
    mainButton.value.isVisible = false;
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

    if (inviteToken) {
      await verifyWalletLink(inviteToken.replaceAll('_', '.'))
        .then(() => {
          webapp.showAlert('You have been added to the wallet');
        })
        .catch((error) => {
          webapp.showAlert(error.response.data.detail);
        });
    }
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
    mainButton,
    disableMainButton,
    shareWallet,
  };
});
