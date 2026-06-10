/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_BASE?: string;
  readonly VITE_DEPLOY_SHA?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
