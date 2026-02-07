<template>
  <div class="menu-container">
    <h2 class="page-title">
      <i class="fas fa-utensils"></i> 餐单管理
    </h2>
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
        <el-table-column prop="total_weight" label="总重量" width="100" />
        <el-table-column prop="total_calories" label="总热量" width="100" />
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
      width="900px"
    >
      <el-form :model="menuForm" :rules="rules" ref="formRef">
        <!-- 基本信息 -->
        <el-card class="form-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>
          
          <div class="form-row">
            <el-form-item label="餐单名称" prop="name" class="form-item">
              <el-input v-model="menuForm.name" placeholder="请输入餐单名称" />
            </el-form-item>
            <el-form-item label="产后阶段" prop="postpartum_period" class="form-item">
              <el-select v-model="menuForm.postpartum_period" placeholder="请选择产后阶段">
                <el-option label="第一周" value="week1" />
                <el-option label="第二周" value="week2" />
                <el-option label="第三周" value="week3" />
                <el-option label="第四周及以上" value="week4+" />
              </el-select>
            </el-form-item>
          </div>
          
          <el-form-item label="描述" prop="description" class="form-item">
            <el-input
              v-model="menuForm.description"
              type="textarea"
              placeholder="请输入餐单描述"
              rows="3"
            />
          </el-form-item>
          
          <div class="form-row">
            <el-form-item label="状态" class="form-item">
              <el-switch v-model="menuForm.is_active" />
            </el-form-item>
          </div>
        </el-card>
        
        <!-- 菜品组合 -->
        <el-card class="form-card" shadow="hover" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>菜品组合</span>
              <el-button type="info" size="small" @click="autoFillMenu" class="auto-fill-btn">
                <el-icon><Star /></el-icon> 自动填充
              </el-button>
            </div>
          </template>
          
          <div class="dish-combination">
            <!-- 菜品库 -->
            <div class="dish-library">
              <div class="library-header">
                <h4>菜品库</h4>
                <el-input
                  v-model="dishSearch"
                  placeholder="搜索菜品"
                  class="dish-search"
                >
                  <template #prefix>
                    <el-icon><Search /></el-icon>
                  </template>
                </el-input>
              </div>
              <div class="dish-items">
                <div 
                  v-for="dish in filteredDishes" 
                  :key="dish.id"
                  class="dish-item"
                  @click="addDish(dish)"
                  @mouseenter="$event.target.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)'"
                  @mouseleave="$event.target.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.1)'"
                >
                  <div class="dish-info">
                    <span class="dish-name">{{ dish.name }}</span>
                    <span class="dish-price">{{ dish.price }}元</span>
                  </div>
                  <div class="dish-nutrition">
                    <span class="nutrition-item">热量: {{ dish.total_calories }}kcal</span>
                  </div>
                </div>
                <div v-if="filteredDishes.length === 0" class="empty-dishes">
                  <el-icon><Warning /></el-icon>
                  <p>未找到匹配的菜品</p>
                </div>
              </div>
            </div>
            
            <!-- 菜单菜品 -->
            <div class="menu-dishes">
              <div class="menu-header">
                <h4>菜单菜品</h4>
                <div class="menu-summary">
                  <el-tag size="small" class="summary-tag">
                    总重量: {{ menuSummary.totalWeight }}g
                  </el-tag>
                  <el-tag size="small" class="summary-tag">
                    总热量: {{ menuSummary.totalCalories }}kcal
                  </el-tag>
                  <el-tag size="small" class="summary-tag">
                    总价: {{ menuSummary.totalPrice }}元
                  </el-tag>
                </div>
              </div>
              
              <div class="menu-dish-list">
                <div 
                  v-for="(dish, index) in menuForm.dishes" 
                  :key="index"
                  class="menu-dish-item"
                >
                  <div class="dish-details">
                    <span class="dish-name">{{ dish.name }}</span>
                    <div class="dish-meta">
                      <span>{{ dish.weight }}g</span>
                      <span>{{ dish.price }}元</span>
                      <span>{{ dish.total_calories }}kcal</span>
                    </div>
                  </div>
                  <el-button type="danger" size="small" @click="removeDish(index)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </div>
                <div v-if="menuForm.dishes.length === 0" class="empty-menu">
                  <el-icon class="empty-icon"><Plus /></el-icon>
                  <p>从左侧点击添加菜品到菜单</p>
                </div>
              </div>
            </div>
          </div>
        </el-card>
        
        <!-- 禁忌检测 -->
        <el-card class="form-card" shadow="hover" style="margin-top: 20px;">
          <template #header>
            <div class="card-header">
              <span>禁忌检测</span>
            </div>
          </template>
          
          <div class="taboo-detection">
            <el-button type="primary" size="small" @click="checkTaboo" class="check-taboo-btn">
              <el-icon><Check /></el-icon> 检测禁忌
            </el-button>
            
            <div v-if="tabooResult" class="taboo-result">
              <div v-if="tabooResult.hasTaboo" class="taboo-warning">
                <el-alert
                  title="禁忌警告"
                  type="warning"
                  :description="tabooResult.warningMessage"
                  show-icon
                  :closable="false"
                  class="taboo-alert"
                />
                <div class="alternative-dishes" v-if="tabooResult.alternatives.length > 0">
                  <h5>推荐替代菜品:</h5>
                  <div class="alternative-list">
                    <div 
                      v-for="dish in tabooResult.alternatives" 
                      :key="dish.id"
                      class="alternative-item"
                      @click="replaceDish(tabooResult.tabooDishId, dish)"
                    >
                      <span>{{ dish.name }}</span>
                      <el-button type="primary" size="small">替换</el-button>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="taboo-safe">
                <el-alert
                  title="检测通过"
                  type="success"
                  description="该菜单未检测到禁忌菜品"
                  show-icon
                  :closable="false"
                  class="taboo-alert"
                />
              </div>
            </div>
          </div>
        </el-card>
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
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, Check, Star, Search, Warning } from '@element-plus/icons-vue'
import axios from 'axios'

