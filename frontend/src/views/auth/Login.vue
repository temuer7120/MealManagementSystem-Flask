<template>
  <div>
    <!-- 主界面导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <i class="fas fa-hotel"></i> 上海巍阁公司管系统
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-nav" aria-controls="navbar-nav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar-nav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#dashboard">
                <i class="fas fa-home"></i> 首页
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#menus">
                <i class="fas fa-utensils"></i> 菜单管理
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#daily-menus">
                <i class="fas fa-calendar-day"></i> 每日餐单
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#customers">
                <i class="fas fa-users"></i> 客户管理
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#dishes">
                <i class="fas fa-drumstick-bite"></i> 菜品管理
              </a>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" id="admin-dropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <i class="fas fa-cog"></i> 管理功能
              </a>
              <ul class="dropdown-menu" aria-labelledby="admin-dropdown">
                <li>
                  <a class="dropdown-item" href="#employees">
                    <i class="fas fa-user-tie"></i> 员工管理
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#finance">
                    <i class="fas fa-money-bill-wave"></i> 财务管理
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#reports">
                    <i class="fas fa-file-alt"></i> 报表打印
                  </a>
                </li>
              </ul>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <span class="nav-link">
                <i class="fas fa-user"></i> 欢迎，<span id="current-user">用户</span>
              </span>
            </li>
            <li class="nav-item">
              <button class="btn btn-outline-light" id="logout-btn">
                <i class="fas fa-sign-out-alt"></i> 退出登录
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- 登录界面 -->
    <div class="login-container">
      <div id="login-page" class="auth-container">
        <h2 class="auth-title">
          <i class="fas fa-sign-in-alt"></i> 上海巍阁公司管系统 - 登录
        </h2>
        <form id="login-form">
          <div class="mb-3">
            <label for="login-username" class="form-label">
              <i class="fas fa-user"></i> 用户名
            </label>
            <input 
              type="text" 
              class="form-control" 
              id="login-username" 
              v-model="loginForm.username"
              @keyup.enter="focusPassword"
              ref="usernameInput"
              required 
              placeholder="请输入用户名"
            >
          </div>
          <div class="mb-3">
            <label for="login-password" class="form-label">
              <i class="fas fa-lock"></i> 密码
            </label>
            <input 
              type="password" 
              class="form-control" 
              id="login-password" 
              v-model="loginForm.password"
              @keyup.enter="handleLogin"
              ref="passwordInput"
              required 
              placeholder="请输入密码"
            >
          </div>
          <button 
            type="button" 
            class="btn btn-primary w-100"
            @click="handleLogin"
            :disabled="loading"
          >
            <i class="fas fa-sign-in-alt"></i> 登录
          </button>
          <div class="mt-3 text-center">
            <button 
              type="button" 
              class="btn btn-link" 
              id="show-register-btn"
              @click="showRegister = true"
            >
              <i class="fas fa-user-plus"></i> 访客注册
            </button>
          </div>
          <div id="login-message" class="message" style="display: none;"></div>
        </form>
      </div>

      <!-- 访客注册界面 -->
      <div id="register-page" class="auth-container" v-if="showRegister">
        <h2 class="auth-title">
          <i class="fas fa-user-plus"></i> 访客注册
        </h2>
        <form id="register-form">
          <div class="row">
            <div class="col-md-6">
              <div class="mb-3">
                <label for="register-username" class="form-label">
                  <i class="fas fa-user"></i> 用户名
                </label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="register-username" 
                  v-model="registerForm.username"
                  required 
                  placeholder="请输入用户名"
                >
              </div>
              <div class="mb-3">
                <label for="register-password" class="form-label">
                  <i class="fas fa-lock"></i> 密码
                </label>
                <input 
                  type="password" 
                  class="form-control" 
                  id="register-password" 
                  v-model="registerForm.password"
                  required 
                  placeholder="请输入密码"
                >
              </div>
              <div class="mb-3">
                <label for="register-name" class="form-label">
                  <i class="fas fa-id-card"></i> 姓名
                </label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="register-name" 
                  v-model="registerForm.name"
                  required 
                  placeholder="请输入姓名"
                >
              </div>
              <div class="mb-3">
                <label for="register-gender" class="form-label">
                  <i class="fas fa-venus-mars"></i> 性别
                </label>
                <select 
                  class="form-control" 
                  id="register-gender" 
                  v-model="registerForm.gender"
                  required
                >
                  <option value="">请选择</option>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="register-age" class="form-label">
                  <i class="fas fa-birthday-cake"></i> 年龄
                </label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="register-age" 
                  v-model="registerForm.age"
                  required 
                  placeholder="请输入年龄"
                >
              </div>
            </div>
            <div class="col-md-6">
              <div class="mb-3">
                <label for="register-birthdate" class="form-label">
                  <i class="fas fa-calendar-alt"></i> 出生日期
                </label>
                <input 
                  type="date" 
                  class="form-control" 
                  id="register-birthdate" 
                  v-model="registerForm.birthdate"
                  required
                >
              </div>
              <div class="mb-3">
                <label for="register-stay-days" class="form-label">
                  <i class="fas fa-hotel"></i> 计划入住天数
                </label>
                <input 
                  type="number" 
                  class="form-control" 
                  id="register-stay-days" 
                  v-model="registerForm.stayDays"
                  required 
                  placeholder="请输入计划入住天数"
                >
              </div>
              <div class="mb-3">
                <label for="register-phone" class="form-label">
                  <i class="fas fa-phone"></i> 联系电话
                </label>
                <input 
                  type="tel" 
                  class="form-control" 
                  id="register-phone" 
                  v-model="registerForm.phone"
                  required 
                  placeholder="请输入联系电话"
                >
              </div>
              <div class="mb-3">
                <label for="register-restrictions" class="form-label">
                  <i class="fas fa-utensils"></i> 饮食禁忌
                </label>
                <textarea 
                  class="form-control" 
                  id="register-restrictions" 
                  v-model="registerForm.restrictions"
                  rows="3" 
                  placeholder="请输入饮食禁忌"
                ></textarea>
              </div>
            </div>
          </div>
          <button 
            type="button" 
            class="btn btn-primary w-100"
            @click="handleRegister"
            :disabled="registerLoading"
          >
            <i class="fas fa-user-plus"></i> 注册
          </button>
          <div class="mt-3 text-center">
            <button 
              type="button" 
              class="btn btn-link" 
              id="show-login-btn"
              @click="showRegister = false"
            >
              <i class="fas fa-sign-in-alt"></i> 已有账号？登录
            </button>
          </div>
          <div id="register-message" class="message" style="display: none;"></div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'


