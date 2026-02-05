<template>
  <div class="dashboard-container">
    <h2 class="page-title">仪表盘</h2>
    <el-row :gutter="20">
      <!-- 订单数量卡片 (对admin, nutritionist, chef, admin_staff, head_nurse, nurse, caregiver显示) -->
      <el-col v-if="dashboardPermissions.orderCount" :span="8">
        <el-card shadow="hover" class="dashboard-card" @click="navigateTo('/order')" style="cursor: pointer;">
          <template #header>
            <div class="card-header">
              <span>订单数量</span>
              <el-icon class="card-header-icon"><ShoppingCart /></el-icon>
            </div>
          </template>
          <div class="card-content">
            <div class="card-value">{{ orderCount }}</div>
            <div class="card-desc">今日内销和外卖订单</div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 服务项目卡片 (对admin, nutritionist, admin_staff, head_nurse, nurse, caregiver, customer, guest显示) -->
      <el-col v-if="dashboardPermissions.serviceProjects" :span="8">
        <el-card shadow="hover" class="dashboard-card" @click="navigateTo('/nutrition')" style="cursor: pointer;">
          <template #header>
            <div class="card-header">
              <span>服务项目</span>
              <el-icon class="card-header-icon"><House /></el-icon>
            </div>
          </template>
          <div class="card-content">
            <div class="card-value">{{ serviceProjects }}</div>
            <div class="card-desc">今日母婴服务项目</div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 每日餐单卡片 (对所有角色显示) -->
      <el-col :span="8">
        <el-card shadow="hover" class="dashboard-card" @click="navigateTo('/menu')" style="cursor: pointer;">
          <template #header>
            <div class="card-header">
              <span>每日餐单</span>
              <el-icon class="card-header-icon"><House /></el-icon>
            </div>
          </template>
          <div class="card-content">
            <div class="card-value">{{ dailyMenuCount }}</div>
            <div class="card-desc">今日餐单数量</div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 客户数量卡片 (对admin, nutritionist, admin_staff, head_nurse, nurse, caregiver显示) -->
      <el-col v-if="dashboardPermissions.customerCount" :span="8">
        <el-card shadow="hover" class="dashboard-card" @click="navigateTo('/customer')" style="cursor: pointer;">
          <template #header>
            <div class="card-header">
              <span>客户数量</span>
              <el-icon class="card-header-icon"><House /></el-icon>
            </div>
          </template>
          <div class="card-content">
            <div class="card-value">{{ currentCustomers }}</div>
            <div class="card-desc">当前在住客户</div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 活跃访客卡片 (仅对admin和admin_staff显示) -->
      <el-col v-if="dashboardPermissions.activeVisitors" :span="8">
        <el-card shadow="hover" class="dashboard-card" @click="navigateTo('/system')" style="cursor: pointer;">
          <template #header>
            <div class="card-header">
              <span>活跃访客</span>
              <el-icon class="card-header-icon"><House /></el-icon>
            </div>
          </template>
          <div class="card-content">
            <div class="card-value">{{ activeVisitors }}</div>
            <div class="card-desc">当前活跃访客</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>{{ getScheduleTitle() }}</span>
              <el-icon class="card-header-icon"><Timer /></el-icon>
            </div>
          </template>
          <el-table :data="recentSchedule" style="width: 100%">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="time" label="时间" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="status" label="状态" />
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>{{ getNotificationTitle() }}</span>
              <el-icon class="card-header-icon"><Warning /></el-icon>
            </div>
          </template>
          <el-table :data="notifications" style="width: 100%">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="time" label="时间" />
            <el-table-column prop="content" label="内容" />
            <el-table-column prop="status" label="状态" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ShoppingCart, House, Timer, Warning } from '@element-plus/icons-vue'
import { getCurrentTheme, applyTheme } from '../../utils/theme'
import { getDashboardPermissions } from '../../utils/permissions'

const router = useRouter()

// 仪表盘数据
const orderCount = ref(0)
const dailyMenuCount = ref(0)
const serviceProjects = ref(0)
const currentCustomers = ref(0)
const activeVisitors = ref(0)
const recentSchedule = ref<any[]>([])
const notifications = ref<any[]>([])

// 用户角色和权限
const currentUser = ref<any>(null)
const dashboardPermissions = ref<any>(getDashboardPermissions('guest'))

// 根据角色获取仪表盘权限
const getCurrentUserDashboardPermissions = () => {
  if (!currentUser.value) return getDashboardPermissions('guest')
  return getDashboardPermissions(currentUser.value.role)
}

