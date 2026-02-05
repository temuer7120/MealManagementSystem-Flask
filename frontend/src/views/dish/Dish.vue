<template>
  <div class="dish-container">
    <h2 class="page-title">菜品管理</h2>
    <!-- 菜品列表 -->
    <el-card shadow="hover" class="dish-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">菜品列表</span>
          <el-button type="primary" @click="openDishForm" class="add-btn">
            <el-icon><Plus /></el-icon> 新增菜品
          </el-button>
        </div>
      </template>
      
      <el-table :data="dishes" style="width: 100%" stripe highlight-current-row>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="菜品名称" min-width="120" />
        <el-table-column prop="nutrition_info" label="营养成分" min-width="180" />
        <el-table-column prop="price" label="价格" width="100" />
        <el-table-column prop="total_weight" label="总量" width="100" />
        <el-table-column prop="category_id" label="分类" width="120">
          <template #default="scope">
            <el-tag size="small" effect="light">{{ getCategoryName(scope.row.category_id) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'" size="small">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editDish(scope.row)" class="edit-btn">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteDish(scope.row.id)" class="delete-btn">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 菜品表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dishForm.id ? '编辑菜品' : '新增菜品'"
      width="900px"
      :close-on-click-modal="false"
      custom-class="dish-dialog"
    >
      <el-form :model="dishForm" :rules="rules" ref="formRef" label-width="100px" class="dish-form">
        <!-- 基本信息卡片 -->
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">基本信息</span>
            </div>
          </template>
          
          <div class="form-row">
            <el-form-item label="菜品名称" prop="name" class="form-item">
              <el-input v-model="dishForm.name" placeholder="请输入菜品名称" @keyup.enter="focusNext('category_id')" class="form-input" />
            </el-form-item>
            <el-form-item label="分类" prop="category_id" class="form-item">
              <el-select v-model="dishForm.category_id" placeholder="请选择分类" class="form-select">
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
          </div>
          
          <div class="form-row">
            <el-form-item label="价格" prop="price" class="form-item">
              <el-input-number v-model="dishForm.price" :min="0" :step="0.01" placeholder="请输入价格" class="form-input" />
            </el-form-item>
            <el-form-item label="总量" prop="total_weight" class="form-item">
              <el-input-number v-model="dishForm.total_weight" :min="0" :step="0.01" placeholder="请输入总量" class="form-input" />
            </el-form-item>
            <el-form-item label="状态" class="form-item">
              <el-switch v-model="dishForm.is_active" active-color="#409EFF" inactive-color="#DCDFE6" />
            </el-form-item>
          </div>
          
          <el-form-item label="营养成分" prop="nutrition_info" class="form-item">
            <el-input
              v-model="dishForm.nutrition_info"
              type="textarea"
              :rows="3"
              placeholder='JSON格式，如：{"蛋白质": "20g", "碳水化合物": "30g", "脂肪": "10g"}'
              class="form-textarea"
            />
            <el-alert
              v-if="!dishForm.nutrition_info"
              title="提示"
              type="info"
              :closable="false"
              show-icon
              class="nutrition-tip"
            >
              营养成分会根据食材自动计算，也可以手动填写
            </el-alert>
          </el-form-item>
        </el-card>
        
        <!-- 菜品图片卡片 -->
        <el-card class="form-card" shadow="hover" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span class="card-title">菜品图片</span>
            </div>
          </template>
          
          <div class="image-upload-section">
            <div class="image-preview" v-if="dishForm.image_url">
              <img :src="dishForm.image_url" alt="菜品图片" class="preview-image">
              <el-button type="danger" size="small" @click="removeImage" class="remove-image-btn">
                <el-icon><Delete /></el-icon> 删除图片
              </el-button>
            </div>
            <div class="upload-area" v-else>
              <el-upload
                class="image-upload"
                action="/api/upload/image"
                :on-success="handleUploadSuccess"
                :on-error="handleUploadError"
                :before-upload="beforeUpload"
                :show-file-list="false"
                accept="image/*"
              >
                <div class="upload-content">
                  <el-icon class="upload-icon"><Upload /></el-icon>
                  <div class="upload-text">点击或拖拽上传图片</div>
                  <div class="upload-hint">支持 JPG、PNG、GIF 格式，大小不超过 2MB</div>
                </div>
              </el-upload>
              <div class="upload-buttons">
                <el-button type="primary" @click="takePhoto" class="photo-btn">
                  <el-icon><Camera /></el-icon> 拍照上传
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 食材组合卡片 -->
        <el-card class="form-card" shadow="hover" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span class="card-title">食材组合</span>
              <el-button type="info" size="small" @click="showIngredientTips" class="tip-btn">
                <el-icon><QuestionFilled /></el-icon> 使用提示
              </el-button>
            </div>
          </template>
          
          <div class="ingredient-combination">
            <!-- 食材库 -->
            <div class="ingredient-library">
              <div class="library-header">
                <h4 class="library-title">食材库</h4>
                <el-input
                  v-model="ingredientSearch"
                  placeholder="搜索食材"
                  class="ingredient-search"
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </div>
              <div class="ingredient-items">
                <div 
                  v-for="ingredient in filteredIngredients" 
                  :key="ingredient.id"
                  class="ingredient-item"
                  draggable="true"
                  @dragstart="onDragStart($event, ingredient)"
                  @mouseenter="$event.target.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)'"
                  @mouseleave="$event.target.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)'"
                >
                  <div class="ingredient-info">
                    <span class="ingredient-name">{{ ingredient.name }}</span>
                    <span class="ingredient-price">{{ ingredient.unit_cost }}元/{{ ingredient.unit_of_measure }}</span>
                  </div>
                </div>
                <div v-if="filteredIngredients.length === 0" class="empty-ingredients">
                  <el-icon><Warning /></el-icon>
                  <p>未找到匹配的食材</p>
                </div>
              </div>
            </div>
            
            <!-- 菜品食材 -->
            <div class="dish-ingredients-container">
              <div class="container-header">
                <h4 class="container-title">菜品食材</h4>
                <div class="nutrition-summary" v-if="dishForm.ingredients && dishForm.ingredients.length > 0">
                  <el-tag size="small" class="nutrition-tag">
                    营养: {{ getNutritionSummary() }}
                  </el-tag>
                  <el-tag size="small" class="price-tag">
                    价格: {{ dishForm.price.toFixed(2) }}元
                  </el-tag>
                  <el-tag size="small" class="weight-tag">
                    总量: {{ dishForm.total_weight.toFixed(2) }}
                  </el-tag>
                </div>
              </div>
              
              <div class="drop-zone" @dragover="onDragOver" @drop="onDrop" @dragenter="onDragEnter">
                <div class="dish-ingredients" v-if="dishForm.ingredients && dishForm.ingredients.length > 0">
                  <div 
                    v-for="(item, index) in dishForm.ingredients" 
                    :key="index"
                    class="dish-ingredient-item"
                  >
                    <div class="ingredient-details">
                      <span class="ingredient-name">{{ item.name }}</span>
                      <div class="quantity-control">
                        <el-input-number 
                          v-model="item.quantity" 
                          :min="0.01" 
                          :step="0.01" 
                          placeholder="用量"
                          size="small"
                          @change="calculateNutrition"
                          class="quantity-input"
                        />
                        <span class="ingredient-unit">{{ item.unit_of_measure }}</span>
                      </div>
                    </div>
                    <el-button type="danger" size="small" @click="removeIngredient(index)" class="remove-ingredient-btn">
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </div>
                </div>
                <div class="empty-drop-zone" v-else>
                  <el-icon class="drop-icon"><ArrowRight /></el-icon>
                  <p class="drop-text">从左侧拖拽食材到此处</p>
                  <p class="drop-hint">或点击食材添加到菜品中</p>
                </div>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 网络查询分解卡片 -->
        <el-card class="form-card" shadow="hover" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span class="card-title">网络查询分解</span>
            </div>
          </template>
          
          <div class="search-section">
            <el-form-item class="search-form-item">
              <el-input
                v-model="searchQuery"
                placeholder="请输入菜品名称进行网络查询"
                class="search-input"
                :prefix-icon="Search"
              />
              <el-button type="primary" @click="searchAndDecompose" :loading="searching" class="search-btn">
                查询并分解
              </el-button>
            </el-form-item>
            <div v-if="searching" class="loading-section">
              <el-icon class="loading-icon"><Loading /></el-icon>
              <span class="loading-text">正在查询... 请稍候</span>
            </div>
            <el-alert
              v-if="searchResult"
              :title="searchResult.name"
              :type="'success'"
              description="查询成功，已自动填充菜品信息"
              show-icon
              class="search-result-alert"
            />
          </div>
        </el-card>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false" class="cancel-btn">取消</el-button>
          <el-button type="primary" @click="submitDish" :loading="submitting" class="save-btn">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 使用提示对话框 -->
    <el-dialog
      v-model="tipDialogVisible"
      title="食材组合使用提示"
      width="500px"
    >
      <div class="tip-content">
        <el-alert
          title="拖拽操作"
          type="info"
          description="从左侧食材库中拖拽食材到右侧菜品食材区域"
          show-icon
          class="tip-alert"
        />
        <el-alert
          title="用量调整"
          type="info"
          description="拖拽后可以调整每个食材的用量，系统会自动重新计算营养成分、总量和价格"
          show-icon
          class="tip-alert"
        />
        <el-alert
          title="网络查询"
          type="info"
          description="可以通过输入菜品名称进行网络查询，系统会自动分解成食材组合并填充信息"
          show-icon
          class="tip-alert"
        />
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="tipDialogVisible = false">我知道了</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, Edit, Upload, Camera, Search, ArrowRight, Loading, QuestionFilled } from '@element-plus/icons-vue'
import axios from 'axios'

// 菜品列表
const dishes = ref<any[]>([])
// 分类列表
const categories = ref<any[]>([])
// 食材列表
const ingredients = ref<any[]>([])
// 对话框可见性
const dialogVisible = ref(false)
// 提示对话框可见性
const tipDialogVisible = ref(false)
// 表单引用
const formRef = ref<any>(null)
// 文件输入引用
const fileInput = ref(null)
// 上传状态
const uploading = ref(false)
// 上传进度
const uploadProgress = ref(0)
// 上传错误
const uploadError = ref('')
// 搜索状态
const searching = ref(false)
// 提交状态
const submitting = ref(false)
// 搜索查询
const searchQuery = ref('')
// 食材搜索
const ingredientSearch = ref('')
// 拖拽中的食材
const draggedIngredient = ref(null)
// 搜索结果
const searchResult = ref<any>(null)

// 菜品表单
const dishForm = ref({
  id: '',
  name: '',
  nutrition_info: '',
  price: 0,
  total_weight: 0,
  category_id: '',
  is_active: true,
  image_url: '',
  ingredients: []
})

// 表单规则
const rules = ref({
  name: [{ required: true, message: '请输入菜品名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }]
})

// 过滤后的食材列表
const filteredIngredients = computed(() => {
  if (!ingredientSearch.value) {
    return ingredients.value
  }
  return ingredients.value.filter(ingredient => 
    ingredient.name.toLowerCase().includes(ingredientSearch.value.toLowerCase())
  )
})

// 获取菜品列表
const fetchDishes = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    dishes.value = [
      { id: 1, name: '清蒸鱼', nutrition_info: '{"蛋白质": "25g", "碳水化合物": "5g", "脂肪": "15g"}', price: 88, total_weight: 500, category_id: 1, is_active: true },
      { id: 2, name: '红烧肉', nutrition_info: '{"蛋白质": "20g", "碳水化合物": "10g", "脂肪": "30g"}', price: 68, total_weight: 400, category_id: 1, is_active: true },
      { id: 3, name: '蔬菜沙拉', nutrition_info: '{"蛋白质": "5g", "碳水化合物": "20g", "脂肪": "10g"}', price: 38, total_weight: 300, category_id: 2, is_active: true }
    ]
  } catch (error) {
    console.error('Error fetching dishes:', error)
    ElMessage.error('获取菜品列表失败')
  }
}

// 获取分类列表
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

// 获取食材列表
const fetchIngredients = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    ingredients.value = [
      { id: 1, name: '西红柿', unit_cost: 2.5, unit_of_measure: '个', nutrition_info: '{"蛋白质": "0.9g", "碳水化合物": "4g", "脂肪": "0.2g"}' },
      { id: 2, name: '鸡蛋', unit_cost: 1.2, unit_of_measure: '个', nutrition_info: '{"蛋白质": "6.3g", "碳水化合物": "0.6g", "脂肪": "5.3g"}' },
      { id: 3, name: '大米', unit_cost: 6.5, unit_of_measure: 'kg', nutrition_info: '{"蛋白质": "7.5g", "碳水化合物": "77g", "脂肪": "0.9g"}' },
      { id: 4, name: '青菜', unit_cost: 3.8, unit_of_measure: '斤', nutrition_info: '{"蛋白质": "2.6g", "碳水化合物": "2.8g", "脂肪": "0.3g"}' },
      { id: 5, name: '猪肉', unit_cost: 28.5, unit_of_measure: '斤', nutrition_info: '{"蛋白质": "20.3g", "碳水化合物": "1.1g", "脂肪": "10.8g"}' }
    ]
  } catch (error) {
    console.error('Error fetching ingredients:', error)
    ElMessage.error('获取食材列表失败')
  }
}

