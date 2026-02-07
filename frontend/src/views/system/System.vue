<template>
  <div class="system-container">
    <h2>系统设置</h2>
    <!-- 系统设置选项卡 -->
    <el-tabs v-model="activeTab" class="system-tabs">
      <el-tab-pane label="用户管理" name="users">
        <el-card shadow="hover" class="system-card">
          <template #header>
            <div class="card-header">
              <span>用户列表</span>
              <el-button type="primary" @click="openUserForm">
                <el-icon><Plus /></el-icon> 新增用户
              </el-button>
            </div>
          </template>
          
          <el-table :data="users" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="email" label="邮箱" width="200" />
            <el-table-column prop="role" label="角色" width="120">
              <template #default="scope">
                <el-tag :type="getRoleType(scope.row.role)">
                  {{ scope.row.role }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="is_active" label="状态" width="100">
              <template #default="scope">
                <el-switch v-model="scope.row.is_active" @change="updateUserStatus(scope.row)" />
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editUser(scope.row)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="deleteUser(scope.row.id)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="角色管理" name="roles">
        <el-card shadow="hover" class="system-card">
          <template #header>
            <div class="card-header">
              <span>角色列表</span>
              <el-button type="primary" @click="openRoleForm">
                <el-icon><Plus /></el-icon> 新增角色
              </el-button>
            </div>
          </template>
          
          <el-table :data="roles" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="角色名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editRole(scope.row)">
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click="deleteRole(scope.row.id)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="权限管理" name="permissions">
        <el-card shadow="hover" class="system-card">
          <template #header>
            <div class="card-header">
              <span>权限列表</span>
            </div>
          </template>
          
          <el-table :data="permissions" style="width: 100%">
            <el-table-column prop="name" label="权限名称" width="150" />
            <el-table-column prop="code" label="权限代码" width="150" />
            <el-table-column prop="module" label="模块" width="120" />
            <el-table-column prop="description" label="描述" />
          </el-table>
        </el-card>
      </el-tab-pane>
      
      <el-tab-pane label="系统信息" name="info">
        <el-card shadow="hover" class="system-card">
          <template #header>
            <div class="card-header">
              <span>系统信息</span>
            </div>
          </template>
          
          <div class="system-info">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="系统版本">1.0.0</el-descriptions-item>
              <el-descriptions-item label="后端API地址">http://127.0.0.1:5000/api</el-descriptions-item>
              <el-descriptions-item label="数据库类型">MySQL</el-descriptions-item>
              <el-descriptions-item label="前端框架">Vue 3 + Element Plus</el-descriptions-item>
              <el-descriptions-item label="最后更新时间">2026-02-04</el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 用户表单对话框 -->
    <el-dialog
      v-model="userDialogVisible"
      title="用户管理"
      width="500px"
    >
      <el-form :model="userForm" :rules="userRules" ref="userFormRef">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!userForm.id">
          <el-input
            v-model="userForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option 
              v-for="role in roles" 
              :key="role.id" 
              :label="role.name" 
              :value="role.name" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="userForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="userDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUser">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 角色表单对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      title="角色管理"
      width="500px"
    >
      <el-form :model="roleForm" :rules="roleRules" ref="roleFormRef">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="roleForm.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="roleForm.description"
            type="textarea"
            placeholder="请输入角色描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="roleDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitRole">保存</el-button>
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

const activeTab = ref('users')
const users = ref<any[]>([])
const roles = ref<any[]>([])
const permissions = ref<any[]>([])
const userDialogVisible = ref(false)
const roleDialogVisible = ref(false)
const userFormRef = ref<any>(null)
const roleFormRef = ref<any>(null)

const userForm = ref({
  id: '',
  username: '',
  email: '',
  password: '',
  role: 'staff',
  is_active: true
})

const userRules = ref({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
})

const roleForm = ref({
  id: '',
  name: '',
  description: ''
})

const roleRules = ref({
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }]
})

const getRoleType = (role: string) => {
  switch (role) {
    case 'admin':
      return 'danger'
    case 'nutritionist':
      return 'success'
    case 'chef':
      return 'warning'
    case 'staff':
      return 'info'
    default:
      return 'default'
  }
}

const fetchUsers = async () => {
  try {
    // 从后端API获取用户列表
    const response = await axios.get('/api/users')
    users.value = response.data
  } catch (error) {
    console.error('Error fetching users:', error)
    ElMessage.error('获取用户列表失败')
  }
}

