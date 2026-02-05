<template>
  <div class="ingredient-container">
    <h2 class="page-title">
      <i class="fas fa-seedling"></i> 食材管理
    </h2>
    <div class="card">
      <div class="card-header">
        <button class="btn btn-primary" @click="showAddForm = true">
          <i class="fas fa-plus"></i> 添加食材
        </button>
      </div>
      <div class="card-body">
        <table class="table table-striped">
          <thead>
            <tr>
              <th>ID</th>
              <th>食材名称</th>
              <th>食材类别</th>
              <th>库存数量</th>
              <th>单位</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ingredient in ingredients" :key="ingredient.id">
              <td>{{ ingredient.id }}</td>
              <td>{{ ingredient.name }}</td>
              <td>{{ ingredient.category }}</td>
              <td>{{ ingredient.stock }}</td>
              <td>{{ ingredient.unit }}</td>
              <td>
                <button class="btn btn-sm btn-info" @click="editIngredient(ingredient)">
                  <i class="fas fa-edit"></i> 编辑
                </button>
                <button class="btn btn-sm btn-danger" @click="deleteIngredient(ingredient.id)">
                  <i class="fas fa-trash"></i> 删除
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加/编辑食材弹窗 -->
    <el-dialog
      v-model="showAddForm"
      :title="editingIngredient ? '编辑食材' : '添加食材'"
      width="500px"
    >
      <div class="form-group">
        <label for="ingredient-name">食材名称</label>
        <input 
          type="text" 
          class="form-control" 
          id="ingredient-name" 
          v-model="formData.name"
          required
        >
      </div>
      <div class="form-group">
        <label for="ingredient-category">食材类别</label>
        <input 
          type="text" 
          class="form-control" 
          id="ingredient-category" 
          v-model="formData.category"
          required
        >
      </div>
      <div class="form-group">
        <label for="ingredient-stock">库存数量</label>
        <input 
          type="number" 
          class="form-control" 
          id="ingredient-stock" 
          v-model="formData.stock"
          required
        >
      </div>
      <div class="form-group">
        <label for="ingredient-unit">单位</label>
        <input 
          type="text" 
          class="form-control" 
          id="ingredient-unit" 
          v-model="formData.unit"
          required
        >
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddForm = false">取消</el-button>
          <el-button type="primary" @click="saveIngredient">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const showAddForm = ref(false)
const editingIngredient = ref(false)
const ingredients = ref([])
const formData = ref({
  id: null,
  name: '',
  category: '',
  stock: 0,
  unit: ''
})

onMounted(() => {
  fetchIngredients()
})

const fetchIngredients = async () => {
  try {
    const response = await axios.get('/api/ingredients')
    ingredients.value = response.data
  } catch (error) {
    console.error('获取食材列表失败:', error)
  }
}

const editIngredient = (ingredient) => {
  editingIngredient.value = true
  formData.value = { ...ingredient }
  showAddForm.value = true
}

const deleteIngredient = async (id) => {
  try {
    await axios.delete(`/api/ingredients/${id}`)
    fetchIngredients()
  } catch (error) {
    console.error('删除食材失败:', error)
  }
}

const saveIngredient = async () => {
  try {
    if (editingIngredient.value) {
      await axios.put(`/api/ingredients/${formData.value.id}`, formData.value)
    } else {
      await axios.post('/api/ingredients', formData.value)
    }
    showAddForm.value = false
    fetchIngredients()
    resetForm()
  } catch (error) {
    console.error('保存食材失败:', error)
  }
}

const resetForm = () => {
  formData.value = {
    id: null,
    name: '',
    category: '',
    stock: 0,
    unit: ''
  }
  editingIngredient.value = false
}
</script>

<style scoped>
.ingredient-container {
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