// 获取分类名称
const getCategoryName = (categoryId: number) => {
  const category = categories.value.find(cat => cat.id === categoryId)
  return category ? category.name : '未知分类'
}

// 打开菜品表单
const openDishForm = () => {
  dishForm.value = {
    id: '',
    name: '',
    nutrition_info: '',
    price: 0,
    total_weight: 0,
    category_id: '',
    is_active: true,
    image_url: '',
    ingredients: []
  }
  searchResult.value = null
  dialogVisible.value = true
}

// 编辑菜品
const editDish = (dish: any) => {
  dishForm.value = { ...dish }
  if (!dishForm.value.ingredients) {
    dishForm.value.ingredients = []
  }
  searchResult.value = null
  dialogVisible.value = true
}

// 删除菜品
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

// 显示食材使用提示
const showIngredientTips = () => {
  tipDialogVisible.value = true
}

// 拖拽开始
const onDragStart = (event: any, ingredient: any) => {
  draggedIngredient.value = ingredient
  event.dataTransfer.effectAllowed = 'copy'
}

// 拖拽结束
const onDragEnd = (event: any) => {
  draggedIngredient.value = null
}

// 拖拽进入
const onDragEnter = (event: any) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'copy'
}

// 拖拽悬停
const onDragOver = (event: any) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'copy'
}

