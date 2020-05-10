<template>
  <div>
    <v-row justify="space-around">
      <v-col cols="12" sm="3">
        <el-input placeholder="组件" v-model="name"></el-input>
      </v-col>
      <v-col cols="12" sm="3">
        <el-select
          v-model="types"
          multiple
          clearable
          filterable
          remote
          reserve-keyword
          placeholder="请输入类型"
          :remote-method="searchTypes"
          :loading="typesLoading"
        >
          <el-option
            v-for="(type,idx) in typeOptions"
            :key="idx"
            :label="type.name"
            :value="type.id"
          ></el-option>
        </el-select>
      </v-col>
      <v-col cols="12" sm="3">
        <el-select
          v-model="attrs"
          multiple
          clearable
          filterable
          remote
          reserve-keyword
          placeholder="请输入类型"
          :remote-method="searchAttrs"
          :loading="attrsLoading"
        >
          <el-option
            v-for="(attr,idx) in attrOptions"
            :key="idx"
            :label="attr.name"
            :value="attr.id"
          ></el-option>
        </el-select>
      </v-col>
    </v-row>
    <div class="d-flex my-2">
      <v-spacer />
      <v-btn @click="loadCom(1)" class="mr-12">
        <v-icon>filter_list</v-icon>筛选
      </v-btn>
    </div>
    <com-list :components="components" class="mb-3 mx-4 mx-md-12 md-lg-20"></com-list>
    <v-pagination
      v-if="comCount > 5"
      v-model="comPage"
      :length="Math.ceil(comCount / 10)"
      :total-visible="7"
      @next="loadCom"
      @previous="loadCom"
      @input="loadCom"
    ></v-pagination>
  </div>
</template>

<script>
import ComList from '@com/ComponentList'
import $com from '@/api/component'
import $type from '@/api/type'
import $attr from '@/api/attr'
import { Select, Option, Input } from 'element-ui'

export default {
  components: {
    ComList,
    ElOption: Option,
    ElSelect: Select,
    ElInput: Input
  },
  data() {
    return {
      components: [],
      comCount: 0,
      comPage: 1,
      comLoading: false,
      name: '',
      types: [],
      typesSearch: [],
      typesLoading: false,
      typeOptions: [],
      attrs: [],
      attrsSearch: [],
      attrsLoading: false,
      attrOptions: []
    }
  },
  created() {
    this.loadCom()
  },
  methods: {
    loadCom(page = 1) {
      this.comLoading = true
      const params = {
        offset: 10 * (page - 1),
        limit: 10,
        types: this.types,
        attrs: this.attrs
      }
      if (this.name) params.search = this.name
      $com.list({ params }).then(res => {
        this.components = res.data.results
        console.log(res.data)
        this.comPage = page
        this.comCount = res.data.count
        this.comLoading = false
      })
    },
    searchTypes(query) {
      if (query !== '') {
        this.typesLoading = true
        $type.list({ params: { search: query } }).then(res => {
          this.typesLoading = false
          this.typeOptions = res.data.results
        })
      } else {
        this.typeOptions = []
      }
    },
    searchAttrs(query) {
      if (query !== '') {
        this.attrsLoading = true
        $attr.list({ params: { search: query } }).then(res => {
          this.attrsLoading = false
          this.attrOptions = res.data.results
        })
      } else {
        this.attrOptions = []
      }
    }
  }
}
</script>

<style>
</style>