<template>
  <v-app>
    <v-app-bar
      app
      src="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg"
      dark      
    >
      <template v-slot:extension>
        <v-tabs>
          <v-tab v-for="(item, idx) in tabs" :key="idx" :to="item.to">{{item.name}}</v-tab>
        </v-tabs>
      </template>

      <v-spacer></v-spacer>
      <v-dialog v-if="!isStaff" v-model="showSignIn" max-width="500px">
        <template v-slot:activator="{ on }">
          <v-btn dark v-on="on">登录</v-btn>
        </template>
        <v-card class="pa-4">
          <sign-in-form
            @success="
                $notify({ title: '登录成功' })
                showSignIn = false
              "
          />
        </v-card>
      </v-dialog>
      <v-btn
        v-else
        @click="
            signOut()
            $notify.info({ title: '退出' })
          "
      >退出</v-btn>
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
import SignInForm from '@com/auth/SignInForm.vue'
import { sync, call } from 'vuex-pathify'

export default {
  name: 'App',
  components: { SignInForm },
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
  computed: {
    ...sync(['auth/isStaff', 'app/showSignIn'])
  },
  methods: {
    signOut: call('auth/signOut')
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
        this.$notify({ messag: '登录过期', type: 'info' })
      }
    }
  }
}
</script>