// 拖拽放置
const onDrop = (event: any) => {
  event.preventDefault()
  if (draggedIngredient.value) {
    // 检查食材是否已存在
    const existingIndex = dishForm.value.ingredients.findIndex(
      (item: any) => item.id === draggedIngredient.value.id
    )
    if (existingIndex === -1) {
      const ingredient = {
        ...draggedIngredient.value,
        quantity: 1
      }
      dishForm.value.ingredients.push(ingredient)
      calculateNutrition()
      ElMessage.success(`已添加食材: ${draggedIngredient.value.name}`)
    } else {
      ElMessage.warning('该食材已存在于菜品中')
    }
  }
}

// 移除食材
const removeIngredient = (index: number) => {
  const removedIngredient = dishForm.value.ingredients[index]
  dishForm.value.ingredients.splice(index, 1)
  calculateNutrition()
  ElMessage.success(`已移除食材: ${removedIngredient.name}`)
}

// 计算营养成分
const calculateNutrition = () => {
  let totalProtein = 0
  let totalCarbs = 0
  let totalFat = 0
  let totalWeight = 0
  let totalCost = 0
  
  dishForm.value.ingredients.forEach((item: any) => {
    // 解析营养成分
    try {
      const nutrition = JSON.parse(item.nutrition_info)
      if (nutrition.蛋白质) {
        totalProtein += parseFloat(nutrition.蛋白质) * item.quantity
      }
      if (nutrition.碳水化合物) {
        totalCarbs += parseFloat(nutrition.碳水化合物) * item.quantity
      }
      if (nutrition.脂肪) {
        totalFat += parseFloat(nutrition.脂肪) * item.quantity
      }
    } catch (e) {
      console.error('Error parsing nutrition info:', e)
    }
    
    // 计算总量和成本
    totalWeight += item.quantity
    totalCost += item.unit_cost * item.quantity
  })
  
  // 更新菜品信息
  dishForm.value.nutrition_info = JSON.stringify({
    蛋白质: `${totalProtein.toFixed(1)}g`,
    碳水化合物: `${totalCarbs.toFixed(1)}g`,
    脂肪: `${totalFat.toFixed(1)}g`
  })
  dishForm.value.total_weight = totalWeight
  dishForm.value.price = totalCost * 1.5 // 成本加成50%
}

