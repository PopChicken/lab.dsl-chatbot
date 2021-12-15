import { useStore } from '@/store'

export function getToken(): string {
  const store = useStore();
  const token = store.$state.token
  if (token === null) {
    return ''
  }
  return token
}

export function setToken(token: string): void {
  const store = useStore();
  store.$state.token = token
}

export function removeToken(): void {
  const store = useStore();
  store.$state.token = ''
}

// const TokenKey = 'token'

// export function getToken(): string {
//   const token = localStorage.getItem(TokenKey)
//   if (token === null) {
//     return ''
//   }
//   return token
// }

// export function setToken(token: string): void {
//   localStorage.setItem(TokenKey, token)
// }

// export function removeToken(): void {
//   localStorage.removeItem(TokenKey)
// }