<template>
  <div class="health-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>健康记录</span>
          <el-button type="primary" @click="openHealthRecordForm">
            <el-icon><Plus /></el-icon> 新增健康记录
          </el-button>
        </div>
      </template>
      
      <!-- 健康记录列表 -->
      <el-table :data="healthRecords" style="width: 100%">
        <el-table-column prop="id" label="记录ID" width="80" />
        <el-table-column prop="record_type" label="记录类型" />
        <el-table-column prop="record_date" label="记录日期" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="summary" label="摘要" />
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="viewHealthRecord(scope.row)">
              查看
            </el-button>
            <el-button type="danger" size="small" @click="deleteHealthRecord(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 新增/编辑健康记录对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑健康记录' : '新增健康记录'"
      width="600px"
    >
      <el-form :model="healthRecordForm" :rules="rules" ref="formRef">
        <el-form-item label="记录类型" prop="record_type">
          <el-select v-model="healthRecordForm.record_type" placeholder="选择记录类型">
            <el-option label="产后检查" value="postpartum_check" />
            <el-option label="新生儿检查" value="newborn_check" />
            <el-option label="体温记录" value="temperature" />
            <el-option label="血压记录" value="blood_pressure" />
            <el-option label="血糖记录" value="blood_sugar" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="记录日期" prop="record_date">
          <el-date-picker
            v-model="healthRecordForm.record_date"
            type="date"
            placeholder="选择记录日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="healthRecordForm.title" placeholder="请输入记录标题" />
        </el-form-item>
        <el-form-item label="详细内容" prop="content">
          <el-input
            v-model="healthRecordForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入详细内容"
          />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="healthRecordForm.notes"
            type="textarea"
            :rows="2"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitHealthRecord">确认</el-button>
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
const healthRecords = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)
const isEdit = ref(false)

// 健康记录表单
const healthRecordForm = ref({
  record_type: '',
  record_date: '',
  title: '',
  content: '',
  notes: ''
})

// 验证规则
const rules = ref({
  record_type: [{ required: true, message: '请选择记录类型', trigger: 'change' }],
  record_date: [{ required: true, message: '请选择记录日期', trigger: 'change' }],
  title: [{ required: true, message: '请输入记录标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入详细内容', trigger: 'blur' }]
})

// 获取健康记录列表
const fetchHealthRecords = async () => {
  try {
    const response = await axios.get('/api/health_records')
    healthRecords.value = response.data
  } catch (error) {
    ElMessage.error('获取健康记录失败')
    console.error('Error fetching health records:', error)
  }
}

// 打开健康记录表单
const openHealthRecordForm = (record?: any) => {
  if (record) {
    isEdit.value = true
    healthRecordForm.value = { ...record }
  } else {
    isEdit.value = false
    healthRecordForm.value = {
      record_type: '',
      record_date: '',
      title: '',
      content: '',
      notes: ''
    }
  }
  dialogVisible.value = true
}

// 提交健康记录
const submitHealthRecord = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        if (isEdit.value) {
          // 编辑健康记录
          await axios.put(`/api/health_records/${healthRecordForm.value.id}`, healthRecordForm.value)
          ElMessage.success('记录更新成功')
        } else {
          // 新增健康记录
          await axios.post('/api/health_records', healthRecordForm.value)
          ElMessage.success('记录创建成功')
        }
        dialogVisible.value = false
        fetchHealthRecords()
      } catch (error) {
        ElMessage.error('操作失败')
        console.error('Error submitting health record:', error)
      }
    }
  })
}

// 查看健康记录详情
const viewHealthRecord = (record: any) => {
  // 实现查看健康记录详情功能
  ElMessage.info('查看健康记录详情功能开发中')
}

// 删除健康记录
const deleteHealthRecord = (recordId: number) => {
  ElMessageBox.confirm('确定要删除该健康记录吗？', '删除记录', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await axios.delete(`/api/health_records/${recordId}`)
      ElMessage.success('记录删除成功')
      fetchHealthRecords()
    } catch (error) {
      ElMessage.error('删除失败')
      console.error('Error deleting health record:', error)
    }
  })
}

// 页面加载时获取数据
onMounted(() => {
  fetchHealthRecords()
})
</script>

<style scoped>
.health-container {
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