// 获取营养成分汇总
const getNutritionSummary = () => {
  try {
    if (!dishForm.value.nutrition_info) {
      return '无'
    }
    const nutrition = JSON.parse(dishForm.value.nutrition_info)
    return `蛋白质: ${nutrition.蛋白质}, 碳水: ${nutrition.碳水化合物}, 脂肪: ${nutrition.脂肪}`
  } catch (e) {
    return '无'
  }
}

// 拍照
const takePhoto = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.capture = 'camera'
  input.onchange = (e: any) => {
    if (e.target.files && e.target.files[0]) {
      handleImageUpload(e)
    }
  }
  input.click()
}

// 处理图片上传
const handleImageUpload = async (e: any) => {
  const file = e.target.files[0]
  if (!file) return
  
  try {
    uploading.value = true
    uploadProgress.value = 0
    uploadError.value = ''
    
    // 创建FormData对象
    const formData = new FormData()
    formData.append('image', file)
    
    // 上传图片到服务器
    const response = await axios.post('/api/upload/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent: any) => {
        if (progressEvent.total) {
          uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      }
    })
    
    // 设置图片URL
    dishForm.value.image_url = response.data.image_url
    
    // 隐藏上传进度
    setTimeout(() => {
      uploading.value = false
      uploadProgress.value = 0
    }, 1000)
    
    ElMessage.success('图片上传成功')
  } catch (error) {
    console.error('上传图片失败:', error)
    uploadError.value = '上传图片失败，请重试'
    uploading.value = false
    uploadProgress.value = 0
    setTimeout(() => {
      uploadError.value = ''
    }, 3000)
    ElMessage.error('上传图片失败，请重试')
  }
}