const menus = ref<any[]>([])
const dishes = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)
const dishSearch = ref('')
const tabooResult = ref<any>(null)

const menuForm = ref({
  id: '',
  name: '',
  description: '',
  price: 0,
  total_weight: 0,
  total_calories: 0,
  is_active: true,
  postpartum_period: '',
  dishes: []
})

const rules = ref({
  name: [{ required: true, message: '请输入餐单名称', trigger: 'blur' }],
  postpartum_period: [{ required: true, message: '请选择产后阶段', trigger: 'blur' }]
})

// 过滤后的菜品列表
const filteredDishes = computed(() => {
  if (!dishSearch.value) {
    return dishes.value
  }
  return dishes.value.filter(dish => 
    dish.name.toLowerCase().includes(dishSearch.value.toLowerCase())
  )
})

// 菜单汇总信息
const menuSummary = computed(() => {
  let totalWeight = 0
  let totalCalories = 0
  let totalPrice = 0
  
  menuForm.value.dishes.forEach((dish: any) => {
    totalWeight += dish.weight || 0
    totalCalories += dish.total_calories || 0
    totalPrice += dish.price || 0
  })
  
  return {
    totalWeight: totalWeight,
    totalCalories: totalCalories,
    totalPrice: totalPrice
  }
})

// 获取菜单列表
const fetchMenus = async () => {
  try {
    // 从后端API获取菜单列表
    const response = await axios.get('/api/menus')
    menus.value = response.data
  } catch (error) {
    console.error('Error fetching menus:', error)
    ElMessage.error('获取餐单列表失败')
  }
}

// 获取菜品列表
const fetchDishes = async () => {
  try {
    // 从后端API获取菜品列表
    const response = await axios.get('/api/dishes')
    dishes.value = response.data
  } catch (error) {
    console.error('Error fetching dishes:', error)
    ElMessage.error('获取菜品列表失败')
  }
}

