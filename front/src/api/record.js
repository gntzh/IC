import http from '@/utils/http'

export const apiURL = 'api/records/'

export function request(url, config) {
    return http({ url: apiURL + url, ...config })
}

export function createByRaw(data, config) {
    return http.post(apiURL + 'by_raw/', data, config)
}

export default { request, createByRaw }
