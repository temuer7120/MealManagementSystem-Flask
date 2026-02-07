<template>
  <div class="order-container">
    <h2 class="page-title">
      <i class="fas fa-shopping-cart"></i> 订单管理
    </h2>
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
        <el-table-column prop="menu_name" label="菜单名称" />
        <el-table-column prop="total_amount" label="订单金额" width="120" />
        <el-table-column prop="total_weight" label="总重量" width="100" />
        <el-table-column prop="total_calories" label="总热量" width="100" />
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
      width="700px"
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
        
        <el-form-item label="菜单" prop="menu_id">
          <el-select v-model="orderForm.menu_id" placeholder="请选择菜单" @change="handleMenuChange">
            <el-option
              v-for="menu in menus"
              :key="menu.id"
              :label="menu.name"
              :value="menu.id"
            />
          </el-select>
        </el-form-item>
        
        <!-- 菜单信息 -->
        <el-card v-if="selectedMenu" shadow="hover" class="menu-info-card">
          <template #header>
            <div class="card-header">
              <span>菜单信息</span>
            </div>
          </template>
          <div class="menu-info">
            <div class="menu-info-item">
              <span class="label">菜单名称：</span>
              <span>{{ selectedMenu.name }}</span>
            </div>
            <div class="menu-info-item">
              <span class="label">描述：</span>
              <span>{{ selectedMenu.description }}</span>
            </div>
            <div class="menu-info-item">
              <span class="label">总重量：</span>
              <span>{{ selectedMenu.total_weight }}g</span>
            </div>
            <div class="menu-info-item">
              <span class="label">总热量：</span>
              <span>{{ selectedMenu.total_calories }}kcal</span>
            </div>
            <div class="menu-info-item">
              <span class="label">价格：</span>
              <span>{{ selectedMenu.price }}元</span>
            </div>
            <div class="menu-info-item">
              <span class="label">产后阶段：</span>
              <span>{{ getPostpartumPeriodText(selectedMenu.postpartum_period) }}</span>
            </div>
          </div>
        </el-card>
        
        <!-- 禁忌检测 -->
        <el-card v-if="selectedMenu" shadow="hover" class="taboo-detection-card">
          <template #header>
            <div class="card-header">
              <span>禁忌检测</span>
              <el-button type="primary" size="small" @click="checkTaboo">
                <el-icon><Check /></el-icon> 检测禁忌
              </el-button>
            </div>
          </template>
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
            </div>
            <div v-else class="taboo-safe">
              <el-alert
                title="检测通过"
                type="success"
                description="该菜单未检测到禁忌"
                show-icon
                :closable="false"
                class="taboo-alert"
              />
            </div>
          </div>
        </el-card>
        
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
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Check } from '@element-plus/icons-vue'
import axios from 'axios'

const orders = ref<any[]>([])
const customers = ref<any[]>([])
const menus = ref<any[]>([])
const dialogVisible = ref(false)
const formRef = ref<any>(null)
const selectedMenu = ref<any>(null)
const tabooResult = ref<any>(null)

const orderForm = ref({
  id: '',
  order_number: '',
  customer_id: '',
  menu_id: '',
  total_amount: 0,
  total_weight: 0,
  total_calories: 0,
  order_date: '',
  status: 'pending'
})

const rules = ref({
  customer_id: [{ required: true, message: '请选择客户', trigger: 'change' }],
  menu_id: [{ required: true, message: '请选择菜单', trigger: 'change' }],
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

const getPostpartumPeriodText = (period: string) => {
  switch (period) {
    case 'week1':
      return '产后第一周'
    case 'week2':
      return '产后第二周'
    case 'week3':
      return '产后第三周'
    case 'week4+':
      return '产后第四周及以上'
    default:
      return period
  }
}

const fetchOrders = async () => {
  try {
    // 从后端API获取订单列表
    const response = await axios.get('/api/orders')
    orders.value = response.data
  } catch (error) {
    console.error('Error fetching orders:', error)
    ElMessage.error('获取订单列表失败')
  }
}

const fetchCustomers = async () => {
  try {
    const response = await axios.get('/api/customers')
    customers.value = response.data
  } catch (error) {
    console.error('Error fetching customers:', error)
    ElMessage.error('获取客户列表失败')
  }
}

const fetchMenus = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    menus.value = [
      {
        id: 1,
        name: '基础月子餐',
        description: '适合产后第一周的基础调理餐',
        price: 380,
        total_weight: 600,
        total_calories: 800,
        is_active: true,
        postpartum_period: 'week1'
      },
      {
        id: 2,
        name: '进阶月子餐',
        description: '适合产后第二周的营养补充餐',
        price: 420,
        total_weight: 650,
        total_calories: 900,
        is_active: true,
        postpartum_period: 'week2'
      },
      {
        id: 3,
        name: '高级月子餐',
        description: '适合产后第三周的全面恢复餐',
        price: 560,
        total_weight: 700,
        total_calories: 1000,
        is_active: true,
        postpartum_period: 'week3'
      }
    ]
  } catch (error) {
    console.error('Error fetching menus:', error)
    ElMessage.error('获取菜单列表失败')
  }
}

