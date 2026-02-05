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
      width="800px"
    >
      <div class="row">
        <!-- 左侧基本信息 -->
        <div class="col-md-6">
          <div class="form-group">
            <label for="ingredient-name">食材名称</label>
            <input 
              type="text" 
              class="form-control" 
              id="ingredient-name" 
              v-model="formData.name"
              required
              @keyup.enter="focusNext('ingredient-category')"
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
              @keyup.enter="focusNext('ingredient-stock')"
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
              @keyup.enter="focusNext('ingredient-unit')"
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
              @keyup.enter="focusNext('ingredient-price')"
            >
          </div>
          <div class="form-group">
            <label for="ingredient-price">价格</label>
            <input 
              type="number" 
              class="form-control" 
              id="ingredient-price" 
              v-model="formData.unit_cost"
              step="0.01"
              @keyup.enter="focusNext('ingredient-supplier')"
            >
          </div>
          <div class="form-group">
            <label for="ingredient-supplier">供应商</label>
            <input 
              type="text" 
              class="form-control" 
              id="ingredient-supplier" 
              v-model="formData.supplier"
              @keyup.enter="focusNext('ingredient-purchaser')"
            >
          </div>
          <div class="form-group">
            <label for="ingredient-purchaser">购买人</label>
            <input 
              type="text" 
              class="form-control" 
              id="ingredient-purchaser" 
              v-model="formData.purchaser"
              @keyup.enter="focusNext('ingredient-purchase-date')"
            >
          </div>
          <div class="form-group">
            <label for="ingredient-purchase-date">购入日期</label>
            <input 
              type="date" 
              class="form-control" 
              id="ingredient-purchase-date" 
              v-model="formData.purchase_date"
              @keyup.enter="focusNext('ingredient-shelf-life')"
            >
          </div>
          <div class="form-group">
            <label for="ingredient-shelf-life">保质期（天）</label>
            <input 
              type="number" 
              class="form-control" 
              id="ingredient-shelf-life" 
              v-model="formData.shelf_life_days"
              @keyup.enter="saveIngredient"
            >
          </div>
        </div>
        
        <!-- 右侧详细信息 -->
        <div class="col-md-6">
          <!-- 图片上传区域 -->
          <div class="form-group mb-4">
            <label class="form-label">食材图片</label>
            <div 
              class="image-upload-section"
              @dragover.prevent
              @drop.prevent="handleDrop"
            >
              <!-- 图片预览区域 -->
              <div class="image-preview-container" v-if="formData.image_url">
                <div class="image-preview">
                  <img :src="formData.image_url" alt="食材图片" class="preview-image">
                  <button class="btn-remove-image" @click="removeImage">
                    <i class="fas fa-times"></i>
                  </button>
                </div>
                <p class="image-info">{{ getImageInfo() }}</p>
              </div>
              
              <!-- 上传提示区域 -->
              <div class="upload-prompt" v-else>
                <div class="upload-icon">
                  <i class="fas fa-cloud-upload-alt"></i>
                </div>
                <h4>上传食材图片</h4>
                <p class="upload-hint">点击上传或拖拽图片到此处</p>
                <p class="upload-format">支持 JPG、PNG、WEBP 格式，最大 5MB</p>
              </div>
              
              <!-- 上传按钮区域 -->
              <div class="upload-buttons">
                <button class="btn btn-primary upload-btn mb-2" @click="takePhoto">
                  <i class="fas fa-camera"></i> 拍照
                </button>
                <button class="btn btn-outline-primary upload-btn" @click="uploadImage">
                  <i class="fas fa-upload"></i> 选择图片
                </button>
              </div>
              
              <!-- 上传进度条 -->
              <div class="upload-progress" v-if="uploading">
                <div class="progress">
                  <div 
                    class="progress-bar" 
                    role="progressbar"
                    :style="{ width: uploadProgress + '%' }"
                    :aria-valuenow="uploadProgress"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  >
                    {{ uploadProgress }}%
                  </div>
                </div>
              </div>
              
              <!-- 上传错误提示 -->
              <div class="upload-error" v-if="uploadError">
                <i class="fas fa-exclamation-circle"></i>
                <span>{{ uploadError }}</span>
              </div>
            </div>
          </div>
          
          <div class="form-group">
            <label for="ingredient-nutrition">营养成分</label>
            <textarea 
              class="form-control" 
              id="ingredient-nutrition" 
              v-model="formData.nutrition_info"
              rows="3"
              placeholder='JSON格式，如：{"蛋白质": "10g", "碳水化合物": "20g", "脂肪": "5g"}'
            ></textarea>
          </div>
          <div class="form-group">
            <label for="ingredient-calories">热量值（每单位）</label>
            <input 
              type="number" 
              class="form-control" 
              id="ingredient-calories" 
              v-model="formData.calories_per_unit"
              step="0.01"
            >
          </div>
          <div class="form-group">
            <label for="ingredient-nutrition">营养成分</label>
            <textarea 
              class="form-control" 
              id="ingredient-nutrition" 
              v-model="formData.nutrition_info"
              rows="3"
              placeholder='JSON格式，如：{"蛋白质": "10g", "碳水化合物": "20g", "脂肪": "5g"}'
            ></textarea>
          </div>
          <div class="form-group">
            <label for="ingredient-features">特点</label>
            <textarea 
              class="form-control" 
              id="ingredient-features" 
              v-model="formData.features"
              rows="2"
            ></textarea>
          </div>
          <div class="form-group">
            <label for="ingredient-taboo">禁忌</label>
            <textarea 
              class="form-control" 
              id="ingredient-taboo" 
              v-model="formData.taboo"
              rows="2"
            ></textarea>
          </div>
        </div>
      </div>
      
      <div class="mt-4">
        <button class="btn btn-info mb-3" @click="autoIdentifyIngredient" v-if="formData.image_url">
          <i class="fas fa-magic"></i> 自动识别食材
        </button>
        <div v-if="identifying" class="alert alert-info">
          <i class="fas fa-spinner fa-spin"></i> 正在识别食材，请稍候...
        </div>
        <div v-if="identifyResult" class="alert alert-success">
          <i class="fas fa-check"></i> 食材识别成功！已自动填充相关信息。
        </div>
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
const identifying = ref(false)
const identifyResult = ref(false)
const fileInput = ref(null)
const uploading = ref(false)
const uploadProgress = ref(0)
const uploadError = ref('')
const formData = ref({
  id: null,
  name: '',
  category: '',
  stock: 0,
  unit: '',
  unit_cost: null,
  description: '',
  calories_per_unit: null,
  nutrition_info: '',
  shelf_life_days: null,
  image_url: '',
  supplier: '',
  purchaser: '',
  purchase_date: '',
  features: '',
  taboo: ''
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

const takePhoto = () => {
  // 触发文件输入，使用相机捕获
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.capture = 'camera'
  input.onchange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleImageUpload(e)
    }
  }
  input.click()
}

