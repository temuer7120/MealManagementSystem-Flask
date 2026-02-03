<template>
  <div class="confinement-meal-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>月子餐计划</span>
          <el-button type="primary" @click="openMealPlanForm">
            <el-icon><Plus /></el-icon> 新增计划
          </el-button>
        </div>
      </template>
      
      <!-- 计划列表 -->
      <el-table :data="mealPlans" style="width: 100%">
        <el-table-column prop="id" label="计划ID" width="80" />
        <el-table-column prop="name" label="计划名称" />
        <el-table-column prop="start_date" label="开始日期" />
        <el-table-column prop="end_date" label="结束日期" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewMealPlan(scope.row)">
              查看
            </el-button>
            <el-button type="danger" size="small" @click="deleteMealPlan(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 新增/编辑计划对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑月子餐计划' : '新增月子餐计划'"
      width="600px"
    >
      <el-form :model="mealPlanForm" :rules="rules" ref="formRef">
        <el-form-item label="计划名称" prop="name">
          <el-input v-model="mealPlanForm.name" placeholder="请输入计划名称" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker
            v-model="mealPlanForm.start_date"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker
            v-model="mealPlanForm.end_date"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="mealPlanForm.description"
            type="textarea"
            placeholder="请输入计划描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitMealPlan">确认</el-button>
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

// 状态管理
const mealPlans = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)
const isEdit = ref(false)

// 表单数据
const mealPlanForm = ref({
  name: '',
  start_date: '',
  end_date: '',
  description: ''
})

// 验证规则
const rules = ref({
  name: [{ required: true, message: '请输入计划名称', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
})

// 获取月子餐计划列表
const fetchMealPlans = async () => {
  try {
    const response = await axios.get('/api/confinement_meal_plans')
    mealPlans.value = response.data
  } catch (error) {
    ElMessage.error('获取月子餐计划失败')
    console.error('Error fetching meal plans:', error)
  }
}

// 打开计划表单
const openMealPlanForm = (plan?: any) => {
  if (plan) {
    isEdit.value = true
    mealPlanForm.value = { ...plan }
  } else {
    isEdit.value = false
    mealPlanForm.value = {
      name: '',
      start_date: '',
      end_date: '',
      description: ''
    }
  }
  dialogVisible.value = true
}

// 提交计划
const submitMealPlan = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (isEdit.value) {
          // 编辑计划
          await axios.put(`/api/confinement_meal_plans/${mealPlanForm.value.id}`, mealPlanForm.value)
          ElMessage.success('计划更新成功')
        } else {
          // 新增计划
          await axios.post('/api/confinement_meal_plans', mealPlanForm.value)
          ElMessage.success('计划创建成功')
        }
        dialogVisible.value = false
        fetchMealPlans()
      } catch (error) {
        ElMessage.error('操作失败')
        console.error('Error submitting meal plan:', error)
      }
    }
  })
}

// 查看计划详情
const viewMealPlan = (plan: any) => {
  // 实现查看计划详情功能
  ElMessage.info('查看计划详情功能开发中')
}

// 删除计划
const deleteMealPlan = (planId: number) => {
  ElMessageBox.confirm('确定要删除该计划吗？', '删除计划', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await axios.delete(`/api/confinement_meal_plans/${planId}`)
      ElMessage.success('计划删除成功')
      fetchMealPlans()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('Error deleting meal plan:', error)
    }
  })
}

// 页面加载时获取数据
onMounted(() => {
  fetchMealPlans()
})
</script>

<style scoped>
.confinement-meal-container {
  padding: 20px;
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