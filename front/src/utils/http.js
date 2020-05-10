import axios from 'axios'
import qs from 'qs'
import jwt from '@/utils/jwt.js'
import store from '@/store'
import userApi from '@/api/user'
const BACK_URL = process.env.VUE_APP_BACK_URL


axios.defaults.timeout = 1000 * 12

axios.defaults.validateStatus = status => status >= 200 && status < 300

axios.defaults.paramsSerializer = function(params) {
  return qs.stringify(params, {
    arrayFormat: 'repeat'
  })
}

const axiosExtra = {
  setHeader(name, value, scopes = 'common') {
    for (let scope of Array.isArray(scopes) ? scopes : [scopes]) {
      if (!value) {
        delete this.defaults.headers[scope][name]
        return
      }
      this.defaults.headers[scope][name] = value
    }
  },
  setToken(token, type, scopes = 'common') {
    const value = !token ? null : (type ? type + ' ' : '') + token
    this.setHeader('Authorization', value, scopes)
  }
}

function Notification(message) {
  return message
}

let isRefreshing = false
let requests = []

function expiredTokenHandler(res) {
  const refreshToken = localStorage.getItem('token:refresh')
  if (refreshToken) {
    const config = res.config
    const payload = jwt.decode(refreshToken)
    if (!jwt.isExpired(payload['exp'])) {
      if (isRefreshing) {
        return new Promise(resolve => {
          requests.push(token => {
            config.headers.Authorization = token
            resolve(instance(config))
          })
        })
      } else {
        isRefreshing = true
        return userApi
          .tokenRefresh(refreshToken)
          .then(
            res => {
              const accessToken = res.data.access
              store.set('auth/accessToken', accessToken)
              requests.forEach(req => req(accessToken))
              requests = []
              config.headers.Authorization = accessToken
              return instance(config)
            },
            err => {
              console.error('refresh token error: ', err)
              store.set('auth/SIGN_OUT!')
            }
          )
          .finally(() => {
            isRefreshing = false
          })
      }
    } else {
      store.set('auth/SIGN_OUT!')
    }
  }
}

const errorHandle = res => {
  const { status, data } = res
  const message = data.message || data.detail || data.msg || '错误'
  switch (status) {
    case 401:
      Notification({
        title: '未登录状态，跳转登录页',
        message: message
      })
      if (res.data.code === 'token_not_valid') {
        return expiredTokenHandler(res)
      }
      break
    // FIXME Notify没有error之类的, 且这是一个占位的函数
    case 403:
      Notification.error({
        title: '登录过期，请重新登录',
        message: message
      })
      break
    case 404:
      Notification.error({
        title: '请求的资源不存在',
        message: message
      })
      break
    case 429:
      Notification.warning({
        title: '请求过于频繁',
        message: message
      })
      break
    default:
      console.log(data)
      console.log(message)
  }
}

const instance = axios.create({
  baseURL: BACK_URL
})

instance.interceptors.request.use(
  config => {
    console.log('请求配置', config)

    // const token = store.get("auth/accessToken");
    // if (token) config.headers.Authorization = "Bearer " + token;
    // config.headers.Authorization =
    //   "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc1OTcwMzk1LCJqdGkiOiI2YTZiZTZkMTRmNGQ0Yjc1ODVhYTY5NTQ2OWJiZGMxNyIsInVzZXJfaWQiOjN9.sd6XUeAgQiJ-OXFeOXm5xb3R25pklk5qNkn_L8WkZdY";
    return config
  },
  err => {
    return Promise.reject(err)
  }
)

instance.interceptors.response.use(
  // 请求成功
  res => res,
  // 请求失败
  err => {
    const { response: res } = err
    console.error('请求失败\n', res.status, '\n', res, '\n', res.data)
    let handledResult
    if (res) {
      handledResult = errorHandle(res)
    } else {
      window.localStorage.setItem('network', false)
    }
    return handledResult || Promise.reject(res)
  }
)

export { axios }
export default instance
