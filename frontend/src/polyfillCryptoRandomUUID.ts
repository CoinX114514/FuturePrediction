/**
 * 为「非安全上下文」下的 `crypto.randomUUID` 提供兼容实现。
 *
 * 设计原因：通过 `http://公网IP` 访问站点时，浏览器不提供标准的 `randomUUID`，
 * 但部分第三方库在模块初始化阶段会调用它，导致控制台报错甚至影响后续逻辑。
 * `index.html` 内已有一份同步脚本；此处作为构建产物的双保险，在入口最早 import。
 */
function patchCryptoRandomUUID(): void {
  try {
    const c = globalThis.crypto
    if (!c || typeof c.randomUUID === 'function') {
      return
    }
    c.randomUUID = function randomUUID(): `${string}-${string}-${string}-${string}-${string}` {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (ch) => {
        const r = (Math.random() * 16) | 0
        const v = ch === 'x' ? r : (r & 0x3) | 0x8
        return v.toString(16)
      }) as `${string}-${string}-${string}-${string}-${string}`
    }
  } catch {
    /* 忽略极端环境下的异常，避免阻塞应用启动 */
  }
}

patchCryptoRandomUUID()
