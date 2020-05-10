import http from '@/utils/http'

export const apiURL = 'api/components/'

export function list(config) {
    return http.get(apiURL, config)
}

export default { list }
