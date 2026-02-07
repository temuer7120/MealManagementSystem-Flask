<template>
  <div class="customer-container">
    <h2 class="page-title">
      <i class="fas fa-user-friends"></i> 客户管理
    </h2>
    <!-- 客户列表 -->
    <el-card shadow="hover" class="customer-card">
      <template #header>
        <div class="card-header">
          <span>客户列表</span>
          <el-button type="primary" @click="openCustomerForm">
            <el-icon><Plus /></el-icon> 新增客户
          </el-button>
        </div>
      </template>
      
      <el-table :data="customers" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="客户姓名" />
        <el-table-column prop="phone" label="联系电话" width="150" />
        <el-table-column prop="email" label="邮箱" width="200" />
        <el-table-column prop="check_in_date" label="入住日期" width="150" />
        <el-table-column prop="check_out_date" label="退房日期" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editCustomer(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteCustomer(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 客户表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="客户管理"
      width="500px"
    >
      <el-form :model="customerForm" :rules="rules" ref="formRef">
        <el-form-item label="客户姓名" prop="name">
          <el-input v-model="customerForm.name" placeholder="请输入客户姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="customerForm.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="customerForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="入住日期" prop="check_in_date">
          <el-date-picker
            v-model="customerForm.check_in_date"
            type="date"
            placeholder="选择入住日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="退房日期" prop="check_out_date">
          <el-date-picker
            v-model="customerForm.check_out_date"
            type="date"
            placeholder="选择退房日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="customerForm.status" placeholder="请选择状态">
            <el-option label="在住" value="在住" />
            <el-option label="已退房" value="已退房" />
            <el-option label="预订" value="预订" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCustomer">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const customers = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)

const customerForm = ref({
  id: '',
  name: '',
  phone: '',
  email: '',
  check_in_date: '',
  check_out_date: '',
  status: '在住'
})

const rules = ref({
  name: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  check_in_date: [{ required: true, message: '请选择入住日期', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
})

const getStatusType = (status: string) => {
  switch (status) {
    case '在住':
      return 'success'
    case '已退房':
      return 'info'
    case '预订':
      return 'warning'
    default:
      return 'default'
  }
}

const fetchCustomers = async () => {
  try {
    // 从后端API获取客户列表
    const response = await axios.get('/api/customers')
    customers.value = response.data
  } catch (error) {
    console.error('Error fetching customers:', error)
    ElMessage.error('获取客户列表失败')
  }
}

const openCustomerForm = () => {
  customerForm.value = {
    id: '',
    name: '',
    phone: '',
    email: '',
    check_in_date: '',
    check_out_date: '',
    status: '在住'
  }
  dialogVisible.value = true
}

const editCustomer = (customer: any) => {
  customerForm.value = { ...customer }
  dialogVisible.value = true
}

const deleteCustomer = (customerId: number) => {
  ElMessageBox.confirm('确定要删除该客户吗？', '删除客户', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 调用后端API删除客户
      await axios.delete(`/api/customers/${customerId}`)
      // 从本地列表中移除
      customers.value = customers.value.filter(customer => customer.id !== customerId)
      ElMessage.success('客户删除成功')
    } catch (error) {
      console.error('Error deleting customer:', error)
      ElMessage.error('删除客户失败')
    }
  })
}

const submitCustomer = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (customerForm.value.id) {
          // 编辑客户
          await axios.put(`/api/customers/${customerForm.value.id}`, customerForm.value)
          ElMessage.success('客户更新成功')
        } else {
          // 新增客户
          await axios.post('/api/customers', customerForm.value)
          ElMessage.success('客户创建成功')
        }
        dialogVisible.value = false
        // 重新获取客户列表
        await fetchCustomers()
      } catch (error) {
        console.error('Error submitting customer:', error)
        ElMessage.error('保存客户失败')
      }
    }
  })
}

onMounted(() => {
  fetchCustomers()
})
</script>

<style scoped>
.customer-container {
  padding: 20px;
}

.customer-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>