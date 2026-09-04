import { defineStore } from 'pinia';
import { login, setLanguageRequest, verifyWalletLink } from 'src/api';
import { TelegramWebApps } from 'telegram-webapps-types-new';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useWallets } from './wallets';
import { i18n, normalizeLocale, MessageLanguages } from 'src/boot/i18n';
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
  const language = ref<MessageLanguages>('en-US');
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

  const enableMainButton = () => {
    mainButton.value.disabled = false;
  };

  const hideMainButton = () => {
    mainButton.value.isVisible = false;
  };
  async function auth() {
    const detectedLanguage = normalizeLocale(webapp.initDataUnsafe.user?.language_code);
    setLanguage(detectedLanguage, false);
    if (!webapp.initDataUnsafe.hash) {
      webapp.showAlert('no hash!');
      return;
    }
    try {
      await login(webapp.initDataUnsafe.hash, webapp.initData).then(
        (response) => {
          token.value = response.data.jwt_token;
        }
      );
      await walletsStore.loadWallets();
      await setLanguageRequest(language.value);
    } catch (error) {
      console.error(error);
      webapp.showAlert('Backend/auth error. Please try reopening the app.');
      return;
    }

    if (inviteToken) {
      await verifyWalletLink(inviteToken.replaceAll('__', '.'))
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

  async function setLanguage(newLanguage: MessageLanguages, persist = true) {
    language.value = newLanguage;
    i18n.global.locale.value = newLanguage;
    if (persist && token.value) {
      await setLanguageRequest(newLanguage);
      await walletsStore.loadWallets();
      const { useCategories } = await import('./category');
      const { useTransaction } = await import('./transactions');
      await useCategories().loadCategories();
      await useTransaction().loadTransactions();
    }
  }

  return {
    webapp,
    showBack,
    hideBack,
    showMainButton,
    hideMainButton,
    auth,
    token,
    language,
    setLanguage,
    confirm,
    enableCloseConfirm,
    disableCloseConfirm,
    showAlert,
    mainButton,
    disableMainButton,
    enableMainButton,
    shareWallet,
  };
});
