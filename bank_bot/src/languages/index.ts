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
        logout: 'Logout',
        relogin: 'Re-Login',
        relogin_text: 'Your token is expired. Please re-login or cancel to stay at this page.',
        cancel: 'Cancel',
        wrongpwd: 'Wrong password',
        usrn: 'Username',
        pwd: 'Password',
        sign: 'Sign in/up',
        usrtext: 'The length of username should be bewteen 4 and 32',
        pwdtext: 'The length of password should be above 8',
        hello: 'Hello! ',
        back: 'Return'
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
        logout: '确认注销',
        relogin: '重新登录',
        relogin_text: '您的登陆凭据已过期，请重新登陆，或者点击取消留在本页面',
        cancel: '取消',
        wrongpwd: '密码错误',
        usrn: '用户名',
        pwd: '密码',
        sign: '登录/注册',
        usrtext: '用户名的长度需要在4位到32位之间',
        pwdtext: '密码的长度需要在8位以上',
        hello: '你好！',
        back: '返回'
			}
		}
	}
})

export default i18n