<template>
  <div>
    <v-form v-model="valid" ref="form" lazy-validation>
      <v-text-field
        v-model="account"
        :counter="16"
        :rules="[rules.required]"
        label="用户名/邮箱"
        autofocus
      ></v-text-field>

      <v-text-field
        v-model="password"
        label="密码"
        :append-icon="showPassword ? 'visibility' : 'visibility_off'"
        :type="showPassword ? 'text' : 'password'"
        autofocus
        counter
        @click:append="showPassword = !showPassword"
      ></v-text-field>
      <v-checkbox v-model="saveToken" label="十日内免登录"></v-checkbox>
      <div class="d-flex justify-end align-center">
        <!-- <v-btn text color="teal" @click="$emit('goSignUp')">
          去注册
        </v-btn>-->
        <v-btn :disabled="!(valid && account)" color="success" class="mx-4" @click="onSubmit">登录</v-btn>
      </div>
    </v-form>
    <!-- <div>
      <a :href="getTpAuthUrl('gh', '/')">home</a>
    </div>-->
  </div>
</template>

<script>
import jwt from '@/utils/jwt.js'
import { call } from 'vuex-pathify'
import $user, { getTpAuthUrl } from '@/api/user.js'

export default {
  data: () => ({
    valid: true,
    account: '',
    rules: { required: v => !!v || '必填项' },
    password: '',
    saveToken: true,
    showPassword: false
  }),
  methods: {
    signIn: call('auth/signIn'),
    onSubmit() {
      if (!this.$refs.form.validate()) {
        return
      }
      $user
        .authenticate({
          username: this.account,
          password: this.password
        })
        .then(
          res => {
            this.signIn({
              access: res.data.access,
              refresh: res.data.refresh,
              saveToken: this.saveToken
            })
            this.$emit('success')
          },
          err => {
            console.log(err)
            this.$emit('failed', err.data.detail)
            this.$notify.error({ title: '用户或密码错误' })
          }
        )
    },
    SignIn: call('auth/SignIn'),
    getTpAuthUrl
  }
}
</script>

<style></style>
