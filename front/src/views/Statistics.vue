<template>
  <div class="mt-2">
    <el-date-picker
      v-model="dateRange"
      type="monthrange"
      range-separator="至"
      start-placeholder="开始月份"
      end-placeholder="结束月份"
      class="mx-2"
    ></el-date-picker>

    <!-- <v-radio-group v-model="by">
      <v-radio v-for="(item, i) in byOptions" :key="i" :label="item[1]" :value="item[0]"></v-radio>
    </v-radio-group>-->
    <my-select ref="filterCom" item="com" class="mr-2"></my-select>
    <v-btn @click="onQuery">查询</v-btn>
    <div class="d-flex justify-center mt-4">
      <table v-show="now.money != null">
        <thead>
          <tr>
            <th>在库数量</th>
            <th>价值总额</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{now.num}}</td>
            <td>{{now.money}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="d-flex justify-center" ref="chart" style="min-height:400px;"></div>
  </div>
</template>

<script>
import $record from '@/api/record'
import $com from '@/api/component'
import { DatePicker, Select, Option } from 'element-ui'
import MySelect from '@com/Select.vue'
import { format } from '@/utils/date'

export default {
  components: {
    MySelect,
    ElDatePicker: DatePicker
  },
  data() {
    return {
      byOptions: [
        ['month', '按月'],
        ['week', '按周']
      ],
      by: 'month',
      dateRange: null,
      chart: null,
      now: {
        money: null,
        num: null
      },
      option: {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          }
        },
        xAxis: {
          name: '时间',
          type: 'category'
        },
        yAxis: [
          {
            name: '数额',
            type: 'value'
          },
          {
            name: '数量',
            type: 'value'
          }
        ],
        series: [
          {
            name: '入库数额',
            type: 'line',
            data: [],
            yAxisIndex: 0,
            smooth: true,
            itemStyle: {
              normal: {
                color: '#3888fa',
                lineStyle: {
                  color: '#3888fa',
                  width: 2
                },
                areaStyle: {
                  color: '#f3f8ff'
                }
              }
            }
          },
          {
            name: '出库数额',
            type: 'line',
            data: [],
            smooth: true,
            itemStyle: {
              normal: {
                color: '#FF005A',
                lineStyle: {
                  color: '#FF005A',
                  width: 2
                }
              }
            }
          },
          {
            name: '入库数量',
            type: 'bar',
            data: [],
            yAxisIndex: 1,
            itemStyle: {
              normal: {
                color: '#3888fa',
                lineStyle: {
                  color: '#3888fa',
                  width: 2
                },
                areaStyle: {
                  color: '#f3f8ff'
                }
              }
            }
          },
          {
            name: '出库数量',
            type: 'bar',
            data: [],
            yAxisIndex: 1,
            itemStyle: {
              normal: {
                color: '#FF005A',
                lineStyle: {
                  color: '#FF005A',
                  width: 2
                }
              }
            }
          }
        ]
      }
    }
  },
  methods: {
    onQuery() {
      this.loadData()
    },
    loadData() {
      if (!this.dateRange || !this.dateRange.length) {
        this.$notify({ title: '请先选定时间范围' })
        return
      }
      $com
        .request('sum/', {
          params: { id__in: this.$refs.filterCom.form.join() }
        })
        .then(res => {
          this.now.money = res.data.money
          this.now.num = res.data.num
        })
      this.option.xAxis.data = []
      this.option.series[0].data = []
      this.option.series[1].data = []
      this.option.series[2].data = []
      this.option.series[3].data = []
      const params = {
        time__date__gte: format('YYYY-mm-dd', this.dateRange[0]),
        time__date__lte: format('YYYY-mm-dd', this.dateRange[1])
      }
      if (this.$refs.filterCom.form.length)
        params.component__in = this.$refs.filterCom.form.join()
      $record.request(`by_${this.by}/`, { params }).then(res => {
        let date = new Date(this.dateRange[0].valueOf())
        let { input, output } = res.data
        while (
          date.getFullYear() != this.dateRange[1].getFullYear() ||
          date.getMonth() != this.dateRange[1].getMonth()
        ) {
          this.option.xAxis.data.push(
            `${date.getFullYear()}-${date.getMonth() + 1}`
          )
          if (
            input[0] &&
            input[0].time__year == date.getFullYear() &&
            input[0].time__month == date.getMonth() + 1
          ) {
            this.option.series[0].data.push(input[0].money)
            this.option.series[2].data.push(input.shift().num)
          } else {
            this.option.series[0].data.push(0)
            this.option.series[2].data.push(0)
          }
          if (
            output[0] &&
            output[0].time__year == date.getFullYear() &&
            output[0].time__month == date.getMonth() + 1
          ) {
            this.option.series[1].data.push(output[0].money)
            this.option.series[3].data.push(output.shift().num)
          } else {
            this.option.series[1].data.push(0)
            this.option.series[3].data.push(0)
          }
          date.setMonth(date.getMonth() + 1)
        }
        this.chart.setOption(this.option)
      })
    },
    searchComs(query) {
      if (query !== '') {
        this.comsLoading = true
        $com.list({ params: { search: query } }).then(res => {
          this.comsLoading = false
          this.comOptions = res.data.results
        })
      } else {
        this.comOptions = []
      }
    }
  },
  mounted() {
    require('echarts/lib/chart/line')
    require('echarts/lib/chart/bar')
    console.log(this.$refs.chart)

    this.chart = this.$echarts.init(this.$refs.chart)
    this.chart.setOption(this.option)
  },
  created() {}
}
</script>

<style>
</style>