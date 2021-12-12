import { createI18n } from 'vue-i18n'

const i18n = createI18n({
	locale: navigator.language,
	messages: {
		'en-US': {
			message: {
        cp: 'Control Panel',
        sel_schema: 'Select a schema',
        confirm: 'Confirm',
        lang: 'Language',
        service_err: 'Fail to connect the server. Please refresh.',
        expire: 'Session expired. Make sure Cookie is enabled.',
        error: 'Network error',
			}
		},
		'zh': {
			message: {
				cp: '控制台',
				sel_schema: '选择一个方案',
				confirm: '确认',
				lang: '语言',
				service_err: '连接服务器失败，请刷新重试',
				expire: '会话过期，请确保允许cookie，并刷新页面。',
				error: '网络异常',
			}
		}
	}
})

export default i18n