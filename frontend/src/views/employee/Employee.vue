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
            <el-tag v-for="role in (scope.row.role ? [scope.row.role] : [])" :key="role" size="small" style="margin-right: 5px;">
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
      <el-form :model="formData" style="padding: 0 20px;">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!editingEmployee">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="formData.full_name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="部门" prop="department">
          <el-input v-model="formData.department" placeholder="请输入部门" />
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="formData.position" placeholder="请输入职位" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="formData.role" placeholder="请选择角色">
            <el-option 
              v-for="role in roles" 
              :key="role.id" 
              :label="role.name" 
              :value="role.name" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
      </el-form>
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
const roles = ref([])
const formData = ref({
  id: null,
  username: '',
  password: '',
  full_name: '',
  email: '',
  phone: '',
  department: '',
  position: '',
  role: '',
  is_active: true
})

onMounted(() => {
  fetchEmployees()
  fetchRoles()
})

const fetchEmployees = async () => {
  try {
    const response = await axios.get('/api/users')
    employees.value = response.data
  } catch (error) {
    console.error('获取员工列表失败:', error)
  }
}

const fetchRoles = async () => {
  try {
    const response = await axios.get('/api/roles')
    roles.value = response.data
  } catch (error) {
    console.error('获取角色列表失败:', error)
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