// 获取日程标题
const getScheduleTitle = () => {
  if (!dashboardPermissions.value) return '近期日程'
  
  const scheduleType = dashboardPermissions.value.scheduleType
  switch (scheduleType) {
    case 'management':
      return '管理相关日程'
    case 'nutrition':
      return '营养相关日程'
    case 'kitchen':
      return '厨房相关日程'
    case 'administrative':
      return '行政相关日程'
    case 'nursing':
      return '护理相关日程'
    case 'customer':
      return '客户相关日程'
    case 'guest':
      return '访客相关日程'
    default:
      return '近期日程'
  }
}

// 获取通知标题
const getNotificationTitle = () => {
  if (!dashboardPermissions.value) return '通知中心'
  
  const notificationType = dashboardPermissions.value.notificationType
  switch (notificationType) {
    case 'all':
      return '全部通知'
    case 'nutrition':
      return '营养相关通知'
    case 'kitchen':
      return '厨房相关通知'
    case 'administrative':
      return '行政相关通知'
    case 'nursing':
      return '护理相关通知'
    case 'customer':
      return '客户相关通知'
    case 'guest':
      return '访客相关通知'
    default:
      return '通知中心'
  }
}

// 获取仪表盘数据
const fetchDashboardData = async () => {
  try {
    // 模拟数据，实际项目中应该从后端API获取
    orderCount.value = 45
    dailyMenuCount.value = 12
    serviceProjects.value = 23
    currentCustomers.value = 28
    activeVisitors.value = 5
    
    // 根据角色获取不同的日程数据
    if (dashboardPermissions.value) {
      const scheduleType = dashboardPermissions.value.scheduleType
      switch (scheduleType) {
        case 'management':
          recentSchedule.value = [
            { title: '系统维护', time: '2026-02-04 14:00', description: '定期系统维护', status: '待处理' },
            { title: '员工培训', time: '2026-02-05 10:00', description: '新员工入职培训', status: '已安排' },
            { title: '财务审核', time: '2026-02-06 09:00', description: '月度财务审核', status: '已安排' }
          ]
          break
        case 'nutrition':
          recentSchedule.value = [
            { title: '营养评估', time: '2026-02-04 11:00', description: '客户营养评估', status: '待处理' },
            { title: '菜单调整', time: '2026-02-05 14:00', description: '下周菜单调整', status: '已安排' },
            { title: '营养培训', time: '2026-02-06 10:00', description: '营养知识培训', status: '已安排' }
          ]
          break
        case 'kitchen':
          recentSchedule.value = [
            { title: '食材采购', time: '2026-02-04 08:00', description: '每日食材采购', status: '已完成' },
            { title: '菜品准备', time: '2026-02-04 09:00', description: '今日菜品准备', status: '进行中' },
            { title: '厨房清洁', time: '2026-02-04 18:00', description: '厨房卫生清洁', status: '待处理' }
          ]
          break
        case 'administrative':
          recentSchedule.value = [
            { title: '客户登记', time: '2026-02-04 10:00', description: '新客户入住登记', status: '待处理' },
            { title: '员工排班', time: '2026-02-05 09:00', description: '下周员工排班', status: '已安排' },
            { title: '费用报销', time: '2026-02-06 14:00', description: '员工费用报销', status: '已安排' }
          ]
          break
        case 'nursing':
          recentSchedule.value = [
            { title: '客户查房', time: '2026-02-04 09:00', description: '每日客户查房', status: '进行中' },
            { title: '护理记录', time: '2026-02-04 16:00', description: '今日护理记录', status: '待处理' },
            { title: '护理培训', time: '2026-02-05 10:00', description: '护理技能培训', status: '已安排' }
          ]
          break
        case 'customer':
          recentSchedule.value = [
            { title: '餐食配送', time: '2026-02-04 12:00', description: '午餐配送', status: '已完成' },
            { title: '健康检查', time: '2026-02-04 15:00', description: '每日健康检查', status: '待处理' },
            { title: '婴儿护理', time: '2026-02-04 16:00', description: '婴儿日常护理', status: '待处理' }
          ]
          break
        case 'guest':
          recentSchedule.value = [
            { title: '访客登记', time: '2026-02-04 10:00', description: '访客信息登记', status: '已完成' },
            { title: '参观安排', time: '2026-02-04 11:00', description: '服务项目参观', status: '进行中' },
            { title: '咨询服务', time: '2026-02-04 14:00', description: '服务项目咨询', status: '待处理' }
          ]
          break
        default:
          recentSchedule.value = []
      }
      
      // 根据角色获取不同的通知数据
      const notificationType = dashboardPermissions.value.notificationType
      switch (notificationType) {
        case 'all':
          notifications.value = [
            { title: '系统更新', time: '2026-02-03 18:00', content: '系统已完成更新，新增功能已上线', status: '已读' },
            { title: '新客户入住', time: '2026-02-04 09:00', content: '张女士已入住，房间号：301', status: '未读' },
            { title: '食材库存不足', time: '2026-02-04 10:00', content: '鸡蛋库存不足，需要及时采购', status: '未读' }
          ]
          break
        case 'nutrition':
          notifications.value = [
            { title: '营养方案更新', time: '2026-02-03 16:00', content: '李女士的营养方案已更新', status: '已读' },
            { title: '新菜品添加', time: '2026-02-04 09:00', content: '新增营养菜品：清蒸鲈鱼', status: '未读' },
            { title: '营养培训通知', time: '2026-02-04 10:00', content: '本周六将进行营养知识培训', status: '未读' }
          ]
          break
        case 'kitchen':
          notifications.value = [
            { title: '食材采购通知', time: '2026-02-03 18:00', content: '明日需要采购的食材清单已更新', status: '已读' },
            { title: '菜品调整通知', time: '2026-02-04 08:00', content: '今日菜品调整：更换为红烧排骨', status: '未读' },
            { title: '厨房设备检查', time: '2026-02-04 17:00', content: '今日下班前需进行设备检查', status: '未读' }
          ]
          break
        case 'administrative':
          notifications.value = [
            { title: '员工考勤提醒', time: '2026-02-03 17:00', content: '请及时完成今日考勤记录', status: '已读' },
            { title: '新员工入职', time: '2026-02-04 09:00', content: '新员工小王今日入职，请安排培训', status: '未读' },
            { title: '费用报销截止', time: '2026-02-04 10:00', content: '本月费用报销截止日期为2月15日', status: '未读' }
          ]
          break
        case 'nursing':
          notifications.value = [
            { title: '护理记录提醒', time: '2026-02-03 17:00', content: '请及时完成今日护理记录', status: '已读' },
            { title: '新客户护理方案', time: '2026-02-04 09:00', content: '张女士的护理方案已更新，请查看', status: '未读' },
            { title: '护理培训通知', time: '2026-02-04 10:00', content: '本周日将进行护理技能培训', status: '未读' }
          ]
          break
        case 'customer':
          notifications.value = [
            { title: '餐食提醒', time: '2026-02-04 11:30', content: '午餐将在12:00准时送达', status: '已读' },
            { title: '健康提醒', time: '2026-02-04 14:00', content: '请按时服用今日药物', status: '未读' },
            { title: '服务评价', time: '2026-02-04 16:00', content: '请对今日服务进行评价', status: '未读' }
          ]
          break
        case 'guest':
          notifications.value = [
            { title: '参观提醒', time: '2026-02-04 10:30', content: '参观将在11:00准时开始', status: '已读' },
            { title: '咨询预约', time: '2026-02-04 13:30', content: '您的咨询预约已确认，时间为14:00', status: '未读' },
            { title: '服务介绍', time: '2026-02-04 15:00', content: '我们的服务项目介绍资料已发送至您的邮箱', status: '未读' }
          ]
          break
        default:
          notifications.value = []
      }
    }
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

// 初始化用户信息和权限
const initUserInfo = () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    currentUser.value = JSON.parse(userStr)
    dashboardPermissions.value = getCurrentUserDashboardPermissions()
  } else {
    currentUser.value = null
    dashboardPermissions.value = getDashboardPermissions('guest')
  }
}

// 跳转函数
const navigateTo = (path: string) => {
  router.push(path)
}

onMounted(() => {
  // 初始化用户信息和权限
  initUserInfo()
  
  // 应用当前用户的主题
  const theme = getCurrentTheme()
  applyTheme(theme)
  
  // 获取仪表盘数据
  fetchDashboardData()
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--primary-color);
  color: white;
  font-weight: bold;
  border-radius: 8px 8px 0 0;
}

.card-header-icon {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
}

.card-content {
  text-align: center;
  padding: 20px 0;
}

.card-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--primary-color);
}

.card-desc {
  font-size: 14px;
  color: #909399;
}
</style>