// 打开菜单表单
const openMenuForm = () => {
  menuForm.value = {
    id: '',
    name: '',
    description: '',
    price: 0,
    total_weight: 0,
    total_calories: 0,
    is_active: true,
    postpartum_period: '',
    dishes: []
  }
  tabooResult.value = null
  dialogVisible.value = true
}

// 编辑菜单
const editMenu = (menu: any) => {
  menuForm.value = {
    ...menu,
    dishes: menu.dishes || []
  }
  tabooResult.value = null
  dialogVisible.value = true
}

// 删除菜单
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

// 添加菜品到菜单
const addDish = (dish: any) => {
  // 检查菜品是否已存在
  const existingIndex = menuForm.value.dishes.findIndex(
    (item: any) => item.id === dish.id
  )
  if (existingIndex === -1) {
    menuForm.value.dishes.push({
      ...dish
    })
    ElMessage.success(`已添加菜品: ${dish.name}`)
  } else {
    ElMessage.warning('该菜品已存在于菜单中')
  }
}

// 从菜单中删除菜品
const removeDish = (index: number) => {
  const removedDish = menuForm.value.dishes[index]
  menuForm.value.dishes.splice(index, 1)
  ElMessage.success(`已移除菜品: ${removedDish.name}`)
}

// 检测禁忌
const checkTaboo = () => {
  if (menuForm.value.dishes.length === 0) {
    ElMessage.warning('请先添加菜品到菜单')
    return
  }
  
  const postpartumPeriod = menuForm.value.postpartum_period
  let hasTaboo = false
  let warningMessage = ''
  let tabooDishId = null
  let alternatives = []
  
  // 检测每个菜品是否符合产后阶段
  menuForm.value.dishes.forEach((dish: any) => {
    if (postpartumPeriod === 'week1' && dish.not_suitable_for.includes('产后第一周')) {
      hasTaboo = true
      warningMessage = `菜品 "${dish.name}" 不适合产后第一周食用`
      tabooDishId = dish.id
      // 查找适合产后第一周的替代菜品
      alternatives = dishes.value.filter((d: any) => 
        d.suitable_for.includes('产后第一周') && d.id !== dish.id
      )
    } else if (postpartumPeriod === 'week2' && dish.not_suitable_for.includes('产后第二周')) {
      hasTaboo = true
      warningMessage = `菜品 "${dish.name}" 不适合产后第二周食用`
      tabooDishId = dish.id
      // 查找适合产后第二周的替代菜品
      alternatives = dishes.value.filter((d: any) => 
        d.suitable_for.includes('产后第二周') && d.id !== dish.id
      )
    } else if (postpartumPeriod === 'week3' && dish.not_suitable_for.includes('产后第三周')) {
      hasTaboo = true
      warningMessage = `菜品 "${dish.name}" 不适合产后第三周食用`
      tabooDishId = dish.id
      // 查找适合产后第三周的替代菜品
      alternatives = dishes.value.filter((d: any) => 
        d.suitable_for.includes('产后第三周') && d.id !== dish.id
      )
    }
  })
  
  tabooResult.value = {
    hasTaboo: hasTaboo,
    warningMessage: warningMessage,
    tabooDishId: tabooDishId,
    alternatives: alternatives
  }
}

// 替换禁忌菜品
const replaceDish = (tabooDishId: number, newDish: any) => {
  const index = menuForm.value.dishes.findIndex(
    (dish: any) => dish.id === tabooDishId
  )
  if (index !== -1) {
    menuForm.value.dishes[index] = { ...newDish }
    ElMessage.success(`已替换菜品为: ${newDish.name}`)
    // 重新检测禁忌
    checkTaboo()
  }
}

