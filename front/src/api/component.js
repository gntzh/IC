import http from '@/utils/http'

export const apiURL = 'api/components/'

export function request(url, config) {
    return http({ url: apiURL + url, ...config })
}

export function list(config) {
    return http.get(apiURL, config)
}

export function create(data, config) {
    return http.post(apiURL, data, config)
}

export function update(id, data, config) {
    return http.put(apiURL + id + '/', data, config)
}


export default { request, list, create, update }
