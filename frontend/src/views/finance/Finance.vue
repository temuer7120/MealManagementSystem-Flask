<template>
  <div class="finance-container">
    <h2 class="page-title">
      <i class="fas fa-money-bill-wave"></i> 财务管理
    </h2>
    <div class="card">
      <div class="card-header">
        <button class="btn btn-primary" @click="showAddForm = true">
          <i class="fas fa-plus"></i> 添加财务记录
        </button>
      </div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>交易类型</th>
              <th>金额</th>
              <th>交易日期</th>
              <th>交易描述</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="finance in finances" :key="finance.id">
              <td>{{ finance.id }}</td>
              <td>
                <span class="badge" :class="getTypeClass(finance.type)">
                  {{ finance.type }}
                </span>
              </td>
              <td>{{ finance.amount }} 元</td>
              <td>{{ finance.transaction_date }}</td>
              <td>{{ finance.description }}</td>
              <td>
                <button class="btn btn-sm btn-info" @click="editFinance(finance)">
                  <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteFinance(finance.id)">
                  <i class="fas fa-trash"></i> 删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加/编辑财务记录弹窗 -->
    <el-dialog
      v-model="showAddForm"
      :title="editingFinance ? '编辑财务记录' : '添加财务记录'"
      width="500px"
    >
      <div class="form-group">
        <label for="finance-type">交易类型</label>
        <select 
          class="form-control" 
          id="finance-type" 
          v-model="formData.type"
          required
        >
          <option value="">请选择交易类型</option>
          <option value="收入">收入</option>
          <option value="支出">支出</option>
        </select>
      </div>
      <div class="form-group">
        <label for="finance-amount">金额</label>
        <input 
          type="number" 
          class="form-control" 
          id="finance-amount" 
          v-model="formData.amount"
          required
          step="0.01"
        >
      </div>
      <div class="form-group">
        <label for="finance-date">交易日期</label>
        <input 
          type="date" 
          class="form-control" 
          id="finance-date" 
          v-model="formData.transaction_date"
          required
        >
      </div>
      <div class="form-group">
        <label for="finance-description">交易描述</label>
        <textarea 
          class="form-control" 
          id="finance-description" 
          v-model="formData.description"
          rows="3"
          required
        ></textarea>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddForm = false">取消</el-button>
          <el-button type="primary" @click="saveFinance">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const showAddForm = ref(false)
const editingFinance = ref(false)
const finances = ref([])
const formData = ref({
  id: null,
  type: '',
  amount: 0,
  transaction_date: '',
  description: ''
})

onMounted(() => {
  fetchFinances()
})

const fetchFinances = async () => {
  try {
    const response = await axios.get('/api/finances')
    finances.value = response.data
  } catch (error) {
    console.error('获取财务记录列表失败:', error)
  }
}

const editFinance = (finance) => {
  editingFinance.value = true
  formData.value = { ...finance }
  showAddForm.value = true
}

const deleteFinance = async (id) => {
  try {
    await axios.delete(`/api/finances/${id}`)
    fetchFinances()
  } catch (error) {
    console.error('删除财务记录失败:', error)
  }
}

const saveFinance = async () => {
  try {
    if (editingFinance.value) {
      await axios.put(`/api/finances/${formData.value.id}`, formData.value)
    } else {
      await axios.post('/api/finances', formData.value)
    }
    showAddForm.value = false
    fetchFinances()
  } catch (error) {
    console.error('保存财务记录失败:', error)
  }
}

const getTypeClass = (type) => {
  return type === '收入' ? 'bg-success text-white' : 'bg-danger text-white'
}
</script>

<style scoped>
.finance-container {
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
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.badge {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
}
</style>