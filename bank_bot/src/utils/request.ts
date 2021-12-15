import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'
import { getToken, setToken } from '@/utils/auth'
import { useStore } from '@/store'
import i18n from '@/languages'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent
    const token = getToken()

    if (token.length > 0) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      // axios.defaults.headers.common['Authorization'] = getToken()

      // console.log(axios.defaults.headers.common['Authorization'])
      const header = config.headers as any
      header.Authorization = getToken();
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data

    // if the custom code is not 20000, it is judged as an error.
    if (res.code !== 0 && res.code !== 1) {
      ElMessage({
        message: res.msg || 'Error',
        type: 'error',
        duration: 5 * 1000
      })

      // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
      if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
        // to re-login
        const t = i18n.global.t
        ElMessageBox.confirm(t('message.relogin_text'), t('message.logout'), {
          confirmButtonText: t('message.relogin'),
          cancelButtonText: t('message.cancel'),
          type: 'warning'
        }).then(() => {
          setToken('')
          location.reload()
        })
      }
      return Promise.reject(new Error(res.msg || 'Error'))
    } else if (res.code == 0) {
      setToken(response.headers['authorization'])
      return res
    } else {
      return res
    }
  },
  error => {
    console.log('err' + error) // for debug
    ElMessage({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service