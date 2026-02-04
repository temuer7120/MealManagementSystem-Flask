<template>
  <div class="menu-container">
    <h2>餐单管理</h2>
    <!-- 餐单列表 -->
    <el-card shadow="hover" class="menu-card">
      <template #header>
        <div class="card-header">
          <span>餐单列表</span>
          <el-button type="primary" @click="openMenuForm">
            <el-icon><Plus /></el-icon> 新增餐单
          </el-button>
        </div>
      </template>
      
      <el-table :data="menus" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="餐单名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="price" label="价格" width="100" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editMenu(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteMenu(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 餐单表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="餐单管理"
      width="500px"
    >
      <el-form :model="menuForm" :rules="rules" ref="formRef">
        <el-form-item label="餐单名称" prop="name">
          <el-input v-model="menuForm.name" placeholder="请输入餐单名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="menuForm.description"
            type="textarea"
            placeholder="请输入餐单描述"
          />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="menuForm.price" :min="0" :step="0.01" placeholder="请输入价格" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="menuForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitMenu">保存</el-button>
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

const menus = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)

const menuForm = ref({
  id: '',
  name: '',
  description: '',
  price: 0,
  is_active: true
})

const rules = ref({
  name: [{ required: true, message: '请输入餐单名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }]
})

const fetchMenus = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    menus.value = [
      { id: 1, name: '基础月子餐', description: '适合产后第一周的基础调理餐', price: 380, is_active: true },
      { id: 2, name: '进阶月子餐', description: '适合产后第二周的营养补充餐', price: 420, is_active: true },
      { id: 3, name: '高级月子餐', description: '适合产后第三周的全面恢复餐', price: 560, is_active: true }
    ]
  } catch (error) {
    console.error('Error fetching menus:', error)
    ElMessage.error('获取餐单列表失败')
  }
}

const openMenuForm = () => {
  menuForm.value = {
    id: '',
    name: '',
    description: '',
    price: 0,
    is_active: true
  }
  dialogVisible.value = true
}

const editMenu = (menu: any) => {
  menuForm.value = { ...menu }
  dialogVisible.value = true
}

const deleteMenu = (menuId: number) => {
  ElMessageBox.confirm('确定要删除该餐单吗？', '删除餐单', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟删除，实际项目中应该调用后端API
      menus.value = menus.value.filter(menu => menu.id !== menuId)
      ElMessage.success('餐单删除成功')
    } catch (error) {
      console.error('Error deleting menu:', error)
      ElMessage.error('删除餐单失败')
    }
  })
}

const submitMenu = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (menuForm.value.id) {
          // 编辑餐单
          const index = menus.value.findIndex(menu => menu.id === menuForm.value.id)
          if (index !== -1) {
            menus.value[index] = { ...menuForm.value }
          }
          ElMessage.success('餐单更新成功')
        } else {
          // 新增餐单
          const newMenu = {
            ...menuForm.value,
            id: menus.value.length + 1
          }
          menus.value.push(newMenu)
          ElMessage.success('餐单创建成功')
        }
        dialogVisible.value = false
      } catch (error) {
        console.error('Error submitting menu:', error)
        ElMessage.error('保存餐单失败')
      }
    }
  })
}

onMounted(() => {
  fetchMenus()
})
</script>

<style scoped>
.menu-container {
  padding: 20px;
}

.menu-card {
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