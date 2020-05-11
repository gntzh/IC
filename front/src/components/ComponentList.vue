<template>
  <div>
    <el-table :data="components" stripe :row-class-name="tableRowClassName">
      <el-table-column prop="id" label="编号"></el-table-column>
      <el-table-column prop="name" label="组件"></el-table-column>
      <el-table-column prop="num" label="库存"></el-table-column>
      <el-table-column label="类型">
        <template slot-scope="scope">
          <v-chip
            class="mr-1 mb-1"
            color="cyan lighten-5"
            text-color="cyan"
            small
            label
            v-for="(type, idx) in scope.row.types_detail"
            :key="idx"
          >{{ type.name }}</v-chip>
        </template>
      </el-table-column>
      <el-table-column label="属性">
        <template slot-scope="scope">
          <v-chip
            class="ma-1 ma-sm-2"
            color="cyan lighten-5"
            text-color="cyan"
            small
            label
            v-for="(type, idx) in scope.row.attrs_detail"
            :key="idx"
          >{{ type.name }}</v-chip>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="60">
        <template slot-scope="scope">
          <el-button @click="$emit('edit', scope.row)" type="text" size="small">编辑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { Table, TableColumn } from 'element-ui'

export default {
  components: { ElTable: Table, ElTableColumn: TableColumn },
  props: {
    components: Array
  },
  methods: {
    tableRowClassName({ row }) {
      if (row.num <= row.min_num) {
        return 'warning'
      }
      return ''
    }
  }
}
</script>

<style>
</style>