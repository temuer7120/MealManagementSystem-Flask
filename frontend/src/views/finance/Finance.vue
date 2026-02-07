<template>
  <div class="finance-container">
    <h2 class="page-title">
      <i class="fas fa-money-bill-wave"></i> 财务管理
    </h2>
    <el-card shadow="hover" class="finance-card">
      <template #header>
        <div class="card-header">
          <el-button type="primary" @click="showAddForm = true">
            <i class="fas fa-plus"></i> 添加财务记录
          </el-button>
        </div>
      </template>
      <el-table :data="finances" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="type" label="交易类型" width="100">
          <template #default="scope">
            <el-tag :type="getTypeType(scope.row.type)">
              {{ scope.row.type }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" width="100">
          <template #default="scope">
            {{ scope.row.amount }} 元
          </template>
        </el-table-column>
        <el-table-column prop="transaction_date" label="交易日期" />
        <el-table-column prop="description" label="交易描述" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editFinance(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteFinance(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

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

const getTypeType = (type) => {
  return type === '收入' ? 'success' : 'danger'
}
</script>

<style scoped>
.finance-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--primary-color);
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-title i {
  font-size: 24px;
}

.finance-card {
  margin-bottom: 24px;
  border-radius: 8px;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 20px;
  background-color: #fafafa;
  border-bottom: 1px solid #ebeef5;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  background-color: #fafafa;
  border-top: 1px solid #ebeef5;
}

/* 确保Element Plus按钮与全局样式一致 */
.el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.el-button--primary:hover {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  opacity: 0.9;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .finance-container {
    padding: 12px;
  }
  
  .page-title {
    font-size: 18px;
  }
  
  .el-dialog {
    width: 90% !important;
  }
}
</style>