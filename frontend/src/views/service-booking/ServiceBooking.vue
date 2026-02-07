<template>
  <div class="service-booking-container">
    <h2 class="page-title">
      <i class="fas fa-calendar-check"></i> 服务预定
    </h2>
    <el-card shadow="hover" class="service-booking-card">
      <template #header>
        <div class="card-header">
          <el-button type="primary" @click="showAddForm = true">
            <i class="fas fa-plus"></i> 添加服务预定
          </el-button>
        </div>
      </template>
      <el-table :data="bookings" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="customer_name" label="客户名称" />
        <el-table-column prop="service_type" label="服务类型" />
        <el-table-column prop="booking_date" label="预定日期" />
        <el-table-column prop="service_duration" label="服务时长" width="100">
          <template #default="scope">
            {{ scope.row.service_duration }} 小时
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editBooking(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteBooking(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑服务预定弹窗 -->
    <el-dialog
      v-model="showAddForm"
      :title="editingBooking ? '编辑服务预定' : '添加服务预定'"
      width="500px"
    >
      <div class="form-group">
        <label for="customer-name">客户名称</label>
        <select 
          class="form-control" 
          id="customer-name" 
          v-model="formData.customer_id"
          required
        >
          <option value="">请选择客户</option>
          <option v-for="customer in customers" :key="customer.id" :value="customer.id">
            {{ customer.name }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="service-item">服务项目</label>
        <select 
          class="form-control" 
          id="service-item" 
          v-model="formData.service_item_id"
          required
        >
          <option value="">请选择服务项目</option>
          <option v-for="item in serviceItems" :key="item.id" :value="item.id">
            {{ item.name }} - {{ item.price }}元
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="booking-date">预定日期</label>
        <input 
          type="date" 
          class="form-control" 
          id="booking-date" 
          v-model="formData.booking_date"
          required
        >
      </div>
      <div class="form-group">
        <label for="start-time">开始时间</label>
        <input 
          type="time" 
          class="form-control" 
          id="start-time" 
          v-model="formData.start_time"
          required
        >
      </div>
      <div class="form-group">
        <label for="status">状态</label>
        <select 
          class="form-control" 
          id="status" 
          v-model="formData.status"
          required
        >
          <option value="">请选择状态</option>
          <option value="待确认">待确认</option>
          <option value="已确认">已确认</option>
          <option value="已完成">已完成</option>
          <option value="已取消">已取消</option>
        </select>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddForm = false">取消</el-button>
          <el-button type="primary" @click="saveBooking">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const showAddForm = ref(false)
const editingBooking = ref(false)
const bookings = ref([])
const customers = ref([])
const serviceItems = ref([])
const formData = ref({
  id: null,
  customer_id: '',
  service_item_id: '',
  booking_date: '',
  start_time: '',
  status: ''
})

onMounted(() => {
  fetchBookings()
  fetchCustomers()
  fetchServiceItems()
})

const fetchBookings = async () => {
  try {
    const response = await axios.get('/api/service_bookings')
    bookings.value = response.data
  } catch (error) {
    console.error('获取服务预定列表失败:', error)
  }
}

const fetchCustomers = async () => {
  try {
    const response = await axios.get('/api/customers')
    // 只显示活跃的入住客户
    customers.value = response.data.filter(customer => customer.status === 'active')
  } catch (error) {
    console.error('获取客户列表失败:', error)
  }
}

const fetchServiceItems = async () => {
  try {
    const response = await axios.get('/api/service_items')
    serviceItems.value = response.data
  } catch (error) {
    console.error('获取服务项目列表失败:', error)
  }
}

const editBooking = (booking) => {
  editingBooking.value = true
  formData.value = { ...booking }
  showAddForm.value = true
}

const deleteBooking = async (id) => {
  try {
    await axios.delete(`/api/service_bookings/${id}`)
    fetchBookings()
  } catch (error) {
    console.error('删除服务预定失败:', error)
  }
}

const saveBooking = async () => {
  try {
    if (editingBooking.value) {
      await axios.put(`/api/service_bookings/${formData.value.id}`, formData.value)
    } else {
      await axios.post('/api/service_bookings', formData.value)
    }
    showAddForm.value = false
    fetchBookings()
    resetForm()
  } catch (error) {
    console.error('保存服务预定失败:', error)
  }
}

const resetForm = () => {
  formData.value = {
    id: null,
    customer_id: '',
    service_item_id: '',
    booking_date: '',
    start_time: '',
    status: ''
  }
  editingBooking.value = false
}

const getStatusType = (status) => {
  switch (status) {
    case '待确认':
      return 'warning'
    case '已确认':
      return 'info'
    case '已完成':
      return 'success'
    case '已取消':
      return 'danger'
    default:
      return 'info'
  }
}
</script>

<style scoped>
.service-booking-container {
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

.service-booking-card {
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

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  background-color: #fafafa;
  border-top: 1px solid #ebeef5;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
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
  .service-booking-container {
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