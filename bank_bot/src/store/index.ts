import { defineStore } from 'pinia'

export const useStore = defineStore({
  id: 'setting',
  state: () =>({
		lang: 'zh',
		token: ''
  }),
  getters: {},
  actions: {}
})