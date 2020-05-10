<template>
  <div>
    <v-row justify="center">
      <v-col cols="11" sm="5" md="4">
        <v-form v-model="valid">
          <v-text-field label="组件" v-model="form.component" :rules="[rules.notNull]"></v-text-field>
          <v-text-field label="交易数量" v-model="form.num" :rules="[rules.notNull, rules.isPosInt]"></v-text-field>
          <v-text-field label="交易金额" v-model="form.money" :rules="[rules.notNull, rules.isFloat]"></v-text-field>
        </v-form>
      </v-col>
      <v-col cols="11" sm="5" md="4">
        <div class="mb-2">
          <span class="font-weight-bold">交易时间：</span>
          <date-picker v-model="form.time" type="datetime" placeholder="选择日期时间"></date-picker>
        </div>
        <v-radio-group v-model="form.operation">
          <v-radio v-for="(item, i) in operations" :key="i" :label="item[1]" :value="item[0]"></v-radio>
        </v-radio-group>

        <div class="d-flex align-self-end">
          <v-spacer />
          <v-btn :disabled="!(valid && form.time)" color="success" @click="onSubmit">提交</v-btn>
        </div>
      </v-col>
    </v-row>
    <div class="d-flex justify-center">
      <table v-if="last.id">
        <thead>
          <tr>
            <th>交易</th>
            <th>交易时间</th>
            <th>组件</th>
            <th>金额</th>
            <th>数量</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ last.operation==1?'入库':'出库'}}</td>
            <td>{{ last.time }}</td>
            <td>{{ last.component_detail.name }}</td>
            <td>{{ last.money }}</td>
            <td>{{ last.num }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { DatePicker } from 'element-ui'
import { sync } from 'vuex-pathify'
import { createByRaw } from '@/api/record'

export default {
  components: { DatePicker },
  data() {
    return {
      rules: {
        notNull: v => Boolean(v) || '此处不能为空',
        isFloat: v => {
          const pattern = /^\d+(\.\d+)?$/
          return pattern.test(v) || '请输入有效正数'
        },
        isPosInt: v => {
          const pattern = /^\d+$/
          return pattern.test(v) || '请输入有效正整数'
        }
      },
      operations: [
        [1, '入库'],
        [-1, '出库']
      ],
      valid: false,
      last: {
        id: null,
        operation: null,
        component_detail: { name: null, money: 0 },
        num: '0',
        money: '0',
        time: ''
      }
    }
  },
  computed: {
    form: sync('record/addForm')
  },
  methods: {
    onSubmit() {
      console.log(this.$store.state.record.addForm)
      createByRaw(this.form).then(res => {
        this.last = res.data
      })
    }
    // loadCom(id, page = 1) {
    //   this.commentLoading = true
    //   comApi
    //     .list({ params: { post: id, offset: 5 * (page - 1), limit: 5 } })
    //     .then(res => {
    //       this.rootComments = res.data.results
    //       this.commentCount = res.data.count
    //       this.commentLoading = false
    //     })
    // },
  }
}
</script>

<style>
</style>