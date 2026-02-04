<template>
  <div class="dish-container">
    <h2>菜品管理</h2>
    <!-- 菜品列表 -->
    <el-card shadow="hover" class="dish-card">
      <template #header>
        <div class="card-header">
          <span>菜品列表</span>
          <el-button type="primary" @click="openDishForm">
            <el-icon><Plus /></el-icon> 新增菜品
          </el-button>
        </div>
      </template>
      
      <el-table :data="dishes" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="菜品名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="price" label="价格" width="100" />
        <el-table-column prop="category_id" label="分类" width="120">
          <template #default="scope">
            {{ getCategoryName(scope.row.category_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editDish(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteDish(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 菜品表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="菜品管理"
      width="500px"
    >
      <el-form :model="dishForm" :rules="rules" ref="formRef">
        <el-form-item label="菜品名称" prop="name">
          <el-input v-model="dishForm.name" placeholder="请输入菜品名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="dishForm.description"
            type="textarea"
            placeholder="请输入菜品描述"
          />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="dishForm.price" :min="0" :step="0.01" placeholder="请输入价格" />
        </el-form-item>
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="dishForm.category_id" placeholder="请选择分类">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="dishForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDish">保存</el-button>
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

const dishes = ref<any[]>([])
const categories = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)

const dishForm = ref({
  id: '',
  name: '',
  description: '',
  price: 0,
  category_id: '',
  is_active: true
})

const rules = ref({
  name: [{ required: true, message: '请输入菜品名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }]
})

const fetchDishes = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    dishes.value = [
      { id: 1, name: '清蒸鱼', description: '新鲜鲈鱼清蒸', price: 88, category_id: 1, is_active: true },
      { id: 2, name: '红烧肉', description: '传统红烧肉', price: 68, category_id: 1, is_active: true },
      { id: 3, name: '蔬菜沙拉', description: '新鲜蔬菜沙拉', price: 38, category_id: 2, is_active: true }
    ]
  } catch (error) {
    console.error('Error fetching dishes:', error)
    ElMessage.error('获取菜品列表失败')
  }
}

const fetchCategories = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    categories.value = [
      { id: 1, name: '主菜' },
      { id: 2, name: '配菜' },
      { id: 3, name: '汤品' },
      { id: 4, name: '点心' }
    ]
  } catch (error) {
    console.error('Error fetching categories:', error)
    ElMessage.error('获取分类列表失败')
  }
}

const getCategoryName = (categoryId: number) => {
  const category = categories.value.find(cat => cat.id === categoryId)
  return category ? category.name : '未知分类'
}

const openDishForm = () => {
  dishForm.value = {
    id: '',
    name: '',
    description: '',
    price: 0,
    category_id: '',
    is_active: true
  }
  dialogVisible.value = true
}

const editDish = (dish: any) => {
  dishForm.value = { ...dish }
  dialogVisible.value = true
}

const deleteDish = (dishId: number) => {
  ElMessageBox.confirm('确定要删除该菜品吗？', '删除菜品', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟删除，实际项目中应该调用后端API
      dishes.value = dishes.value.filter(dish => dish.id !== dishId)
      ElMessage.success('菜品删除成功')
    } catch (error) {
      console.error('Error deleting dish:', error)
      ElMessage.error('删除菜品失败')
    }
  })
}

const submitDish = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (dishForm.value.id) {
          // 编辑菜品
          const index = dishes.value.findIndex(dish => dish.id === dishForm.value.id)
          if (index !== -1) {
            dishes.value[index] = { ...dishForm.value }
          }
          ElMessage.success('菜品更新成功')
        } else {
          // 新增菜品
          const newDish = {
            ...dishForm.value,
            id: dishes.value.length + 1
          }
          dishes.value.push(newDish)
          ElMessage.success('菜品创建成功')
        }
        dialogVisible.value = false
      } catch (error) {
        console.error('Error submitting dish:', error)
        ElMessage.error('保存菜品失败')
      }
    }
  })
}

onMounted(() => {
  fetchDishes()
  fetchCategories()
})
</script>

<style scoped>
.dish-container {
  padding: 20px;
}

.dish-card {
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