const uploadImage = () => {
  // 触发文件输入，选择图片
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleImageUpload(e)
    }
  }
  input.click()
}

const handleImageUpload = async (e) => {
  const file = e.target.files[0]
  await processFile(file)
}

const handleDrop = async (e) => {
  const file = e.dataTransfer.files[0]
  await processFile(file)
}

const processFile = async (file) => {
  if (!file) return
  
  // 验证文件类型
  if (!file.type.match('image.*')) {
    uploadError.value = '请上传有效的图片文件'
    setTimeout(() => {
      uploadError.value = ''
    }, 3000)
    return
  }
  
  // 验证文件大小
  if (file.size > 5 * 1024 * 1024) {
    uploadError.value = '图片大小不能超过5MB'
    setTimeout(() => {
      uploadError.value = ''
    }, 3000)
    return
  }
  
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
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        }
      }
    })
    
    // 设置图片URL
    formData.value.image_url = response.data.image_url
    
    // 3秒后隐藏上传进度
    setTimeout(() => {
      uploading.value = false
      uploadProgress.value = 0
    }, 1000)
  } catch (error) {
    console.error('上传图片失败:', error)
    uploadError.value = '上传图片失败，请重试'
    uploading.value = false
    uploadProgress.value = 0
    setTimeout(() => {
      uploadError.value = ''
    }, 3000)
  }
}

