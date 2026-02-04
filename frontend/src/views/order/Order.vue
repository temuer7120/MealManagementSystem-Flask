<template>
  <div class="order-container">
    <h2>订单管理</h2>
    <!-- 订单列表 -->
    <el-card shadow="hover" class="order-card">
      <template #header>
        <div class="card-header">
          <span>订单列表</span>
          <el-button type="primary" @click="openOrderForm">
            <el-icon><Plus /></el-icon> 新增订单
          </el-button>
        </div>
      </template>
      
      <el-table :data="orders" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="order_number" label="订单编号" width="180" />
        <el-table-column prop="customer_name" label="客户姓名" />
        <el-table-column prop="total_amount" label="订单金额" width="120" />
        <el-table-column prop="order_date" label="下单日期" width="180" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editOrder(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteOrder(scope.row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 订单表单对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="订单管理"
      width="500px"
    >
      <el-form :model="orderForm" :rules="rules" ref="formRef">
        <el-form-item label="客户" prop="customer_id">
          <el-select v-model="orderForm.customer_id" placeholder="请选择客户">
            <el-option
              v-for="customer in customers"
              :key="customer.id"
              :label="customer.name"
              :value="customer.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="订单金额" prop="total_amount">
          <el-input-number v-model="orderForm.total_amount" :min="0" :step="0.01" placeholder="请输入订单金额" />
        </el-form-item>
        <el-form-item label="下单日期" prop="order_date">
          <el-date-picker
            v-model="orderForm.order_date"
            type="datetime"
            placeholder="选择下单日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="orderForm.status" placeholder="请选择状态">
            <el-option label="待处理" value="pending" />
            <el-option label="处理中" value="processing" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitOrder">保存</el-button>
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

const orders = ref<any[]>([])
const customers = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)

const orderForm = ref({
  id: '',
  order_number: '',
  customer_id: '',
  total_amount: 0,
  order_date: '',
  status: 'pending'
})

const rules = ref({
  customer_id: [{ required: true, message: '请选择客户', trigger: 'change' }],
  total_amount: [{ required: true, message: '请输入订单金额', trigger: 'blur' }],
  order_date: [{ required: true, message: '请选择下单日期', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
})

const getStatusType = (status: string) => {
  switch (status) {
    case 'pending':
      return 'warning'
    case 'processing':
      return 'info'
    case 'completed':
      return 'success'
    case 'cancelled':
      return 'danger'
    default:
      return 'default'
  }
}

const fetchOrders = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    orders.value = [
      {
        id: 1,
        order_number: 'ORD-20260204-001',
        customer_id: 1,
        customer_name: '张女士',
        total_amount: 380,
        order_date: '2026-02-04 10:30:00',
        status: 'completed'
      },
      {
        id: 2,
        order_number: 'ORD-20260204-002',
        customer_id: 2,
        customer_name: '李女士',
        total_amount: 420,
        order_date: '2026-02-04 09:15:00',
        status: 'completed'
      },
      {
        id: 3,
        order_number: 'ORD-20260204-003',
        customer_id: 3,
        customer_name: '王女士',
        total_amount: 560,
        order_date: '2026-02-04 08:45:00',
        status: 'processing'
      }
    ]
  } catch (error) {
    console.error('Error fetching orders:', error)
    ElMessage.error('获取订单列表失败')
  }
}

const fetchCustomers = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    customers.value = [
      { id: 1, name: '张女士' },
      { id: 2, name: '李女士' },
      { id: 3, name: '王女士' }
    ]
  } catch (error) {
    console.error('Error fetching customers:', error)
    ElMessage.error('获取客户列表失败')
  }
}

const openOrderForm = () => {
  const today = new Date()
  const orderNumber = `ORD-${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}-${String(orders.value.length + 1).padStart(3, '0')}`
  
  orderForm.value = {
    id: '',
    order_number: orderNumber,
    customer_id: '',
    total_amount: 0,
    order_date: today.toISOString().slice(0, 19).replace('T', ' '),
    status: 'pending'
  }
  dialogVisible.value = true
}

const editOrder = (order: any) => {
  orderForm.value = { ...order }
  dialogVisible.value = true
}

const deleteOrder = (orderId: number) => {
  ElMessageBox.confirm('确定要删除该订单吗？', '删除订单', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 模拟删除，实际项目中应该调用后端API
      orders.value = orders.value.filter(order => order.id !== orderId)
      ElMessage.success('订单删除成功')
    } catch (error) {
      console.error('Error deleting order:', error)
      ElMessage.error('删除订单失败')
    }
  })
}

const submitOrder = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        // 获取客户姓名
        const customer = customers.value.find(cust => cust.id === orderForm.value.customer_id)
        const customerName = customer ? customer.name : '未知客户'
        
        if (orderForm.value.id) {
          // 编辑订单
          const index = orders.value.findIndex(order => order.id === orderForm.value.id)
          if (index !== -1) {
            orders.value[index] = {
              ...orderForm.value,
              customer_name: customerName
            }
          }
          ElMessage.success('订单更新成功')
        } else {
          // 新增订单
          const newOrder = {
            ...orderForm.value,
            id: orders.value.length + 1,
            customer_name: customerName
          }
          orders.value.push(newOrder)
          ElMessage.success('订单创建成功')
        }
        dialogVisible.value = false
      } catch (error) {
        console.error('Error submitting order:', error)
        ElMessage.error('保存订单失败')
      }
    }
  })
}

onMounted(() => {
  fetchOrders()
  fetchCustomers()
})
</script>

<style scoped>
.order-container {
  padding: 20px;
}

.order-card {
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