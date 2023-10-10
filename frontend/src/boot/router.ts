import { boot } from 'quasar/wrappers';
import { useWebApp } from 'src/stores/webapp';

export default boot(async ({ router }) => {
  router.beforeEach(async (to) => {
    const webappStore = useWebApp();

    if (to.name === 'index') {
      webappStore.hideBack();
    } else {
      console.log('SHOW');
      webappStore.showBack();
    }

    webappStore.hideMainButton()
    return true;
  });
});
