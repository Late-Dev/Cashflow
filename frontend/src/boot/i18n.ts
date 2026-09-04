import { boot } from 'quasar/wrappers';
import { createI18n } from 'vue-i18n';

import messages from 'src/i18n';

export type MessageLanguages = keyof typeof messages;
export type MessageSchema = typeof messages['en-US'];

/* eslint-disable @typescript-eslint/no-empty-interface */
declare module 'vue-i18n' {
  export interface DefineLocaleMessage extends MessageSchema {}
  export interface DefineDateTimeFormat {}
  export interface DefineNumberFormat {}
}
/* eslint-enable @typescript-eslint/no-empty-interface */

export function normalizeLocale(language?: string): MessageLanguages {
  const normalized = (language || '').toLowerCase().replace('_', '-');
  if (normalized.startsWith('ru')) return 'ru';
  if (normalized.startsWith('zh') || normalized.startsWith('cn')) return 'zh-CN';
  return 'en-US';
}

export const i18n = createI18n({
  locale: 'en-US',
  fallbackLocale: 'en-US',
  legacy: false,
  messages,
});

export default boot(({ app }) => {
  app.use(i18n);
});
