<template>
  <div class="data-entry-container">
    <h1 class="page-title">数据录入中心</h1>
    
    <!-- 阶段导航 -->
    <div class="stage-navigation">
      <el-steps :active="currentStage" finish-status="success">
        <el-step 
          v-for="(stage, index) in stages" 
          :key="index"
          :title="stage.title"
          :description="stage.description"
        />
      </el-steps>
    </div>
    
    <!-- 录入区域 -->
    <div class="entry-content">
      <!-- 第一阶段：基础独立表 -->
      <div v-if="currentStage === 0" class="stage-content">
        <h2>第一阶段：基础独立表</h2>
        
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <span>角色管理</span>
              <el-button type="primary" @click="addRole" size="small">添加角色</el-button>
            </div>
          </template>
          <el-table :data="roles" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="角色名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editRole(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteRole(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <span>菜单分类管理</span>
              <el-button type="primary" @click="addMenuCategory" size="small">添加分类</el-button>
            </div>
          </template>
          <el-table :data="menuCategories" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="分类名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editMenuCategory(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteMenuCategory(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <span>服务分类管理</span>
              <el-button type="primary" @click="addServiceCategory" size="small">添加分类</el-button>
            </div>
          </template>
          <el-table :data="serviceCategories" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="分类名称" />
            <el-table-column prop="description" label="描述" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editServiceCategory(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteServiceCategory(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
      
      <!-- 第二阶段：依赖基础表的核心表 -->
      <div v-if="currentStage === 1" class="stage-content">
        <h2>第二阶段：依赖基础表的核心表</h2>
        
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <span>用户管理</span>
              <el-button type="primary" @click="addUser" size="small">添加用户</el-button>
            </div>
          </template>
          <el-table :data="users" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="full_name" label="姓名" />
            <el-table-column prop="department" label="部门" />
            <el-table-column prop="position" label="职位" />
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editUser(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteUser(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <el-card class="mb-4">
          <template #header>
            <div class="card-header">
              <span>菜品管理</span>
              <el-button type="primary" @click="addDish" size="small">添加菜品</el-button>
              <el-button type="success" @click="showImageUpload = true" size="small">图片识别</el-button>
            </div>
          </template>
          <el-table :data="dishes" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="菜品名称" />
            <el-table-column prop="category_name" label="分类" />
            <el-table-column prop="price" label="价格" />
            <el-table-column prop="is_available" label="状态">
              <template #default="scope">
                <el-tag :type="scope.row.is_available ? 'success' : 'danger'">
                  {{ scope.row.is_available ? '可用' : '不可用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button type="primary" size="small" @click="editDish(scope.row)">编辑</el-button>
                <el-button type="danger" size="small" @click="deleteDish(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>
      
      <!-- 第三阶段：关联表和依赖表 -->
      <div v-if="currentStage === 2" class="stage-content">
        <h2>第三阶段：关联表和依赖表</h2>
        <!-- 内容略 -->
      </div>
      
      <!-- 第四阶段：业务流程表 -->
      <div v-if="currentStage === 3" class="stage-content">
        <h2>第四阶段：业务流程表</h2>
        <!-- 内容略 -->
      </div>
      
      <!-- 第五阶段：高级业务表 -->
      <div v-if="currentStage === 4" class="stage-content">
        <h2>第五阶段：高级业务表</h2>
        <!-- 内容略 -->
      </div>
      
      <!-- 第六阶段：特殊功能表 -->
      <div v-if="currentStage === 5" class="stage-content">
        <h2>第六阶段：特殊功能表</h2>
        <!-- 内容略 -->
      </div>
    </div>
    
    <!-- 阶段控制 -->
    <div class="stage-controls">
      <el-button @click="prevStage" :disabled="currentStage === 0">上一阶段</el-button>
      <el-button @click="nextStage" :disabled="currentStage === stages.length - 1">下一阶段</el-button>
    </div>
    
    <!-- 图片上传对话框 -->
    <el-dialog
      v-model="showImageUpload"
      title="图片识别录入"
      width="600px"
    >
      <div class="image-upload-section">
        <el-upload
          class="image-uploader"
          action="#"
          :auto-upload="false"
          :on-change="handleImageChange"
          :show-file-list="false"
          accept="image/*"
        >
          <el-button type="primary">选择图片</el-button>
        </el-upload>
        
        <div v-if="selectedImage" class="image-preview">
          <img :src="selectedImage" alt="预览图片" class="preview-img" />
          <el-button type="success" @click="recognizeImage" class="mt-2">识别图片</el-button>
        </div>
        
        <div v-if="recognitionResult" class="recognition-result">
          <h3>识别结果</h3>
          <el-form :model="recognitionResult" label-width="100px">
            <el-form-item label="菜品名称">
              <el-input v-model="recognitionResult.name" />
            </el-form-item>
            <el-form-item label="菜品分类">
              <el-select v-model="recognitionResult.category_id">
                <el-option 
                  v-for="category in menuCategories" 
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="价格">
              <el-input v-model.number="recognitionResult.price" type="number" />
            </el-form-item>
            <el-form-item label="描述">
              <el-input v-model="recognitionResult.description" type="textarea" />
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="saveRecognizedDish" class="mt-2">保存菜品</el-button>
        </div>
      </div>
    </el-dialog>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="showDialog"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="formData" label-width="100px">
        <template v-if="dialogType === 'role'">
          <el-form-item label="角色名称">
            <el-input v-model="formData.name" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="formData.description" type="textarea" />
          </el-form-item>
        </template>
        
        <template v-if="dialogType === 'menuCategory'">
          <el-form-item label="分类名称">
            <el-input v-model="formData.name" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="formData.description" type="textarea" />
          </el-form-item>
        </template>
        
        <template v-if="dialogType === 'serviceCategory'">
          <el-form-item label="分类名称">
            <el-input v-model="formData.name" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="formData.description" type="textarea" />
          </el-form-item>
        </template>
        
        <template v-if="dialogType === 'user'">
          <el-form-item label="用户名">
            <el-input v-model="formData.username" />
          </el-form-item>
          <el-form-item label="姓名">
            <el-input v-model="formData.full_name" />
          </el-form-item>
          <el-form-item label="部门">
            <el-input v-model="formData.department" />
          </el-form-item>
          <el-form-item label="职位">
            <el-input v-model="formData.position" />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input v-model="formData.email" />
          </el-form-item>
          <el-form-item label="电话">
            <el-input v-model="formData.phone" />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="formData.role_id">
              <el-option 
                v-for="role in roles" 
                :key="role.id"
                :label="role.name"
                :value="role.id"
              />
            </el-select>
          </el-form-item>
        </template>
        
        <template v-if="dialogType === 'dish'">
          <el-form-item label="菜品名称">
            <el-input v-model="formData.name" />
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="formData.category_id">
              <el-option 
                v-for="category in menuCategories" 
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="价格">
            <el-input v-model.number="formData.price" type="number" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="formData.description" type="textarea" />
          </el-form-item>
          <el-form-item label="状态">
            <el-switch v-model="formData.is_available" />
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDialog = false">取消</el-button>
          <el-button type="primary" @click="saveForm">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import api from '../../utils/axios'

// 阶段定义
const stages = [
  { title: '基础独立表', description: '无外键依赖的基础表' },
  { title: '核心表', description: '依赖基础表的核心表' },
  { title: '关联表', description: '关联表和依赖表' },
  { title: '业务流程表', description: '业务流程相关表' },
  { title: '高级业务表', description: '高级业务功能表' },
  { title: '特殊功能表', description: '特殊功能相关表' }
]

const currentStage = ref(0)

// 数据状态
const roles = ref<any[]>([])
const menuCategories = ref<any[]>([])
const serviceCategories = ref<any[]>([])
const users = ref<any[]>([])
const dishes = ref<any[]>([])

// 对话框状态
const showDialog = ref(false)
const dialogTitle = ref('')
const dialogType = ref('')
const formData = reactive({})

// 图片上传状态
const showImageUpload = ref(false)
const selectedImage = ref('')
const recognitionResult = ref<any>(null)

// 阶段控制
const prevStage = () => {
  if (currentStage.value > 0) {
    currentStage.value--
  }
}

const nextStage = () => {
  if (currentStage.value < stages.length - 1) {
    currentStage.value++
  }
}

// 加载数据
const loadData = async () => {
  try {
    const rolesRes = await api.get('/api/roles')
    roles.value = rolesRes.data
    
    const categoriesRes = await api.get('/api/menu_categories')
    menuCategories.value = categoriesRes.data
    
    const serviceRes = await api.get('/api/service_categories')
    serviceCategories.value = serviceRes.data
    
    const usersRes = await api.get('/api/users')
    users.value = usersRes.data
    
    const dishesRes = await api.get('/api/dishes')
    dishes.value = dishesRes.data
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

// 对话框操作
const openDialog = (type: string, title: string, data: any = {}) => {
  dialogType.value = type
  dialogTitle.value = title
  Object.assign(formData, data)
  showDialog.value = true
}

const addRole = () => openDialog('role', '添加角色', { is_active: true })
const editRole = (row: any) => openDialog('role', '编辑角色', { ...row })
const deleteRole = async (id: number) => {
  try {
    await api.delete(`/api/roles/${id}`)
    loadData()
  } catch (error) {
    console.error('删除角色失败:', error)
  }
}

const addMenuCategory = () => openDialog('menuCategory', '添加菜单分类', { is_active: true })
const editMenuCategory = (row: any) => openDialog('menuCategory', '编辑菜单分类', { ...row })
const deleteMenuCategory = async (id: number) => {
  try {
    await api.delete(`/api/menu_categories/${id}`)
    loadData()
  } catch (error) {
    console.error('删除菜单分类失败:', error)
  }
}

const addServiceCategory = () => openDialog('serviceCategory', '添加服务分类', { is_active: true })
const editServiceCategory = (row: any) => openDialog('serviceCategory', '编辑服务分类', { ...row })
const deleteServiceCategory = async (id: number) => {
  try {
    await api.delete(`/api/service_categories/${id}`)
    loadData()
  } catch (error) {
    console.error('删除服务分类失败:', error)
  }
}

const addUser = () => openDialog('user', '添加用户', { is_active: true })
const editUser = (row: any) => openDialog('user', '编辑用户', { ...row })
const deleteUser = async (id: number) => {
  try {
    await api.delete(`/api/users/${id}`)
    loadData()
  } catch (error) {
    console.error('删除用户失败:', error)
  }
}

const addDish = () => openDialog('dish', '添加菜品', { is_available: true })
const editDish = (row: any) => openDialog('dish', '编辑菜品', { ...row })
const deleteDish = async (id: number) => {
  try {
    await api.delete(`/api/dishes/${id}`)
    loadData()
  } catch (error) {
    console.error('删除菜品失败:', error)
  }
}

// 保存表单
const saveForm = async () => {
  try {
    let url = ''
    let method = 'post'
    
    switch (dialogType.value) {
      case 'role':
        url = formData.id ? `/api/roles/${formData.id}` : '/api/roles'
        method = formData.id ? 'put' : 'post'
        break
      case 'menuCategory':
        url = formData.id ? `/api/menu_categories/${formData.id}` : '/api/menu_categories'
        method = formData.id ? 'put' : 'post'
        break
      case 'serviceCategory':
        url = formData.id ? `/api/service_categories/${formData.id}` : '/api/service_categories'
        method = formData.id ? 'put' : 'post'
        break
      case 'user':
        url = formData.id ? `/api/users/${formData.id}` : '/api/users'
        method = formData.id ? 'put' : 'post'
        break
      case 'dish':
        url = formData.id ? `/api/dishes/${formData.id}` : '/api/dishes'
        method = formData.id ? 'put' : 'post'
        break
    }
    
    await api[method](url, formData)
    showDialog.value = false
    loadData()
  } catch (error) {
    console.error('保存失败:', error)
  }
}

// 图片处理
const handleImageChange = (file: any) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    selectedImage.value = e.target?.result as string
  }
  reader.readAsDataURL(file.raw)
}

const recognizeImage = async () => {
  // 模拟图片识别
  recognitionResult.value = {
    name: '红烧肉',
    category_id: menuCategories.value[0]?.id || '',
    price: 68.00,
    description: '传统红烧肉，肥而不腻'
  }
}

const saveRecognizedDish = async () => {
  try {
    await api.post('/api/dishes', recognitionResult.value)
    showImageUpload.value = false
    selectedImage.value = ''
    recognitionResult.value = null
    loadData()
  } catch (error) {
    console.error('保存菜品失败:', error)
  }
}

// 初始化
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.data-entry-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 30px;
  color: #303133;
}

.stage-navigation {
  margin-bottom: 30px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.entry-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stage-content h2 {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #409eff;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stage-controls {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.image-upload-section {
  text-align: center;
}

.preview-img {
  max-width: 100%;
  max-height: 300px;
  margin: 10px 0;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.recognition-result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f0f9eb;
  border-radius: 4px;
}

.mb-4 {
  margin-bottom: 20px;
}

.mt-2 {
  margin-top: 10px;
}

.preview-img {
  max-width: 100%;
  max-height: 300px;
  object-fit: contain;
}
</style>
