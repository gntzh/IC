<template>
  <div>
    <com-form></com-form>
    <v-row justify="space-around">
      <v-col cols="12" sm="3">
        <el-input placeholder="组件名称" v-model="name"></el-input>
      </v-col>
      <v-col cols="12" sm="3">
        <my-select ref="filterType" item="type"></my-select>
      </v-col>
      <v-col cols="12" sm="3">
        <my-select ref="filterAttr"></my-select>
      </v-col>
    </v-row>
    <div class="d-flex my-2">
      <v-spacer />
      <v-btn @click="loadCom(1)" class="mr-12">
        <v-icon>filter_list</v-icon>筛选
      </v-btn>
    </div>
    <com-list @edit="handleEdit" :components="components" class="mb-3 mx-4 mx-md-12 md-lg-20"></com-list>
    <v-pagination
      v-if="comCount > 5"
      v-model="comPage"
      :length="Math.ceil(comCount / 10)"
      :total-visible="7"
      @next="loadCom"
      @previous="loadCom"
      @input="loadCom"
    ></v-pagination>
    <v-dialog v-model="dialogEdit" max-width="600px">
      <com-form ref="comEdit" :id="id"></com-form>
    </v-dialog>
  </div>
</template>

<script>
import ComList from '@com/ComponentList'
import $com from '@/api/component'
import { Input } from 'element-ui'
import MySelect from '@com/Select.vue'
import AddAttr from '@com/AddAttr.vue'
import ComForm from '@com/ComForm.vue'

export default {
  components: {
    ComList,
    MySelect,
    // AddAttr,
    ElInput: Input,
    ComForm
  },
  data() {
    return {
      valid: false,
      id: null,
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
      components: [],
      comCount: 0,
      comPage: 1,
      comLoading: false,
      name: '',
      dialogType: false,
      dialogAttr: false,
      dialogEdit: false
    }
  },
  methods: {
    onSubmit() {
      console.log('cccccccc')
      const data = {
        ...this.form,
        types: this.$refs.formType.form,
        attrs: this.$refs.formAttr.form
      }
      if (this.id == null) {
        $com.create(data)
      } else {
        $com.update(this.id, data)
      }
    },
    handleEdit(row) {
      console.log(row)
      this.dialogEdit = true
      this.id = row.id
      console.log(this.id)

      this.$refs.comEdit.form.name = row.name
      this.$refs.comEdit.form.num = row.num
      this.$refs.comEdit.form.money = row.money
      this.$refs.comEdit.form.min_num = row.min_num
      this.$refs.comEdit.$refs.formAttr.form = row.attrs
      this.$refs.comEdit.$refs.formType.form = row.types
    },
    loadCom(page = 1) {
      this.comLoading = true
      const params = {
        offset: 10 * (page - 1),
        limit: 10,
        types: this.$refs.filterType.form,
        attrs: this.$refs.filterAttr.form
      }
      if (this.name) params.search = this.name
      $com.list({ params }).then(res => {
        this.components = res.data.results
        console.log(res.data)
        this.comPage = page
        this.comCount = res.data.count
        this.comLoading = false
      })
    }
  },
  computed: {
    prompt() {
      return this.id == null ? '新增' : '修改'
    }
  }
}
</script>

<style>
</style>