// 处理上传成功
const handleUploadSuccess = (response: any) => {
  dishForm.value.image_url = response.image_url
  ElMessage.success('图片上传成功')
}

// 处理上传失败
const handleUploadError = () => {
  ElMessage.error('上传图片失败，请重试')
}

// 上传前校验
const beforeUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB！')
    return false
  }
  return true
}

// 移除图片
const removeImage = () => {
  dishForm.value.image_url = ''
  uploadError.value = ''
  ElMessage.success('图片已删除')
}

// 焦点导航
const focusNext = (field: string) => {
  // 简单的焦点导航实现，实际项目中可以使用更复杂的方法
  console.log('Focus next field:', field)
  // 这里可以实现更精确的焦点控制
}

// 网络查询分解
const searchAndDecompose = async () => {
  if (!searchQuery.value) {
    ElMessage.warning('请输入菜品名称')
    return
  }
  
  searching.value = true
  searchResult.value = null
  
  try {
    // 模拟网络查询，实际项目中应该调用后端API
    setTimeout(() => {
      // 模拟查询结果
      const mockResult = {
        name: searchQuery.value,
        ingredients: [
          { id: 1, name: '西红柿', unit_cost: 2.5, unit_of_measure: '个', quantity: 2, nutrition_info: '{"蛋白质": "0.9g", "碳水化合物": "4g", "脂肪": "0.2g"}' },
          { id: 2, name: '鸡蛋', unit_cost: 1.2, unit_of_measure: '个', quantity: 3, nutrition_info: '{"蛋白质": "6.3g", "碳水化合物": "0.6g", "脂肪": "5.3g"}' }
        ],
        nutrition_info: '{"蛋白质": "20g", "碳水化合物": "10g", "脂肪": "15g"}',
        total_weight: 300,
        price: 15
      }
      
      // 自动填充结果
      dishForm.value.name = mockResult.name
      dishForm.value.ingredients = mockResult.ingredients
      dishForm.value.nutrition_info = mockResult.nutrition_info
      dishForm.value.total_weight = mockResult.total_weight
      dishForm.value.price = mockResult.price
      
      // 设置搜索结果
      searchResult.value = mockResult
      
      ElMessage.success('查询分解成功，已自动填充菜品信息')
      searching.value = false
    }, 1500)
  } catch (error) {
    console.error('查询分解失败:', error)
    ElMessage.error('查询分解失败，请重试')
    searching.value = false
  }
}

// 提交菜品
const submitDish = async () => {
  if (!formRef.value) return
  
  submitting.value = true
  
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
      } finally {
        submitting.value = false
      }
    } else {
      submitting.value = false
    }
  })
}

// 初始化
onMounted(() => {
  fetchDishes()
  fetchCategories()
  fetchIngredients()
})
</script>

<style scoped>
/* 页面容器 */
.dish-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 页面标题 */
.page-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409EFF;
}