const fetchRoles = async () => {
  try {
    // 从后端API获取角色列表
    const response = await axios.get('/api/roles')
    roles.value = response.data
  } catch (error) {
    console.error('Error fetching roles:', error)
    ElMessage.error('获取角色列表失败')
  }
}

const fetchPermissions = async () => {
  try {
    // 从后端API获取权限列表
    const response = await axios.get('/api/permissions')
    permissions.value = response.data
  } catch (error) {
    console.error('Error fetching permissions:', error)
    ElMessage.error('获取权限列表失败')
  }
}

const openUserForm = () => {
  userForm.value = {
    id: '',
    username: '',
    email: '',
    password: '',
    role: 'staff',
    is_active: true
  }
  userDialogVisible.value = true
}

const editUser = (user: any) => {
  userForm.value = { ...user }
  userDialogVisible.value = true
}

const deleteUser = (userId: number) => {
  ElMessageBox.confirm('确定要删除该用户吗？', '删除用户', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 调用后端API删除用户
      await axios.delete(`/api/users/${userId}`)
      // 从本地列表中移除
      users.value = users.value.filter(user => user.id !== userId)
      ElMessage.success('用户删除成功')
    } catch (error) {
      console.error('Error deleting user:', error)
      ElMessage.error('删除用户失败')
    }
  })
}

const updateUserStatus = async (user: any) => {
  try {
    // 调用后端API更新用户状态
    await axios.put(`/api/users/${user.id}`, {
      is_active: user.is_active
    })
    ElMessage.success(`用户 ${user.username} 状态已更新`)
  } catch (error) {
    console.error('Error updating user status:', error)
    ElMessage.error('更新用户状态失败')
    // 恢复原来的状态
    user.is_active = !user.is_active
  }
}

const submitUser = async () => {
  if (!userFormRef.value) return
  
  await userFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (userForm.value.id) {
          // 编辑用户
          await axios.put(`/api/users/${userForm.value.id}`, userForm.value)
          // 更新本地列表
          const index = users.value.findIndex(user => user.id === userForm.value.id)
          if (index !== -1) {
            users.value[index] = { ...userForm.value }
          }
          ElMessage.success('用户更新成功')
        } else {
          // 新增用户
          const response = await axios.post('/api/users', userForm.value)
          const newUser = response.data
          users.value.push(newUser)
          ElMessage.success('用户创建成功')
        }
        userDialogVisible.value = false
      } catch (error) {
        console.error('Error submitting user:', error)
        ElMessage.error('保存用户失败')
      }
    }
  })
}

const openRoleForm = () => {
  roleForm.value = {
    id: '',
    name: '',
    description: ''
  }
  roleDialogVisible.value = true
}

const editRole = (role: any) => {
  roleForm.value = { ...role }
  roleDialogVisible.value = true
}

const deleteRole = (roleId: number) => {
  ElMessageBox.confirm('确定要删除该角色吗？', '删除角色', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 调用后端API删除角色
      await axios.delete(`/api/roles/${roleId}`)
      // 从本地列表中移除
      roles.value = roles.value.filter(role => role.id !== roleId)
      ElMessage.success('角色删除成功')
    } catch (error) {
      console.error('Error deleting role:', error)
      ElMessage.error('删除角色失败')
    }
  })
}

const submitRole = async () => {
  if (!roleFormRef.value) return
  
  await roleFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (roleForm.value.id) {
          // 编辑角色
          await axios.put(`/api/roles/${roleForm.value.id}`, roleForm.value)
          // 更新本地列表
          const index = roles.value.findIndex(role => role.id === roleForm.value.id)
          if (index !== -1) {
            roles.value[index] = { ...roleForm.value }
          }
          ElMessage.success('角色更新成功')
        } else {
          // 新增角色
          const response = await axios.post('/api/roles', roleForm.value)
          const newRole = response.data
          roles.value.push(newRole)
          ElMessage.success('角色创建成功')
        }
        roleDialogVisible.value = false
      } catch (error) {
        console.error('Error submitting role:', error)
        ElMessage.error('保存角色失败')
      }
    }
  })
}

onMounted(() => {
  fetchUsers()
  fetchRoles()
  fetchPermissions()
})
</script>

<style scoped>
.system-container {
  padding: 20px;
}

.system-tabs {
  margin-top: 20px;
}

.system-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.system-info {
  padding: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>