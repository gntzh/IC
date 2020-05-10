<template>
  <div>
    <el-date-picker
      v-model="dateRange"
      type="monthrange"
      range-separator="至"
      start-placeholder="开始月份"
      end-placeholder="结束月份"
    ></el-date-picker>

    <v-radio-group v-model="by">
      <v-radio v-for="(item, i) in byOptions" :key="i" :label="item[1]" :value="item[0]"></v-radio>
    </v-radio-group>
    <el-select
      v-model="coms"
      multiple
      clearable
      filterable
      remote
      reserve-keyword
      placeholder="搜索组件"
      :remote-method="searchComs"
      :loading="comsLoading"
    >
      <el-option v-for="(com,idx) in comOptions" :key="idx" :label="com.name" :value="com.id"></el-option>
    </el-select>
    <v-btn @click="onQuery">查询</v-btn>
    <div ref="chart" style="width: 600px;height:400px;"></div>
  </div>
</template>

<script>
import $record from '@/api/record'
import $com from '@/api/component'
import { DatePicker, Select, Option } from 'element-ui'
import { format } from '@/utils/date'

export default {
  components: {
    ElOption: Option,
    ElSelect: Select,
    ElDatePicker: DatePicker
  },
  data() {
    return {
      coms: [],
      comsSearch: [],
      comsLoading: false,
      comOptions: [],
      byOptions: [
        ['month', '按月'],
        ['week', '按周']
      ],
      by: 'month',
      dateRange: null,
      chart: null,
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
      this.option.xAxis.data = []
      this.option.series[0].data = []
      this.option.series[1].data = []
      this.option.series[2].data = []
      this.option.series[3].data = []
      const params = {
        time__date__gte: format('YYYY-mm-dd', this.dateRange[0]),
        time__date__lte: format('YYYY-mm-dd', this.dateRange[1])
      }
      if (this.coms.length) params.component__in = this.coms.join()
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

          //   console.log(
          //     date,
          //     date.getFullYear(),
          //     date.getMonth() + 1,
          //     this.option.series[0].data
          //   )
          //   console.log(date)

          date.setMonth(date.getMonth() + 1)
        }
        console.log(this.option)
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