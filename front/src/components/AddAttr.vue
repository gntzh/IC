<template>
  <div class="white pa-2">
    <v-text-field label="名称" v-model="form.name" :rules="[v => Boolean(v) || '此处不能为空']"></v-text-field>
    <div class="d-flex">
      <v-spacer />
      <v-btn right color="blue" @click="onSubmit">新增</v-btn>
    </div>
  </div>
</template>

<script>
import { create as $attr } from '@/api/attr'
import { create as $type } from '@/api/type'

export default {
  props: { item: { type: String, default: 'attr' } },
  data() {
    return {
      form: { name: '' },
      api: {
        $attr,
        $type
      }
    }
  },
  methods: {
    onSubmit() {
      this.api['$' + this.item](this.form).then(res =>
        this.$notify({ title: '成功' }).catch(err => {
          this.$notify({ title: '类型存在' })
        })
      )
    }
  }
}
</script>

<style>
</style>