const handleMenuChange = (menuId: number) => {
  const menu = menus.value.find(m => m.id === menuId)
  if (menu) {
    selectedMenu.value = menu
    orderForm.value.total_amount = menu.price
    orderForm.value.total_weight = menu.total_weight
    orderForm.value.total_calories = menu.total_calories
    tabooResult.value = null
  } else {
    selectedMenu.value = null
    orderForm.value.total_amount = 0
    orderForm.value.total_weight = 0
    orderForm.value.total_calories = 0
    tabooResult.value = null
  }
}

const checkTaboo = () => {
  if (!selectedMenu.value) {
    ElMessage.warning('请先选择菜单')
    return
  }
  
  const customer = customers.value.find(c => c.id === orderForm.value.customer_id)
  if (!customer) {
    ElMessage.warning('请先选择客户')
    return
  }
  
  // 检测菜单的产后阶段是否与客户的产后阶段匹配
  const menuPeriod = selectedMenu.value.postpartum_period
  const customerPeriod = customer.postpartum_period
  
  let hasTaboo = false
  let warningMessage = ''
  
  if (menuPeriod === 'week1' && (customerPeriod === 'week2' || customerPeriod === 'week3' || customerPeriod === 'week4+')) {
    hasTaboo = true
    warningMessage = `菜单适合产后第一周，客户当前处于${getPostpartumPeriodText(customerPeriod)}，建议选择更适合的菜单`
  } else if (menuPeriod === 'week2' && (customerPeriod === 'week3' || customerPeriod === 'week4+')) {
    hasTaboo = true
    warningMessage = `菜单适合产后第二周，客户当前处于${getPostpartumPeriodText(customerPeriod)}，建议选择更适合的菜单`
  } else if (menuPeriod === 'week3' && customerPeriod === 'week4+') {
    hasTaboo = true
    warningMessage = `菜单适合产后第三周，客户当前处于${getPostpartumPeriodText(customerPeriod)}，建议选择更适合的菜单`
  } else if (menuPeriod === 'week2' && customerPeriod === 'week1') {
    hasTaboo = true
    warningMessage = `菜单适合产后第二周，客户当前处于${getPostpartumPeriodText(customerPeriod)}，该菜单可能过于滋补，建议选择更适合的菜单`
  } else if (menuPeriod === 'week3' && (customerPeriod === 'week1' || customerPeriod === 'week2')) {
    hasTaboo = true
    warningMessage = `菜单适合产后第三周，客户当前处于${getPostpartumPeriodText(customerPeriod)}，该菜单可能过于滋补，建议选择更适合的菜单`
  } else if (menuPeriod === 'week4+' && (customerPeriod === 'week1' || customerPeriod === 'week2' || customerPeriod === 'week3')) {
    hasTaboo = true
    warningMessage = `菜单适合产后第四周及以上，客户当前处于${getPostpartumPeriodText(customerPeriod)}，该菜单可能过于滋补，建议选择更适合的菜单`
  }
  
  tabooResult.value = {
    hasTaboo: hasTaboo,
    warningMessage: warningMessage
  }
}

const openOrderForm = () => {
  const today = new Date()
  const orderNumber = `ORD-${today.getFullYear()}${String(today.getMonth() + 1).padStart(2, '0')}${String(today.getDate()).padStart(2, '0')}-${String(orders.value.length + 1).padStart(3, '0')}`
  
  orderForm.value = {
    id: '',
    order_number: orderNumber,
    customer_id: '',
    menu_id: '',
    total_amount: 0,
    total_weight: 0,
    total_calories: 0,
    order_date: today.toISOString().slice(0, 19).replace('T', ' '),
    status: 'pending'
  }
  selectedMenu.value = null
  tabooResult.value = null
  dialogVisible.value = true
}

const editOrder = (order: any) => {
  orderForm.value = { ...order }
  // 获取菜单信息
  const menu = menus.value.find(m => m.id === order.menu_id)
  if (menu) {
    selectedMenu.value = menu
  }
  dialogVisible.value = true
}

const deleteOrder = (orderId: number) => {
  ElMessageBox.confirm('确定要删除该订单吗？', '删除订单', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // 调用后端API删除订单
      await axios.delete(`/api/orders/${orderId}`)
      // 从本地列表中移除
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
        
        // 获取菜单名称
        const menu = menus.value.find(m => m.id === orderForm.value.menu_id)
        const menuName = menu ? menu.name : '未知菜单'
        
        if (orderForm.value.id) {
          // 编辑订单
          const index = orders.value.findIndex(order => order.id === orderForm.value.id)
          if (index !== -1) {
            orders.value[index] = {
              ...orderForm.value,
              customer_name: customerName,
              menu_name: menuName
            }
          }
          ElMessage.success('订单更新成功')
        } else {
          // 新增订单
          const newOrder = {
            ...orderForm.value,
            id: orders.value.length + 1,
            customer_name: customerName,
            menu_name: menuName
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
  fetchMenus()
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

.menu-info-card {
  margin: 20px 0;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.menu-info {
  padding: 10px;
}

.menu-info-item {
  margin: 8px 0;
  display: flex;
  align-items: center;
}

.menu-info-item .label {
  font-weight: bold;
  width: 100px;
}

.taboo-detection-card {
  margin: 20px 0;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.taboo-result {
  padding: 10px;
}

.taboo-alert {
  margin: 10px 0;
}

.el-table .cell {
  white-space: normal;
  word-break: break-all;
}

@media (max-width: 768px) {
  .order-container {
    padding: 10px;
  }
  
  .menu-info-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .menu-info-item .label {
    width: 100%;
    margin-bottom: 4px;
  }
}
</style>