<template>
  <el-select
    v-model="form"
    multiple
    clearable
    filterable
    remote
    reserve-keyword
    :placeholder="'请输入'+prompt"
    :remote-method="searchAttrs"
    :loading="itemsLoading"
  >
    <el-option v-for="(item,idx) in itemOptions" :key="idx" :label="item.name" :value="item.id"></el-option>
  </el-select>
</template>

<script>
import $type from '@/api/type'
import $attr from '@/api/attr'
import $com from '@/api/component'
import { Select, Option } from 'element-ui'

export default {
  components: {
    ElOption: Option,
    ElSelect: Select
  },
  props: {
    item: {
      type: String,
      default: 'attr'
    }
  },
  data() {
    return {
      form: [],
      itemsSearch: [],
      itemsLoading: false,
      itemOptions: [],
      apis: {
        $type,
        $attr,
        $com
      }
    }
  },
  methods: {
    searchAttrs(query) {
      console.log(this.item, this.apis['$' + this.item])

      if (query !== '') {
        this.itemsLoading = true
        this.apis['$' + this.item]
          .list({ params: { search: query } })
          .then(res => {
            this.itemsLoading = false
            this.itemOptions = res.data.results
          })
      } else {
        this.itemOptions = []
      }
    }
  },
  computed: {
    prompt() {
      if (this.item == 'attr') return '属性'
      else if (this.item == 'type') return '类型'
      else return '组件名称'
    }
  }
}
</script>

<style>
</style>