const removeImage = () => {
  formData.value.image_url = ''
  uploadError.value = ''
}

const getImageInfo = () => {
  if (!formData.value.image_url) return ''
  const url = formData.value.image_url
  const filename = url.split('/').pop()
  return `已上传: ${filename}`
}

const autoIdentifyIngredient = async () => {
  if (!formData.value.image_url) {
    alert('请先上传食材图片')
    return
  }
  
  identifying.value = true
  identifyResult.value = false
  
  try {
    // 调用后端AI识别接口
    const response = await axios.post('/api/ingredients/identify', {
      image_url: formData.value.image_url
    })
    
    const result = response.data
    
    // 自动填充识别结果
    if (result.name) formData.value.name = result.name
    if (result.category) formData.value.category = result.category
    if (result.nutrition_info) formData.value.nutrition_info = JSON.stringify(result.nutrition_info)
    if (result.calories) formData.value.calories_per_unit = result.calories
    if (result.features) formData.value.features = result.features
    if (result.taboo) formData.value.taboo = result.taboo
    if (result.description) formData.value.description = result.description
    if (result.shelf_life_days) formData.value.shelf_life_days = result.shelf_life_days
    
    identifyResult.value = true
    
    // 3秒后隐藏成功提示
    setTimeout(() => {
      identifyResult.value = false
    }, 3000)
  } catch (error) {
    console.error('自动识别食材失败:', error)
    alert('自动识别失败，请重试')
  } finally {
    identifying.value = false
  }
}

const saveIngredient = async () => {
  try {
    // 准备保存数据
    const saveData = {
      ...formData.value,
      current_stock: formData.value.stock,
      unit_of_measure: formData.value.unit
    }
    
    // 处理营养成分JSON
    if (saveData.nutrition_info) {
      try {
        saveData.nutrition_info = JSON.parse(saveData.nutrition_info)
      } catch {
        // 如果不是有效的JSON，保持原样
      }
    }
    
    // 移除不需要的字段
    delete saveData.stock
    delete saveData.unit
    delete saveData.supplier
    delete saveData.purchaser
    delete saveData.purchase_date
    delete saveData.features
    delete saveData.taboo
    
    if (editingIngredient.value) {
      await axios.put(`/api/ingredients/${saveData.id}`, saveData)
    } else {
      await axios.post('/api/ingredients', saveData)
    }
    
    showAddForm.value = false
    fetchIngredients()
    resetForm()
  } catch (error) {
    console.error('保存食材失败:', error)
    alert('保存失败，请重试')
  }
}

const resetForm = () => {
  formData.value = {
    id: null,
    name: '',
    category: '',
    stock: 0,
    unit: '',
    unit_cost: null,
    description: '',
    calories_per_unit: null,
    nutrition_info: '',
    shelf_life_days: null,
    image_url: '',
    supplier: '',
    purchaser: '',
    purchase_date: '',
    features: '',
    taboo: ''
  }
  editingIngredient.value = false
  identifyResult.value = false
}