// 自动填充菜单
const autoFillMenu = () => {
  const postpartumPeriod = menuForm.value.postpartum_period
  if (!postpartumPeriod) {
    ElMessage.warning('请先选择产后阶段')
    return
  }
  
  // 根据产后阶段自动填充适合的菜品
  let suitableDishes = []
  
  if (postpartumPeriod === 'week1') {
    suitableDishes = dishes.value.filter((d: any) => 
      d.suitable_for.includes('产后第一周')
    )
  } else if (postpartumPeriod === 'week2') {
    suitableDishes = dishes.value.filter((d: any) => 
      d.suitable_for.includes('产后第二周')
    )
  } else if (postpartumPeriod === 'week3') {
    suitableDishes = dishes.value.filter((d: any) => 
      d.suitable_for.includes('产后第三周')
    )
  } else if (postpartumPeriod === 'week4+') {
    suitableDishes = dishes.value.filter((d: any) => 
      d.suitable_for.includes('第四周') || d.suitable_for.includes('以上')
    )
  }
  
  // 最多选择3个菜品
  suitableDishes = suitableDishes.slice(0, 3)
  menuForm.value.dishes = suitableDishes
  ElMessage.success('已自动填充适合的菜品')
}

// 提交菜单
const submitMenu = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 计算菜单汇总信息
        const summary = menuSummary.value
        menuForm.value.price = summary.totalPrice
        menuForm.value.total_weight = summary.totalWeight
        menuForm.value.total_calories = summary.totalCalories
        
        if (menuForm.value.id) {
          // 编辑菜单
          const index = menus.value.findIndex(menu => menu.id === menuForm.value.id)
          if (index !== -1) {
            menus.value[index] = { ...menuForm.value }
          }
          ElMessage.success('餐单更新成功')
        } else {
          // 新增菜单
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
  fetchDishes()
})
</script>

<style scoped>
.menu-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.menu-card {
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

/* 表单样式 */
.form-card {
  border-radius: 8px;
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

/* 菜品组合区域 */
.dish-combination {
  display: flex;
  gap: 20px;
  min-height: 400px;
}

.dish-library {
  flex: 1;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #ebeef5;
}

.library-header {
  margin-bottom: 16px;
}

.library-header h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.dish-search {
  width: 100%;
  margin-bottom: 16px;
}

.dish-items {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.dish-item {
  background-color: #ffffff;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.dish-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.dish-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.dish-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.dish-price {
  font-size: 12px;
  color: #67c23a;
  font-weight: 500;
}

.dish-nutrition {
  font-size: 12px;
  color: #909399;
}

.nutrition-item {
  margin-right: 12px;
}

.empty-dishes {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #909399;
  text-align: center;
}

.empty-dishes i {
  font-size: 32px;
  margin-bottom: 12px;
}

/* 菜单菜品区域 */
.menu-dishes {
  flex: 1;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  border: 1px solid #ebeef5;
}

.menu-header {
  margin-bottom: 16px;
}

.menu-header h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.menu-summary {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.summary-tag {
  border-radius: 4px;
  font-size: 12px;
}

.menu-dish-list {
  max-height: 300px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.menu-dish-item {
  background-color: #ffffff;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  padding: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.menu-dish-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  background-color: #ffffff;
}

.dish-details {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.dish-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: #909399;
}

.empty-menu {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #909399;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 12px;
  opacity: 0.5;
}

/* 禁忌检测区域 */
.taboo-detection {
  padding: 16px 0;
}

.check-taboo-btn {
  margin-bottom: 16px;
}

.taboo-result {
  margin-top: 16px;
}

.taboo-alert {
  margin-bottom: 16px;
}

.alternative-dishes {
  margin-top: 16px;
}

.alternative-dishes h5 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 500;
  color: #303133;
}

.alternative-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alternative-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #f8f9fa;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.alternative-item:hover {
  background-color: #ecf5ff;
  border-color: #409EFF;
}

/* 自动填充按钮 */
.auto-fill-btn {
  border-radius: 4px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .dish-combination {
    flex-direction: column;
    min-height: 600px;
  }
  
  .dish-library,
  .menu-dishes {
    min-height: 300px;
  }
}

@media (max-width: 768px) {
  .menu-container {
    padding: 12px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
  
  .dish-combination {
    flex-direction: column;
  }
  
  .menu-dish-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .dish-details {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .menu-summary {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>