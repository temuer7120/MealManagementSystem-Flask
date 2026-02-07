<template>
  <div class="employee-container">
    <h2 class="page-title">
      <i class="fas fa-users"></i> 员工管理
    </h2>
    <el-card shadow="hover" class="employee-card">
      <template #header>
        <div class="card-header">
          <el-button type="primary" @click="showAddForm = true">
            <i class="fas fa-plus"></i> 添加员工
          </el-button>
        </div>
      </template>
      <el-table :data="employees" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="full_name" label="姓名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="department" label="部门" />
        <el-table-column prop="position" label="职位" />
        <el-table-column label="角色">
          <template #default="scope">
            <el-tag v-for="role in scope.row.roles" :key="role" size="small" style="margin-right: 5px;">
              {{ role }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'" size="small">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editEmployee(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteEmployee(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑员工弹窗 -->
    <el-dialog
      v-model="showAddForm"
      :title="editingEmployee ? '编辑员工' : '添加员工'"
      width="500px"
    >
      <div class="form-group">
        <label for="employee-username">用户名</label>
        <input 
          type="text" 
          class="form-control" 
          id="employee-username" 
          v-model="formData.username"
          required
        >
      </div>
      <div class="form-group" v-if="!editingEmployee">
        <label for="employee-password">密码</label>
        <input 
          type="password" 
          class="form-control" 
          id="employee-password" 
          v-model="formData.password"
          required
        >
      </div>
      <div class="form-group">
        <label for="employee-full-name">姓名</label>
        <input 
          type="text" 
          class="form-control" 
          id="employee-full-name" 
          v-model="formData.full_name"
        >
      </div>
      <div class="form-group">
        <label for="employee-email">邮箱</label>
        <input 
          type="email" 
          class="form-control" 
          id="employee-email" 
          v-model="formData.email"
        >
      </div>
      <div class="form-group">
        <label for="employee-phone">联系电话</label>
        <input 
          type="tel" 
          class="form-control" 
          id="employee-phone" 
          v-model="formData.phone"
        >
      </div>
      <div class="form-group">
        <label for="employee-department">部门</label>
        <input 
          type="text" 
          class="form-control" 
          id="employee-department" 
          v-model="formData.department"
        >
      </div>
      <div class="form-group">
        <label for="employee-position">职位</label>
        <input 
          type="text" 
          class="form-control" 
          id="employee-position" 
          v-model="formData.position"
        >
      </div>
      <div class="form-group">
        <label for="employee-is-active">状态</label>
        <select 
          class="form-control" 
          id="employee-is-active" 
          v-model="formData.is_active"
        >
          <option :value="true">启用</option>
          <option :value="false">禁用</option>
        </select>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddForm = false">取消</el-button>
          <el-button type="primary" @click="saveEmployee">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const showAddForm = ref(false)
const editingEmployee = ref(false)
const employees = ref([])
const formData = ref({
  id: null,
  username: '',
  password: '',
  full_name: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  is_active: true
})

onMounted(() => {
  fetchEmployees()
})

const fetchEmployees = async () => {
  try {
    const response = await axios.get('/api/users')
    employees.value = response.data
  } catch (error) {
    console.error('获取员工列表失败:', error)
  }
}

const editEmployee = (employee) => {
  editingEmployee.value = true
  formData.value = { ...employee }
  showAddForm.value = true
}

const deleteEmployee = async (id) => {
  try {
    await axios.delete(`/api/users/${id}`)
    fetchEmployees()
  } catch (error) {
    console.error('删除员工失败:', error)
  }
}

const saveEmployee = async () => {
  try {
    if (editingEmployee.value) {
      await axios.put(`/api/users/${formData.value.id}`, formData.value)
    } else {
      await axios.post('/api/users', formData.value)
    }
    showAddForm.value = false
    fetchEmployees()
  } catch (error) {
    console.error('保存员工失败:', error)
  }
}
</script>

<style scoped>
.employee-container {
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

.employee-card {
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
  .employee-container {
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