const focusNext = (elementId) => {
  const element = document.getElementById(elementId)
  if (element) {
    element.focus()
  }
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

/* 图片上传区域样式 */
.image-upload-section {
  border: 2px dashed #e0e0e0;
  border-radius: 12px;
  padding: 40px 30px;
  text-align: center;
  background-color: #fafbfc;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.image-upload-section:hover {
  border-color: var(--primary-color);
  background-color: #f0f7ff;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.1);
}

.image-upload-section.drag-over {
  border-color: var(--primary-color);
  background-color: #e3f2fd;
  box-shadow: 0 4px 16px rgba(52, 152, 219, 0.2);
}

/* 图片预览容器 */
.image-preview-container {
  margin-bottom: 20px;
}

.image-preview {
  position: relative;
  display: inline-block;
  margin-bottom: 10px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease;
}

.image-preview:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.preview-image {
  max-width: 100%;
  max-height: 240px;
  display: block;
  border-radius: 8px;
  transition: filter 0.2s ease;
}

.image-preview:hover .preview-image {
  filter: brightness(0.9);
}

.btn-remove-image {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.9);
  border: none;
  color: #333;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
  opacity: 0;
  visibility: hidden;
}

.image-preview:hover .btn-remove-image {
  opacity: 1;
  visibility: visible;
}

.btn-remove-image:hover {
  background-color: #ff4757;
  color: white;
  transform: scale(1.1);
}

.image-info {
  font-size: 13px;
  color: #666;
  margin-top: 8px;
  font-weight: 400;
}

/* 上传提示区域 */
.upload-prompt {
  margin-bottom: 25px;
}

.upload-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #e3f2fd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  transition: all 0.3s ease;
}

.upload-icon i {
  font-size: 32px;
  color: var(--primary-color);
  transition: transform 0.3s ease;
}

.image-upload-section:hover .upload-icon i {
  transform: scale(1.1);
}

.upload-prompt h4 {
  margin: 0 0 10px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.upload-hint {
  margin: 0 0 5px;
  font-size: 14px;
  color: #666;
}

.upload-format {
  margin: 0;
  font-size: 12px;
  color: #999;
}

/* 上传按钮区域 */
.upload-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 20px;
}

.upload-btn {
  min-width: 140px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.upload-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 上传进度条 */
.upload-progress {
  margin-top: 20px;
  max-width: 300px;
  margin-left: auto;
  margin-right: auto;
}

.progress {
  height: 8px;
  border-radius: 4px;
  background-color: #e0e0e0;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: var(--primary-color);
  border-radius: 4px;
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 10px;
  font-weight: bold;
  min-width: 20px;
}

/* 上传错误提示 */
.upload-error {
  margin-top: 15px;
  padding: 10px 15px;
  background-color: #fee;
  border: 1px solid #fcc;
  border-radius: 6px;
  color: #c62828;
  font-size: 13px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  animation: fadeIn 0.3s ease;
}

.upload-error i {
  font-size: 14px;
}

/* 表单标签样式 */
.form-label {
  font-weight: 600;
  margin-bottom: 10px;
  display: block;
  color: #333;
  font-size: 14px;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(52, 152, 219, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(52, 152, 219, 0);
  }
}

/* 响应式调整 */
@media (max-width: 768px) {
  .image-upload-section {
    padding: 30px 20px;
  }
  
  .upload-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .upload-btn {
    width: 100%;
    max-width: 200px;
  }
  
  .image-preview img {
    max-height: 180px;
  }
}

/* 响应式布局调整 */
@media (max-width: 768px) {
  .row {
    flex-direction: column;
  }
  
  .col-md-6 {
    width: 100%;
    margin-bottom: 20px;
  }
  
  .el-dialog {
    width: 90% !important;
  }
}

/* 表单样式优化 */
.form-control {
  border-radius: 4px;
  border: 1px solid #ced4da;
  padding: 8px 12px;
  font-size: 14px;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}

/* 按钮样式优化 */
.btn {
  border-radius: 4px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.btn-info {
  background-color: #17a2b8;
  border-color: #17a2b8;
}

.btn-info:hover {
  background-color: #138496;
  border-color: #117a8b;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

/* 提示信息样式 */
.alert {
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 15px;
  border: 1px solid transparent;
}

.alert-info {
  color: #155724;
  background-color: #d4edda;
  border-color: #c3e6cb;
}

.alert-success {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}

/* 加载动画 */
.fa-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>