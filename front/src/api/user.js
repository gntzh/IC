import http from '@/utils/http'
const BACK_URL = process.env.VUE_APP_BACK_URL
const FRONT_URL = process.env.VUE_APP_FRONT_URL

export const apiURL = 'api/'
export const tp_types = {
  gh: {
    url: 'github'
  }
}

export function getTpAuthUrl(type, now) {
  return (
    BACK_URL +
    apiURL +
    'auth/' +
    tp_types[type].url +
    `/?callback=${FRONT_URL}third_party_auth/` +
    `&state=${type + '.' + now + '.0'}`
  )
}

export default {
  authenticate(data, config) {
    return http.post(apiURL + 'token/', data, config)
  },
  tokenRefresh(refresh) {
    return http.post(apiURL + 'token/refresh/', { refresh })
  },
  signUp(data, config) {
    return http.post(apiURL + 'users/sign_up/', data, config)
  },
  tokenVerify(data, config) {
    return http.post(apiURL + 'token/verify/', data, config)
  },
  userRetrieve(pk, config) {
    return http.get(apiURL + 'users/' + pk + '/', config)
  },
  tpAuth(code, state) {
    const type = state.split('.')[0]
    return http.get(`${apiURL}auth/${tp_types[type].url}_callback/`, {
      params: {
        code,
        state
      }
    })
  }
}
