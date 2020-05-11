<template>
  <v-row justify="center" class="white">
    <v-col cols="11" sm="5" md="4">
      <v-form v-model="valid">
        <v-text-field label="组件名称" v-model="form.name" :rules="[rules.notNull]"></v-text-field>
        <v-text-field label="在库数量" v-model="form.num" :rules="[rules.notNull, rules.isPosInt]"></v-text-field>
        <v-text-field label="价值金额" v-model="form.money" :rules="[rules.notNull, rules.isFloat]"></v-text-field>
        <v-text-field label="库存警告" v-model="form.min_num" :rules="[rules.notNull, rules.isPosInt]"></v-text-field>
      </v-form>
    </v-col>
    <v-col cols="11" sm="5" md="4">
      <div class="mb-2">
        <my-select ref="formType" item="type"></my-select>
        <v-dialog v-model="dialogType" max-width="600px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" icon v-on="on">
              <v-icon>add</v-icon>
            </v-btn>
          </template>
          <add-attr item="type"></add-attr>
        </v-dialog>
      </div>
      <div class="mb-2">
        <my-select ref="formAttr" item="attr"></my-select>
        <v-dialog v-model="dialogAttr" max-width="600px">
          <template v-slot:activator="{ on }">
            <v-btn color="primary" icon v-on="on">
              <v-icon>add</v-icon>
            </v-btn>
          </template>
          <add-attr></add-attr>
        </v-dialog>
      </div>
      <div class="d-flex align-self-end">
        <v-spacer />
        <v-btn
          class="mr-2"
          :disabled="!(valid && form.name)"
          color="success"
          @click="onSubmit"
        >{{ id == null?'新建':'修改' }}</v-btn>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import MySelect from '@com/Select.vue'
import AddAttr from '@com/AddAttr.vue'
import $com from '@/api/component'

export default {
  components: {
    MySelect,
    AddAttr
  },
  props: {
    id: {
      default: null
    }
  },
  data() {
    return {
      valid: false,
      form: {
        name: '',
        money: '',
        num: '',
        min_num: ''
      },
      rules: {
        notNull: v => Boolean(v.length) || '此处不能为空',
        isFloat: v => {
          const pattern = /^\d+(\.\d+)?$/
          return pattern.test(v) || '请输入有效正数'
        },
        isPosInt: v => {
          const pattern = /^\d+$/
          return pattern.test(v) || '请输入有效正整数'
        }
      },
      dialogType: false,
      dialogAttr: false
    }
  },
  methods: {
    onSubmit() {
      const data = {
        ...this.form,
        types: this.$refs.formType.form,
        attrs: this.$refs.formAttr.form
      }
      if (this.id == null) {
        $com.create(data).then(
          res => this.$notify({ title: '成功' }),
          err => this.$notify({ title: '已存在', type: 'error' })
        )
      } else {
        $com.update(this.id, data).then(
          res => this.$notify({ title: '成功' }),
          err => this.$notify({ title: '失败', type: 'error' })
        )
      }
    }
  }
}
</script>

<style>
</style>