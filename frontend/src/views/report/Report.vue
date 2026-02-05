<template>
  <div class="report-container">
    <h2 class="page-title">
      <i class="fas fa-file-invoice"></i> 报表打印
    </h2>
    <div class="card">
      <div class="card-header">
        <div class="form-group">
          <label for="report-type">选择报表类型</label>
          <select 
            class="form-control" 
            id="report-type" 
            v-model="selectedReportType"
            @change="generateReport"
          >
            <option value="">请选择报表类型</option>
            <option value="order">订单报表</option>
            <option value="finance">财务报表</option>
            <option value="customer">客户报表</option>
            <option value="employee">员工报表</option>
          </select>
        </div>
      </div>
      <div class="card-body">
        <div v-if="loading" class="loading">
          <i class="fas fa-spinner fa-spin"></i> 正在生成报表...
        </div>
        <div v-else-if="reportData.length > 0" class="report-content">
          <h3>{{ getReportTitle(selectedReportType) }}</h3>
          <div class="report-header">
            <p>生成日期: {{ new Date().toLocaleDateString() }}</p>
            <p>上海巍阁公司管理系统</p>
          </div>
          <table class="table table-striped">
            <thead>
              <tr>
                <th v-for="column in getReportColumns(selectedReportType)" :key="column">
                  {{ column }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in reportData" :key="index">
                <td v-for="column in getReportColumns(selectedReportType)" :key="column">
                  {{ getItemValue(item, column) }}
                </td>
              </tr>
            </tbody>
          </table>
          <div class="report-footer">
            <p>报表生成完毕</p>
          </div>
          <div class="mt-4 text-center">
            <button class="btn btn-primary" @click="printReport">
              <i class="fas fa-print"></i> 打印报表
            </button>
          </div>
        </div>
        <div v-else class="empty-state">
          <i class="fas fa-file-invoice fa-3x"></i>
          <p>请选择报表类型生成报表</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const selectedReportType = ref('')
const reportData = ref([])
const loading = ref(false)

const generateReport = async () => {
  if (!selectedReportType.value) {
    reportData.value = []
    return
  }

  loading.value = true
  try {
    let response
    switch (selectedReportType.value) {
      case 'order':
        response = await axios.get('/api/orders')
        break
      case 'finance':
        response = await axios.get('/api/finances')
        break
      case 'customer':
        response = await axios.get('/api/customers')
        break
      case 'employee':
        response = await axios.get('/api/employees')
        break
      default:
        reportData.value = []
        return
    }
    reportData.value = response.data
  } catch (error) {
    console.error('生成报表失败:', error)
    reportData.value = []
  } finally {
    loading.value = false
  }
}

const getReportTitle = (type) => {
  switch (type) {
    case 'order':
      return '订单报表'
    case 'finance':
      return '财务报表'
    case 'customer':
      return '客户报表'
    case 'employee':
      return '员工报表'
    default:
      return '报表'
  }
}

const getReportColumns = (type) => {
  switch (type) {
    case 'order':
      return ['订单ID', '客户姓名', '订单金额', '订单日期', '订单状态']
    case 'finance':
      return ['交易ID', '交易类型', '金额', '交易日期', '交易描述']
    case 'customer':
      return ['客户ID', '客户姓名', '联系电话', '入住日期', '会员等级']
    case 'employee':
      return ['员工ID', '员工姓名', '工号', '职位', '联系电话', '入职日期']
    default:
      return []
  }
}

const getItemValue = (item, column) => {
  switch (column) {
    case '订单ID':
      return item.id || ''
    case '客户姓名':
      return item.customer_name || item.name || ''
    case '订单金额':
      return item.amount || ''
    case '订单日期':
      return item.order_date || ''
    case '订单状态':
      return item.status || ''
    case '交易ID':
      return item.id || ''
    case '交易类型':
      return item.type || ''
    case '金额':
      return item.amount || ''
    case '交易日期':
      return item.transaction_date || ''
    case '交易描述':
      return item.description || ''
    case '客户ID':
      return item.id || ''
    case '联系电话':
      return item.phone || ''
    case '入住日期':
      return item.check_in_date || ''
    case '会员等级':
      return item.member_level || ''
    case '员工ID':
      return item.id || ''
    case '工号':
      return item.employee_id || ''
    case '职位':
      return item.position || ''
    case '入职日期':
      return item.hire_date || ''
    default:
      return ''
  }
}

const printReport = () => {
  window.print()
}
</script>

<style scoped>
.report-container {
  padding: 20px;
}

.page-title {
  color: var(--primary-color);
  margin-bottom: 20px;
  font-weight: bold;
}

.card {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  background-color: var(--primary-color);
  color: white;
  padding: 15px;
}

.card-body {
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

.btn-primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.btn-primary:hover {
  background-color: var(--primary-color);
  opacity: 0.9;
  border-color: var(--primary-color);
}

.loading {
  text-align: center;
  padding: 40px;
  color: var(--primary-color);
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.report-content {
  margin-top: 20px;
}

.report-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ddd;
}

.report-footer {
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #ddd;
  text-align: right;
}

@media print {
  .card-header,
  .mt-4 {
    display: none;
  }
  
  .card {
    box-shadow: none;
    border: none;
  }
}
</style>