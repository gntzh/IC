<template>
  <v-app>
    <v-app-bar
      app
      src="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg"
      dark
      shrink-on-scroll
    >
      <template v-slot:extension>
        <v-tabs>
          <v-tab v-for="(item, idx) in tabs" :key="idx" :to="item.to">{{item.name}}</v-tab>
        </v-tabs>
      </template>

      <v-spacer></v-spacer>

      <v-btn text>
        <span>登录</span>
      </v-btn>
    </v-app-bar>

    <v-content>
      <keep-alive>
        <router-view v-if="$route.meta.keepAlive" />
      </keep-alive>
      <router-view v-if="!$route.meta.keepAlive" />
    </v-content>
  </v-app>
</template>

<script>
import jwt from '@/utils/jwt'
import $user from '@/api/user'

export default {
  name: 'App',
  components: {},
  data() {
    return {
      tabs: [
        { name: '首页', to: '/' },
        { name: '元器件', to: { name: 'Components' } },
        { name: '添加交易', to: { name: 'AddRecord' } },
        { name: '统计', to: { name: 'Statistics' } }
      ]
    }
  },
  beforeCreate() {
    if (localStorage.getItem('theme__dark') === 'true') {
      this.$vuetify.theme.dark = true
    }
    const refreshToken = localStorage.getItem('token:refresh')
    if (refreshToken) {
      const payload = jwt.decode(refreshToken)
      if (!jwt.isExpired(payload['exp'])) {
        $user.tokenRefresh(refreshToken).then(res => {
          this.$store.set('auth/signIn!', {
            saveToken: true,
            access: res.data.access
          })
        })
      } else {
        localStorage.removeItem('token:refresh')
        this.$notify({ msg: '登录过期', color: 'info' })
      }
    }
  }
}
</script>