import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const registerLoading = ref(false)
const showRegister = ref(false)
const usernameInput = ref<HTMLInputElement>()
const passwordInput = ref<HTMLInputElement>()

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: '',
  name: '',
  gender: '',
  age: null,
  birthdate: null,
  stayDays: null,
  phone: '',
  restrictions: ''
})

onMounted(() => {
  // 自动清空表单
  loginForm.value.username = ''
  loginForm.value.password = ''
  
  // 光标默认聚焦到用户名输入框
  setTimeout(() => {
    usernameInput.value?.focus()
  }, 100)
})

const focusPassword = () => {
  passwordInput.value?.focus()
}

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    showMessage('请输入用户名和密码', 'danger')
    return
  }
  
  loading.value = true
  try {
    const response = await axios.post('/api/auth/login', {
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    
    const { access_token, user } = response.data
    
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(user))
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    
    showMessage('登录成功', 'success')
    
    // 跳转到仪表板
    setTimeout(() => {
      router.push('/dashboard')
    }, 1000)
  } catch (error: any) {
    showMessage(error.response?.data?.error || '登录失败，请检查用户名和密码', 'danger')
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!registerForm.value.username || !registerForm.value.password || !registerForm.value.name) {
    showMessage('请填写必要信息', 'danger')
    return
  }
  
  registerLoading.value = true
  try {
    await axios.post('/api/auth/register', {
      username: registerForm.value.username,
      password: registerForm.value.password,
      role: 'guest'
    })
    
    showMessage('注册成功，请登录', 'success')
    
    // 切换到登录界面并填充用户名
    setTimeout(() => {
      showRegister.value = false
      loginForm.value.username = registerForm.value.username
      loginForm.value.password = ''
      usernameInput.value?.focus()
    }, 1000)
  } catch (error: any) {
    showMessage(error.response?.data?.error || '注册失败，请重试', 'danger')
  } finally {
    registerLoading.value = false
  }
}

const showMessage = (message: string, type: 'success' | 'danger') => {
  const messageElement = document.getElementById(type === 'success' ? 'register-message' : 'login-message')
  if (messageElement) {
    messageElement.className = `message message-${type}`
    messageElement.textContent = message
    messageElement.style.display = 'block'
    
    setTimeout(() => {
      messageElement.style.display = 'none'
    }, 3000)
  }
}
</script>

<style scoped>
@import url('https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css');
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');

/* 全局样式 */
body {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  background-color: #f8f9fa;
  color: #333;
}

/* 导航栏样式 */
.navbar {
  background-color: #3498db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-nav .nav-link {
  color: white;
  font-size: 1rem;
  margin-right: 1rem;
}

.navbar-nav .nav-link:hover {
  color: #f0f0f0;
}

/* 登录容器 */
.login-container {
  min-height: 80vh;
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

/* 认证容器 */
.auth-container {
  max-width: 500px;
  width: 100%;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  animation: fadeIn 0.3s ease-in-out;
}

/* 淡入动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 认证标题 */
.auth-title {
  color: #3498db;
  font-weight: bold;
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
}

/* 表单标签 */
.form-label {
  font-weight: bold;
  color: #555;
}

/* 表单控件 */
.form-control {
  border-radius: 4px;
  border: 1px solid #ddd;
}

.form-control:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
}

/* 按钮样式 */
.btn-primary {
  background-color: #3498db;
  border-color: #3498db;
  font-size: 1rem;
  padding: 12px;
  margin-top: 10px;
}

.btn-primary:hover {
  background-color: #2980b9;
  border-color: #2980b9;
}

.btn-link {
  color: #3498db;
  text-decoration: none;
}

.btn-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

/* 消息提示 */
.message {
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  animation: fadeIn 0.3s ease-in-out;
}

.message-success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}

.message-danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

/* 间距 */
.mt-3 {
  margin-top: 1rem;
}

.text-center {
  text-align: center;
}

.mb-3 {
  margin-bottom: 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-container {
    padding: 1.5rem;
  }
  
  .auth-title {
    font-size: 1.2rem;
  }
  
  .navbar-nav {
    flex-direction: column;
  }
  
  .navbar-nav .nav-link {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }
  
  .login-container {
    min-height: 70vh;
  }
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #3498db;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #2980b9;
}
</style>