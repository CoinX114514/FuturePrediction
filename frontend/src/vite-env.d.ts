/// <reference types="vite/client" />

/** Vite 环境变量类型（供 import.meta.env 使用） */
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL?: string
  readonly MODE: string
  readonly DEV: boolean
  readonly PROD: boolean
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
