const TokenKey = 'token'

export function getToken(): string {
  const token = localStorage.getItem(TokenKey)
  if (token === null) {
    return ''
  }
  return token
}

export function setToken(token: string): void {
  localStorage.setItem(TokenKey, token)
}

export function removeToken(): void {
  localStorage.removeItem(TokenKey)
}