/* 卡片样式 */
.dish-card {
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

.card-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

/* 按钮样式 */
.add-btn {
  border-radius: 4px;
  font-weight: 500;
}

.edit-btn,
.delete-btn {
  margin-right: 8px;
  border-radius: 4px;
}

/* 对话框样式 */
.dish-dialog {
  border-radius: 8px;
  overflow: hidden;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  padding: 16px;
  background-color: #fafafa;
  border-top: 1px solid #ebeef5;
}

.cancel-btn,
.save-btn {
  margin-left: 8px;
  border-radius: 4px;
  min-width: 80px;
}

/* 表单样式 */
.dish-form {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
}

.form-card {
  border-radius: 8px;
  margin-bottom: 20px;
  overflow: hidden;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
}

.form-item {
  flex: 1;
}

.form-input,
.form-select {
  width: 100%;
  border-radius: 4px;
}

.form-textarea {
  width: 100%;
  border-radius: 4px;
  resize: vertical;
  min-height: 100px;
}

/* 营养成分提示 */
.nutrition-tip {
  margin-top: 8px;
  border-radius: 4px;
}

/* 图片上传区域 */
.image-upload-section {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.image-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.preview-image {
  max-width: 300px;
  max-height: 200px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
}

.preview-image:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.remove-image-btn {
  margin-top: 8px;
  border-radius: 4px;
}

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 40px;
  text-align: center;
  background-color: #ffffff;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #409EFF;
  background-color: #ecf5ff;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.upload-icon {
  font-size: 48px;
  color: #c0c4cc;
  transition: all 0.3s ease;
}

.upload-area:hover .upload-icon {
  color: #409EFF;
}

.upload-text {
  font-size: 16px;
  color: #606266;
  font-weight: 500;
}

.upload-hint {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.upload-buttons {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.photo-btn {
  border-radius: 4px;
  font-weight: 500;
}

/* 食材组合区域 */
.ingredient-combination {
  display: flex;
  gap: 24px;
  min-height: 400px;
}

.ingredient-library {
  flex: 1;
  background-color: #ffffff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.library-header {
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
  background-color: #fafafa;
}

.library-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 12px;
}

.ingredient-search {
  width: 100%;
  border-radius: 4px;
}

.ingredient-items {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.ingredient-item {
  background-color: #ffffff;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 12px;
  cursor: grab;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ingredient-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
  border-color: #409EFF;
}

.ingredient-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.ingredient-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.ingredient-price {
  font-size: 12px;
  color: #67c23a;
  font-weight: 500;
}

.dish-ingredients-container {
  flex: 1;
  background-color: #ffffff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.container-header {
  padding: 16px;
  border-bottom: 1px solid #ebeef5;
  background-color: #fafafa;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.container-title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.nutrition-summary {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.nutrition-tag,
.price-tag,
.weight-tag {
  border-radius: 4px;
  font-size: 12px;
}

.drop-zone {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-y: auto;
}

.dish-ingredients {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dish-ingredient-item {
  background-color: #f8f9fa;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.dish-ingredient-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  background-color: #ffffff;
}

.ingredient-details {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.quantity-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.quantity-input {
  width: 120px;
  border-radius: 4px;
}

.ingredient-unit {
  font-size: 12px;
  color: #909399;
  white-space: nowrap;
}

.remove-ingredient-btn {
  border-radius: 4px;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-drop-zone {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  padding: 40px 20px;
  text-align: center;
}

.drop-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.4;
  transition: all 0.3s ease;
}

.drop-text {
  font-size: 16px;
  margin-bottom: 8px;
  color: #606266;
}

.drop-hint {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.empty-ingredients {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #909399;
  text-align: center;
}

/* 网络查询分解区域 */
.search-section {
  padding: 16px;
  background-color: #fafafa;
  border-radius: 8px;
}

.search-form-item {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-input {
  flex: 1;
  border-radius: 4px;
}

.search-btn {
  border-radius: 4px;
  font-weight: 500;
  white-space: nowrap;
}

.loading-section {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 16px;
  padding: 16px;
  background-color: #ecf5ff;
  border-radius: 4px;
  color: #409EFF;
}

.loading-icon {
  margin-right: 8px;
  animation: spin 1s linear infinite;
}

.loading-text {
  font-size: 14px;
}

.search-result-alert {
  margin-top: 16px;
  border-radius: 4px;
}

/* 提示对话框 */
.tip-content {
  padding: 8px 0;
}

.tip-alert {
  margin-bottom: 12px;
  border-radius: 4px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .ingredient-combination {
    flex-direction: column;
    min-height: 600px;
  }
  
  .ingredient-library,
  .dish-ingredients-container {
    min-height: 300px;
  }
}

@media (max-width: 768px) {
  .dish-container {
    padding: 12px;
  }
  
  .page-title {
    font-size: 20px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
  
  .search-form-item {
    flex-direction: column;
    align-items: stretch;
  }
  
  .nutrition-summary {
    justify-content: center;
  }
  
  .upload-area {
    padding: 20px;
  }
  
  .preview-image {
    max-width: 200px;
    max-height: 150px;
  }
}

/* 动画效果 */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>