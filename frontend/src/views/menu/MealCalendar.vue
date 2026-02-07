<template>
  <div class="meal-calendar-container">
    <h2>月子餐日历</h2>
    
    <!-- 视图切换 -->
    <div class="view-switcher mb-4">
      <el-button 
        :type="currentView === 'week' ? 'primary' : 'default'"
        @click="changeView('week')"
      >
        周视图
      </el-button>
      <el-button 
        :type="currentView === 'month' ? 'primary' : 'default'"
        @click="changeView('month')"
      >
        月视图
      </el-button>
      <el-button 
        :type="currentView === 'day' ? 'primary' : 'default'"
        @click="changeView('day')"
      >
        日视图
      </el-button>
    </div>
    
    <!-- 日期选择器 -->
    <div class="date-picker mb-4">
      <el-date-picker
        v-model="currentDate"
        type="date"
        placeholder="选择日期"
        @change="handleDateChange"
      />
      <el-button type="primary" @click="generateMealPlan">
        生成餐单
      </el-button>
    </div>
    
    <!-- 周视图 -->
    <div v-if="currentView === 'week'" class="week-view">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>{{ weekStartDate }} 至 {{ weekEndDate }}</span>
            <div>
              <el-button size="small" @click="prevWeek">上一周</el-button>
              <el-button size="small" @click="nextWeek">下一周</el-button>
            </div>
          </div>
        </template>
        
        <div class="week-table-container">
          <table class="week-table">
            <thead>
              <tr>
                <th class="meal-type-header">餐次</th>
                <th v-for="(day, index) in weekDays" :key="index" class="day-header">
                  <div class="day-date">{{ formatDate(day) }}</div>
                  <div class="day-week">{{ formatWeekday(day) }}</div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(mealType, index) in mealTypes" :key="index">
                <td class="meal-type-cell">{{ mealType.label }}</td>
                <td v-for="(day, dayIndex) in weekDays" :key="dayIndex" class="meal-cell">
                  <div v-if="getMealForDayAndType(day, mealType.value)" class="meal-item">
                    {{ getMealForDayAndType(day, mealType.value)?.name }}
                  </div>
                  <div v-else class="empty-meal">
                    <el-button size="small" type="primary" @click="addMeal(day, mealType.value)">
                      添加
                    </el-button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </el-card>
    </div>
    
    <!-- 月视图 -->
    <div v-else-if="currentView === 'month'" class="month-view">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>{{ currentYear }}年{{ currentMonth }}月</span>
            <div>
              <el-button size="small" @click="prevMonth">上个月</el-button>
              <el-button size="small" @click="nextMonth">下个月</el-button>
            </div>
          </div>
        </template>
        
        <el-calendar v-model="currentDate">
          <template #dateCell="{ date, data }">
            <div class="calendar-cell">
              <div class="cell-date">{{ data.day }}</div>
              <div class="cell-meals">
                <div v-for="(meal, index) in getMealsForDate(date)" :key="index" class="meal-tag">
                  {{ meal.mealType }}
                </div>
                <div v-if="getMealsForDate(date).length === 0" class="no-meals">
                  无餐单
                </div>
              </div>
            </div>
          </template>
        </el-calendar>
      </el-card>
    </div>
    
    <!-- 日视图 -->
    <div v-else-if="currentView === 'day'" class="day-view">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>{{ formatDate(currentDate) }} {{ formatWeekday(currentDate) }}</span>
            <div>
              <el-button size="small" @click="prevDay">前一天</el-button>
              <el-button size="small" @click="nextDay">后一天</el-button>
            </div>
          </div>
        </template>
        
        <div class="day-meals">
          <el-timeline>
            <el-timeline-item 
              v-for="(mealType, index) in mealTypes" 
              :key="index"
              :timestamp="mealType.time"
              placement="top"
            >
              <el-card :body-style="{ padding: '10px' }">
                <div class="meal-detail">
                  <h4>{{ mealType.label }}</h4>
                  <div v-if="getMealForDayAndType(currentDate, mealType.value)" class="meal-content">
                    <div class="meal-name">{{ getMealForDayAndType(currentDate, mealType.value)?.name }}</div>
                    <div class="meal-info">
                      <span class="calories">{{ getMealForDayAndType(currentDate, mealType.value)?.calories }} kcal</span>
                      <span class="weight">{{ getMealForDayAndType(currentDate, mealType.value)?.weight }} g</span>
                    </div>
                    <el-button size="small" type="primary" @click="editMeal(currentDate, mealType.value)">
                      编辑
                    </el-button>
                  </div>
                  <div v-else class="no-meal">
                    <el-button size="small" type="primary" @click="addMeal(currentDate, mealType.value)">
                      添加餐单
                    </el-button>
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-card>
    </div>
    
    <!-- 添加/编辑餐单对话框 -->
    <el-dialog
      v-model="mealDialogVisible"
      :title="isEditMeal ? '编辑餐单' : '添加餐单'"
      width="500px"
    >
      <el-form :model="mealForm" :rules="mealRules" ref="mealFormRef">
        <el-form-item label="餐单名称" prop="name">
          <el-input v-model="mealForm.name" placeholder="请输入餐单名称" />
        </el-form-item>
        <el-form-item label="卡路里" prop="calories">
          <el-input-number v-model="mealForm.calories" :min="0" :step="10" placeholder="请输入卡路里" />
        </el-form-item>
        <el-form-item label="重量" prop="weight">
          <el-input-number v-model="mealForm.weight" :min="0" :step="10" placeholder="请输入重量" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="mealForm.description"
            type="textarea"
            placeholder="请输入餐单描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="mealDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitMeal">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

