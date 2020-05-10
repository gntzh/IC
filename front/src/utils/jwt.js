export default {
  decode(token) {
    return JSON.parse(
      decodeURIComponent(escape(window.atob(token.split('.')[1])))
    )
  },
  isExpired(time) {
    const date = new Date()
    return date.getTime() > time * 1000
  }
}
