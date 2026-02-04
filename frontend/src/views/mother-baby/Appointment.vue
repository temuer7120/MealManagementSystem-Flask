<template>
  <div class="appointment-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>服务预约</span>
          <el-button type="primary" @click="openAppointmentForm">
            <el-icon><Plus /></el-icon> 新增预约
          </el-button>
        </div>
      </template>
      
      <!-- 服务项目列表 -->
      <div class="service-categories">
        <h3>服务项目分类</h3>
        <el-row :gutter="20">
          <el-col :span="8" v-for="category in categories" :key="category.id">
            <el-card :body-style="{ padding: '0px' }">
              <div class="category-card">
                <div class="category-header">
                  <h4>{{ category.name }}</h4>
                  <p>{{ category.description }}</p>
                </div>
                <div class="service-items">
                  <el-collapse v-model="activeCategory">
                    <el-collapse-item :title="'查看服务项目'" :name="category.id">
                      <el-list>
                        <el-list-item v-for="item in category.items" :key="item.id">
                          <template #prefix>
                            <el-avatar :size="40" :src="item.image_url || ''">{{ item.name.charAt(0) }}</el-avatar>
                          </template>
                          <div class="service-item-info">
                            <h5>{{ item.name }}</h5>
                            <p>{{ item.description }}</p>
                            <div class="service-item-meta">
                              <span class="duration">{{ item.duration_minutes }}分钟</span>
                              <span class="price">¥{{ item.price }}</span>
                            </div>
                          </div>
                          <template #suffix>
                            <el-button type="primary" size="small" @click="bookService(item)">
                              预约
                            </el-button>
                          </template>
                        </el-list-item>
                      </el-list>
                    </el-collapse-item>
                  </el-collapse>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
      
      <!-- 预约记录 -->
      <div class="appointment-records" style="margin-top: 40px;">
        <h3>预约记录</h3>
        <el-table :data="appointments" style="width: 100%">
          <el-table-column prop="id" label="预约ID" width="80" />
          <el-table-column prop="service_item_name" label="服务项目" />
          <el-table-column prop="appointment_time" label="预约时间" />
          <el-table-column prop="status" label="状态" />
          <el-table-column label="操作" width="150">
            <template #default="scope">
              <el-button type="primary" size="small" @click="editAppointment(scope.row)">
                编辑
              </el-button>
              <el-button type="danger" size="small" @click="cancelAppointment(scope.row.id)">
                取消
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
    
    <!-- 预约表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="服务预约"
      width="500px"
    >
      <el-form :model="appointmentForm" :rules="rules" ref="formRef">
        <el-form-item label="服务项目" prop="service_item_id">
          <el-select v-model="appointmentForm.service_item_id" placeholder="选择服务项目">
            <el-option
              v-for="item in allServiceItems"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="预约日期" prop="appointment_date">
          <el-date-picker
            v-model="appointmentForm.appointment_date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预约时间" prop="appointment_time">
          <el-time-picker
            v-model="appointmentForm.appointment_time"
            placeholder="选择时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="appointmentForm.notes"
            type="textarea"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitAppointment">确认预约</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'

// 状态管理
const categories = ref<any[]>([])
const appointments = ref<any[]>([])
const activeCategory = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)

// 预约表单
const appointmentForm = ref({
  service_item_id: '',
  appointment_date: '',
  appointment_time: '',
  notes: ''
})

// 表单验证规则
const rules = ref({
  service_item_id: [{ required: true, message: '请选择服务项目', trigger: 'change' }],
  appointment_date: [{ required: true, message: '请选择预约日期', trigger: 'change' }],
  appointment_time: [{ required: true, message: '请选择预约时间', trigger: 'change' }]
})

// 计算所有服务项目
const allServiceItems = computed(() => {
  return categories.value.flatMap(category => category.items || [])
})

// 获取服务分类和项目
const fetchServiceCategories = async () => {
  try {
    const response = await axios.get('/api/service_categories')
    const categoryList = response.data
    
    // 为每个分类获取服务项目
    for (const category of categoryList) {
      const itemsResponse = await axios.get(`/api/service_items?category_id=${category.id}`)
      category.items = itemsResponse.data
    }
    
    categories.value = categoryList
  } catch (error) {
    ElMessage.error('获取服务分类失败')
    console.error('Error fetching service categories:', error)
  }
}

// 获取预约记录
const fetchAppointments = async () => {
  try {
    const response = await axios.get('/api/appointments')
    appointments.value = response.data
  } catch (error) {
    ElMessage.error('获取预约记录失败')
    console.error('Error fetching appointments:', error)
  }
}

// 打开预约表单
const openAppointmentForm = () => {
  appointmentForm.value = {
    service_item_id: '',
    appointment_date: '',
    appointment_time: '',
    notes: ''
  }
  dialogVisible.value = true
}

// 提交预约
const submitAppointment = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 合并日期和时间
        const appointmentDateTime = new Date(`${appointmentForm.value.appointment_date} ${appointmentForm.value.appointment_time}`)
        
        const response = await axios.post('/api/appointments', {
          service_item_id: appointmentForm.value.service_item_id,
          appointment_time: appointmentDateTime.toISOString(),
          notes: appointmentForm.value.notes
        })
        
        ElMessage.success('预约成功')
        dialogVisible.value = false
        fetchAppointments()
      } catch (error) {
        ElMessage.error('预约失败')
        console.error('Error submitting appointment:', error)
      }
    }
  })
}

// 预约服务项目
const bookService = (item: any) => {
  appointmentForm.value.service_item_id = item.id
  dialogVisible.value = true
}

// 编辑预约
const editAppointment = (appointment: any) => {
  // 实现编辑预约功能
  ElMessage.info('编辑预约功能开发中')
}

// 取消预约
const cancelAppointment = (appointmentId: number) => {
  ElMessageBox.confirm('确定要取消该预约吗？', '取消预约', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await axios.delete(`/api/appointments/${appointmentId}`)
      ElMessage.success('预约已取消')
      fetchAppointments()
    } catch (error) {
      ElMessage.error('取消预约失败')
      console.error('Error canceling appointment:', error)
    }
  })
}

// 页面加载时获取数据
onMounted(() => {
  fetchServiceCategories()
  fetchAppointments()
})
</script>

<style scoped>
.appointment-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.service-categories {
  margin-bottom: 30px;
}

.category-card {
  height: 100%;
}

.category-header {
  padding: 15px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e4e7ed;
}

.category-header h4 {
  margin: 0 0 5px 0;
}

.category-header p {
  margin: 0;
  font-size: 14px;
  color: #606266;
}

.service-items {
  padding: 15px;
}

.service-item-info {
  flex: 1;
  margin-left: 15px;
}

.service-item-info h5 {
  margin: 0 0 5px 0;
}

.service-item-info p {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #606266;
}

.service-item-meta {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.duration {
  color: #409eff;
}

.price {
  color: #f56c6c;
  font-weight: bold;
}

.appointment-records {
  margin-top: 30px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>