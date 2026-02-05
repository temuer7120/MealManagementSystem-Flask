<template>
  <div class="service-booking-container">
    <h2 class="page-title">
      <i class="fas fa-calendar-check"></i> 服务预定
    </h2>
    <div class="card">
      <div class="card-header">
        <button class="btn btn-primary" @click="showAddForm = true">
          <i class="fas fa-plus"></i> 添加服务预定
        </button>
      </div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>客户名称</th>
              <th>服务类型</th>
              <th>预定日期</th>
              <th>服务时长</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in bookings" :key="booking.id">
              <td>{{ booking.id }}</td>
              <td>{{ booking.customer_name }}</td>
              <td>{{ booking.service_type }}</td>
              <td>{{ booking.booking_date }}</td>
              <td>{{ booking.service_duration }} 小时</td>
              <td>
                <span class="badge" :class="getStatusClass(booking.status)">
                  {{ booking.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-info" @click="editBooking(booking)">
                  <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteBooking(booking.id)">
                  <i class="fas fa-trash"></i> 删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加/编辑服务预定弹窗 -->
    <el-dialog
      v-model="showAddForm"
      :title="editingBooking ? '编辑服务预定' : '添加服务预定'"
      width="500px"
    >
      <div class="form-group">
        <label for="customer-name">客户名称</label>
        <input 
          type="text" 
          class="form-control" 
          id="customer-name" 
          v-model="formData.customer_name"
          required
        >
      </div>
      <div class="form-group">
        <label for="service-type">服务类型</label>
        <select 
          class="form-control" 
          id="service-type" 
          v-model="formData.service_type"
          required
        >
          <option value="">请选择服务类型</option>
          <option value="产后护理">产后护理</option>
          <option value="新生儿护理">新生儿护理</option>
          <option value="营养咨询">营养咨询</option>
          <option value="其他服务">其他服务</option>
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
        <label for="service-duration">服务时长（小时）</label>
        <input 
          type="number" 
          class="form-control" 
          id="service-duration" 
          v-model="formData.service_duration"
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
const formData = ref({
  id: null,
  customer_name: '',
  service_type: '',
  booking_date: '',
  service_duration: 0,
  status: ''
})

onMounted(() => {
  fetchBookings()
})

const fetchBookings = async () => {
  try {
    const response = await axios.get('/api/service-bookings')
    bookings.value = response.data
  } catch (error) {
    console.error('获取服务预定列表失败:', error)
  }
}

const editBooking = (booking) => {
  editingBooking.value = true
  formData.value = { ...booking }
  showAddForm.value = true
}

const deleteBooking = async (id) => {
  try {
    await axios.delete(`/api/service-bookings/${id}`)
    fetchBookings()
  } catch (error) {
    console.error('删除服务预定失败:', error)
  }
}

const saveBooking = async () => {
  try {
    if (editingBooking.value) {
      await axios.put(`/api/service-bookings/${formData.value.id}`, formData.value)
    } else {
      await axios.post('/api/service-bookings', formData.value)
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
    customer_name: '',
    service_type: '',
    booking_date: '',
    service_duration: 0,
    status: ''
  }
  editingBooking.value = false
}

const getStatusClass = (status) => {
  switch (status) {
    case '待确认':
      return 'bg-warning text-white'
    case '已确认':
      return 'bg-info text-white'
    case '已完成':
      return 'bg-success text-white'
    case '已取消':
      return 'bg-danger text-white'
    default:
      return 'bg-secondary text-white'
  }
}
</script>

<style scoped>
.service-booking-container {
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