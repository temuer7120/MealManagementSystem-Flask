<template>
  <div class="employee-container">
    <h2 class="page-title">
      <i class="fas fa-users"></i> 员工管理
    </h2>
    <div class="card">
      <div class="card-header">
        <button class="btn btn-primary" @click="showAddForm = true">
          <i class="fas fa-plus"></i> 添加员工
        </button>
      </div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>员工姓名</th>
              <th>工号</th>
              <th>职位</th>
              <th>联系电话</th>
              <th>入职日期</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="employee in employees" :key="employee.id">
              <td>{{ employee.id }}</td>
              <td>{{ employee.name }}</td>
              <td>{{ employee.employee_id }}</td>
              <td>{{ employee.position }}</td>
              <td>{{ employee.phone }}</td>
              <td>{{ employee.hire_date }}</td>
              <td>
                <button class="btn btn-sm btn-info" @click="editEmployee(employee)">
                  <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteEmployee(employee.id)">
                  <i class="fas fa-trash"></i> 删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加/编辑员工弹窗 -->
    <el-dialog
      v-model="showAddForm"
      :title="editingEmployee ? '编辑员工' : '添加员工'"
      width="500px"
    >
      <div class="form-group">
        <label for="employee-name">员工姓名</label>
        <input 
          type="text" 
          class="form-control" 
          id="employee-name" 
          v-model="formData.name"
          required
        >
      </div>
      <div class="form-group">
        <label for="employee-id">工号</label>
        <input 
          type="text" 
          class="form-control" 
          id="employee-id" 
          v-model="formData.employee_id"
          required
        >
      </div>
      <div class="form-group">
        <label for="employee-position">职位</label>
        <select 
          class="form-control" 
          id="employee-position" 
          v-model="formData.position"
          required
        >
          <option value="">请选择职位</option>
          <option value="管理员">管理员</option>
          <option value="护士">护士</option>
          <option value="厨师">厨师</option>
          <option value="护理员">护理员</option>
          <option value="其他">其他</option>
        </select>
      </div>
      <div class="form-group">
        <label for="employee-phone">联系电话</label>
        <input 
          type="tel" 
          class="form-control" 
          id="employee-phone" 
          v-model="formData.phone"
          required
        >
      </div>
      <div class="form-group">
        <label for="employee-hire-date">入职日期</label>
        <input 
          type="date" 
          class="form-control" 
          id="employee-hire-date" 
          v-model="formData.hire_date"
          required
        >
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
  name: '',
  employee_id: '',
  position: '',
  phone: '',
  hire_date: ''
})

onMounted(() => {
  fetchEmployees()
})

const fetchEmployees = async () => {
  try {
    const response = await axios.get('/api/employees')
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
    await axios.delete(`/api/employees/${id}`)
    fetchEmployees()
  } catch (error) {
    console.error('删除员工失败:', error)
  }
}

const saveEmployee = async () => {
  try {
    if (editingEmployee.value) {
      await axios.put(`/api/employees/${formData.value.id}`, formData.value)
    } else {
      await axios.post('/api/employees', formData.value)
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
</style>