// 状态管理
const currentView = ref('week') // week, month, day
const currentDate = ref(new Date())
const mealDialogVisible = ref(false)
const mealFormRef = ref<any>(null)
const isEditMeal = ref(false)

// 餐单数据
const meals = ref<any[]>([])

// 餐次配置
const mealTypes = [
  { value: 'breakfast', label: '早餐', time: '08:00' },
  { value: 'morning_snack', label: '上午茶', time: '10:00' },
  { value: 'lunch', label: '午餐', time: '12:00' },
  { value: 'afternoon_snack', label: '下午茶', time: '15:00' },
  { value: 'dinner', label: '晚餐', time: '18:00' },
  { value: 'night_snack', label: '夜宵', time: '21:00' }
]

// 餐单表单
const mealForm = ref({
  name: '',
  calories: 0,
  weight: 0,
  description: ''
})

// 验证规则
const mealRules = ref({
  name: [{ required: true, message: '请输入餐单名称', trigger: 'blur' }],
  calories: [{ required: true, message: '请输入卡路里', trigger: 'blur' }],
  weight: [{ required: true, message: '请输入重量', trigger: 'blur' }]
})

// 计算周开始和结束日期
const weekStartDate = computed(() => {
  const date = new Date(currentDate.value)
  const day = date.getDay()
  const diff = date.getDate() - day + (day === 0 ? -6 : 1) // 调整为周一为开始
  return formatDate(new Date(date.setDate(diff)))
})

const weekEndDate = computed(() => {
  const date = new Date(currentDate.value)
  const day = date.getDay()
  const diff = date.getDate() - day + (day === 0 ? 0 : 7) // 调整为周日为结束
  return formatDate(new Date(date.setDate(diff)))
})

// 计算周天数
const weekDays = computed(() => {
  const days = []
  const startDate = new Date(currentDate.value)
  const day = startDate.getDay()
  const diff = startDate.getDate() - day + (day === 0 ? -6 : 1) // 调整为周一为开始
  startDate.setDate(diff)
  
  for (let i = 0; i < 7; i++) {
    const currentDay = new Date(startDate)
    currentDay.setDate(startDate.getDate() + i)
    days.push(currentDay)
  }
  return days
})

// 计算当前年月
const currentYear = computed(() => {
  return currentDate.value.getFullYear()
})

const currentMonth = computed(() => {
  return currentDate.value.getMonth() + 1
})

// 视图切换
const changeView = (view: string) => {
  currentView.value = view
}

// 日期操作
const prevWeek = () => {
  const date = new Date(currentDate.value)
  date.setDate(date.getDate() - 7)
  currentDate.value = date
}

const nextWeek = () => {
  const date = new Date(currentDate.value)
  date.setDate(date.getDate() + 7)
  currentDate.value = date
}

const prevMonth = () => {
  const date = new Date(currentDate.value)
  date.setMonth(date.getMonth() - 1)
  currentDate.value = date
}

const nextMonth = () => {
  const date = new Date(currentDate.value)
  date.setMonth(date.getMonth() + 1)
  currentDate.value = date
}

const prevDay = () => {
  const date = new Date(currentDate.value)
  date.setDate(date.getDate() - 1)
  currentDate.value = date
}

const nextDay = () => {
  const date = new Date(currentDate.value)
  date.setDate(date.getDate() + 1)
  currentDate.value = date
}

