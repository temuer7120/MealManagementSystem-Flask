<template>
  <div class="nutrition-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>营养分析</span>
          <el-button type="primary" @click="generateNutritionReport">
            <el-icon><Document /></el-icon> 生成营养报告
          </el-button>
        </div>
      </template>
      
      <!-- 营养分析图表 -->
      <div class="nutrition-charts">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="chart-header">
                  <span>营养成分分析</span>
                </div>
              </template>
              <div id="nutritionChart" style="width: 100%; height: 400px;"></div>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="hover">
              <template #header>
                <div class="chart-header">
                  <span>营养摄入趋势</span>
                </div>
              </template>
              <div id="nutritionTrendChart" style="width: 100%; height: 400px;"></div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 营养建议 -->
      <div class="nutrition-advice" style="margin-top: 30px;">
        <el-card shadow="hover">
          <template #header>
            <div class="advice-header">
              <span>营养建议</span>
            </div>
          </template>
          <el-list>
            <el-list-item v-for="advice in nutritionAdvice" :key="advice.id">
              <template #prefix>
                <el-avatar :size="40" :type="advice.type">{{ advice.title.charAt(0) }}</el-avatar>
              </template>
              <div class="advice-content">
                <h5>{{ advice.title }}</h5>
                <p>{{ advice.content }}</p>
              </div>
            </el-list-item>
          </el-list>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 状态管理
const nutritionAdvice = ref([
  {
    id: 1,
    title: '蛋白质摄入建议',
    content: '产后妈妈每天应摄入80-100克蛋白质，以促进身体恢复和乳汁分泌。',
    type: 'primary'
  },
  {
    id: 2,
    title: '钙摄入建议',
    content: '哺乳期妈妈每天应摄入1200毫克钙，以满足自身和宝宝的需求。',
    type: 'success'
  },
  {
    id: 3,
    title: '铁摄入建议',
    content: '产后妈妈应多摄入富含铁的食物，如瘦肉、动物肝脏等，以预防贫血。',
    type: 'warning'
  },
  {
    id: 4,
    title: '维生素摄入建议',
    content: '多吃新鲜蔬菜和水果，保证维生素的充足摄入，促进身体恢复。',
    type: 'info'
  }
])

// 图表实例
let nutritionChart: echarts.ECharts | null = null
let nutritionTrendChart: echarts.ECharts | null = null

// 初始化营养成分分析图表
const initNutritionChart = () => {
  const chartDom = document.getElementById('nutritionChart')
  if (!chartDom) return
  
  nutritionChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '营养成分占比',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '营养成分',
        type: 'pie',
        radius: '50%',
        data: [
          { value: 30, name: '蛋白质' },
          { value: 25, name: '碳水化合物' },
          { value: 20, name: '脂肪' },
          { value: 15, name: '维生素' },
          { value: 10, name: '矿物质' }
        ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  nutritionChart.setOption(option)
}

// 初始化营养摄入趋势图表
const initNutritionTrendChart = () => {
  const chartDom = document.getElementById('nutritionTrendChart')
  if (!chartDom) return
  
  nutritionTrendChart = echarts.init(chartDom)
  
  const option = {
    title: {
      text: '一周营养摄入趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['蛋白质', '碳水化合物', '脂肪'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '蛋白质',
        type: 'line',
        stack: 'Total',
        data: [85, 90, 88, 92, 87, 95, 93]
      },
      {
        name: '碳水化合物',
        type: 'line',
        stack: 'Total',
        data: [150, 160, 155, 165, 158, 162, 159]
      },
      {
        name: '脂肪',
        type: 'line',
        stack: 'Total',
        data: [65, 70, 68, 72, 69, 75, 73]
      }
    ]
  }
  
  nutritionTrendChart.setOption(option)
}

// 生成营养报告
const generateNutritionReport = () => {
  ElMessage.success('营养报告生成中，稍后将下载')
  // 实现营养报告生成功能
}

// 页面加载时初始化图表
onMounted(() => {
  initNutritionChart()
  initNutritionTrendChart()
  
  // 监听窗口大小变化，调整图表大小
  window.addEventListener('resize', () => {
    nutritionChart?.resize()
    nutritionTrendChart?.resize()
  })
})

// 页面卸载时销毁图表实例
onUnmounted(() => {
  nutritionChart?.dispose()
  nutritionTrendChart?.dispose()
})
</script>

<style scoped>
.nutrition-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nutrition-charts {
  margin-bottom: 30px;
}

.chart-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.advice-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.advice-content {
  margin-left: 15px;
}

.advice-content h5 {
  margin: 0 0 5px 0;
}

.advice-content p {
  margin: 0;
  font-size: 14px;
  color: #606266;
}
</style>