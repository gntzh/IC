import http from '@/utils/http'

export const apiURL = 'api/attrs/'

export function list(config) {
    return http.get(apiURL, config)
}

export function retrieve(id, config) {
    return http.get(apiURL + id + '/', config)
}

export function create(data, config) {
    return http.post(apiURL, data, config)
}

export default { list, retrieve, create }