// 日期格式化
const formatDate = (date: Date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const formatWeekday = (date: Date) => {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return weekdays[date.getDay()]
}

// 处理日期变化
const handleDateChange = () => {
  // 可以添加日期变化后的处理逻辑
}

// 生成餐单
const generateMealPlan = () => {
  // 模拟生成餐单数据
  const mockMeals = [
    { date: formatDate(currentDate.value), mealType: 'breakfast', name: '小米粥', calories: 300, weight: 200, description: '营养早餐' },
    { date: formatDate(currentDate.value), mealType: 'lunch', name: '清蒸排骨', calories: 500, weight: 300, description: '营养午餐' },
    { date: formatDate(currentDate.value), mealType: 'dinner', name: '清炒菠菜', calories: 400, weight: 250, description: '营养晚餐' }
  ]
  
  meals.value = [...meals.value, ...mockMeals]
  ElMessage.success('餐单生成成功')
}

// 获取指定日期和餐次的餐单
const getMealForDayAndType = (date: Date, mealType: string) => {
  const dateStr = formatDate(date)
  return meals.value.find(meal => meal.date === dateStr && meal.mealType === mealType)
}

// 获取指定日期的所有餐单
const getMealsForDate = (date: Date) => {
  const dateStr = formatDate(date)
  return meals.value.filter(meal => meal.date === dateStr)
}

// 添加餐单
const addMeal = (date: Date, mealType: string) => {
  isEditMeal.value = false
  mealForm.value = {
    name: '',
    calories: 0,
    weight: 0,
    description: ''
  }
  mealDialogVisible.value = true
}

// 编辑餐单
const editMeal = (date: Date, mealType: string) => {
  const meal = getMealForDayAndType(date, mealType)
  if (meal) {
    isEditMeal.value = true
    mealForm.value = { ...meal }
    mealDialogVisible.value = true
  }
}

// 提交餐单
const submitMeal = async () => {
  if (!mealFormRef.value) return
  
  await mealFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (isEditMeal.value) {
          // 编辑餐单
          const index = meals.value.findIndex(meal => 
            meal.date === mealForm.value.date && meal.mealType === mealForm.value.mealType
          )
          if (index !== -1) {
            meals.value[index] = { ...mealForm.value }
          }
          ElMessage.success('餐单更新成功')
        } else {
          // 新增餐单
          meals.value.push({ ...mealForm.value })
          ElMessage.success('餐单添加成功')
        }
        mealDialogVisible.value = false
      } catch (error) {
        ElMessage.error('操作失败')
        console.error('Error submitting meal:', error)
      }
    }
  })
}

// 初始化数据
const initData = () => {
  // 模拟初始数据
  const today = new Date()
  const mockData = [
    { date: formatDate(today), mealType: 'breakfast', name: '小米粥', calories: 300, weight: 200, description: '营养早餐' },
    { date: formatDate(today), mealType: 'lunch', name: '清蒸排骨', calories: 500, weight: 300, description: '营养午餐' },
    { date: formatDate(today), mealType: 'dinner', name: '清炒菠菜', calories: 400, weight: 250, description: '营养晚餐' }
  ]
  meals.value = mockData
}

onMounted(() => {
  initData()
})
</script>

<style scoped>
.meal-calendar-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.view-switcher {
  display: flex;
  gap: 10px;
}

.date-picker {
  display: flex;
  gap: 10px;
  align-items: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 周视图样式 */
.week-table-container {
  overflow-x: auto;
}

.week-table {
  width: 100%;
  border-collapse: collapse;
}

.week-table th,
.week-table td {
  border: 1px solid #ebeef5;
  padding: 10px;
  text-align: center;
}

.meal-type-header {
  width: 100px;
  background-color: #f5f7fa;
  font-weight: bold;
}

.day-header {
  min-width: 120px;
  background-color: #f5f7fa;
}

.day-date {
  font-weight: bold;
}

.day-week {
  font-size: 12px;
  color: #909399;
}

.meal-type-cell {
  background-color: #f5f7fa;
  font-weight: bold;
}

.meal-cell {
  min-height: 100px;
  vertical-align: top;
}

.meal-item {
  background-color: #ecf5ff;
  padding: 5px;
  border-radius: 4px;
  margin-bottom: 5px;
}

.empty-meal {
  margin-top: 20px;
}

/* 月视图样式 */
.month-view {
  margin-top: 20px;
}

.calendar-cell {
  height: 100px;
  padding: 5px;
}

.cell-date {
  font-weight: bold;
  margin-bottom: 5px;
}

.cell-meals {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.meal-tag {
  font-size: 12px;
  background-color: #ecf5ff;
  padding: 2px 5px;
  border-radius: 3px;
  display: inline-block;
}

.no-meals {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

/* 日视图样式 */
.day-view {
  margin-top: 20px;
}

.day-meals {
  margin-top: 20px;
}

.meal-detail {
  margin-top: 10px;
}

.meal-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 5px;
}

.meal-info {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
}

.no-meal {
  margin-top: 20px;
}

/* 对话框样式 */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .meal-calendar-container {
    padding: 10px;
  }
  
  .view-switcher {
    flex-direction: column;
  }
  
  .date-picker {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .week-table th,
  .week-table td {
    padding: 5px;
  }
  
  .day-header {
    min-width: 80px;
  }
  
  .calendar-cell {
    height: 80px;
  }
}
</style>