<template>
  <div>
    <!-- 主界面导航栏 -->
    <nav class="navbar navbar-expand-lg navbar-dark" :style="{ backgroundColor: '#FF99A8' }">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <i class="fas fa-hotel"></i> 上海巍阁母婴护理中心
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-nav" aria-controls="navbar-nav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbar-nav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">
                <i class="fas fa-home"></i> 首页
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#about">
                <i class="fas fa-info-circle"></i> 关于我们
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#services">
                <i class="fas fa-concierge-bell"></i> 服务项目
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#pricing">
                <i class="fas fa-tag"></i> 价格体系
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#contact">
                <i class="fas fa-envelope"></i> 联系我们
              </a>
            </li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <button class="btn btn-light" @click="openLoginDialog">
                <i class="fas fa-sign-in-alt"></i> 登录
              </button>
            </li>
            <li class="nav-item">
              <button class="btn btn-light" style="margin-left: 10px;" @click="openRegisterDialog">
                <i class="fas fa-user-plus"></i> 注册
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- 公司宣传内容 -->
    <div class="company-banner" :style="{ backgroundColor: '#FF99A8' }">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-md-6">
            <h1>上海巍阁母婴护理中心</h1>
            <p class="lead">专业母婴护理服务，为您和宝宝提供全方位的呵护</p>
            <p>我们拥有一支经验丰富的专业团队，包括营养师、厨师、护士和护理人员，致力于为产后妈妈和新生儿提供最优质的护理服务。</p>
            <div class="mt-4">
              <button class="btn btn-light btn-lg" @click="openLoginDialog">立即咨询</button>
              <button class="btn btn-outline-light btn-lg" style="margin-left: 10px;" @click="scrollToServices">了解服务</button>
            </div>
          </div>
          <div class="col-md-6">
            <img src="https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20mother%20and%20baby%20care%20center%20interior%2C%20modern%20design%2C%20warm%20lighting%2C%20comfortable%20environment%2C%20high%20quality&image_size=landscape_16_9" alt="上海巍阁母婴护理中心" class="img-fluid rounded">
          </div>
        </div>
      </div>
    </div>

    <!-- 服务项目展示 -->
    <div class="services-section" id="services" :style="{ backgroundColor: '#FF99A8' }">
      <div class="container">
        <h2 class="text-center mb-5">我们的服务项目</h2>
        <div class="row">
          <div class="col-md-4">
            <div class="service-card">
              <i class="fas fa-baby fa-3x mb-3"></i>
              <h3>新生儿护理</h3>
              <p>专业护士24小时贴心护理，包括喂养、洗澡、抚触、脐带护理等</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="service-card">
              <i class="fas fa-user-nurse fa-3x mb-3"></i>
              <h3>产后护理</h3>
              <p>产后妈妈身体恢复指导，包括伤口护理、乳房护理、产后修复等</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="service-card">
              <i class="fas fa-utensils fa-3x mb-3"></i>
              <h3>营养膳食</h3>
              <p>专业营养师定制的产后恢复餐单，科学搭配，促进身体恢复</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer" :style="{ backgroundColor: '#FF99A8' }">
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <h3>上海巍阁母婴护理中心</h3>
            <p>专业母婴护理服务提供商</p>
            <p><i class="fas fa-map-marker-alt"></i> 上海市浦东新区张江高科技园区</p>
            <p><i class="fas fa-phone"></i> 400-888-8888</p>
            <p><i class="fas fa-envelope"></i> info@weige.com</p>
          </div>
          <div class="col-md-4">
            <h3>快速链接</h3>
            <ul class="footer-links">
              <li><a href="#">首页</a></li>
              <li><a href="#about">关于我们</a></li>
              <li><a href="#services">服务项目</a></li>
              <li><a href="#pricing">价格体系</a></li>
              <li><a href="#contact">联系我们</a></li>
            </ul>
          </div>
          <div class="col-md-4">
            <h3>关注我们</h3>
            <div class="social-icons">
              <a href="#" class="social-icon"><i class="fab fa-weixin fa-2x"></i></a>
              <a href="#" class="social-icon"><i class="fab fa-weibo fa-2x"></i></a>
              <a href="#" class="social-icon"><i class="fab fa-tiktok fa-2x"></i></a>
              <a href="#" class="social-icon"><i class="fab fa-instagram fa-2x"></i></a>
            </div>
            <p class="mt-4">© 2026 上海巍阁母婴护理中心. 保留所有权利.</p>
          </div>
        </div>
      </div>
    </footer>

    <!-- 登录弹窗 -->
    <el-dialog
      v-model="loginDialogVisible"
      title="会员登录"
      width="500px"
      center
    >
      <div class="auth-container">
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
          <div id="login-message" class="message" style="display: none;"></div>
          <div class="mt-3 text-center">
            <button 
              type="button" 
              class="btn btn-link" 
              id="show-register-btn"
              @click="switchToRegister"
            >
              <i class="fas fa-user-plus"></i> 新用户注册
            </button>
          </div>
        </form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="loginDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleLogin" :loading="loading" :style="{ backgroundColor: '#FF99A8', borderColor: '#FF99A8' }">
            登录
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 注册弹窗 -->
    <el-dialog
      v-model="registerDialogVisible"
      title="用户注册"
      width="600px"
      center
    >
      <div class="auth-container">
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
          <div id="register-message" class="message" style="display: none;"></div>
          <div class="mt-3 text-center">
            <button 
              type="button" 
              class="btn btn-link" 
              id="show-login-btn"
              @click="switchToLogin"
            >
              <i class="fas fa-sign-in-alt"></i> 已有账号？登录
            </button>
          </div>
        </form>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="registerDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleRegister" :loading="registerLoading" :style="{ backgroundColor: '#FF99A8', borderColor: '#FF99A8' }">
            注册
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { getThemeByRole, applyTheme } from '../../utils/theme'

const router = useRouter()
const loading = ref(false)
const registerLoading = ref(false)
const loginDialogVisible = ref(false)
const registerDialogVisible = ref(false)
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
  loginForm.value.username = ''
  loginForm.value.password = ''
})

const focusPassword = () => {
  passwordInput.value?.focus()
}

const scrollToServices = () => {
  const servicesSection = document.getElementById('services')
  if (servicesSection) {
    servicesSection.scrollIntoView({ behavior: 'smooth' })
  }
}

const openLoginDialog = () => {
  loginForm.value.username = ''
  loginForm.value.password = ''
  loginDialogVisible.value = true
  registerDialogVisible.value = false
  
  setTimeout(() => {
    usernameInput.value?.focus()
  }, 100)
}

const openRegisterDialog = () => {
  registerForm.value = {
    username: '',
    password: '',
    name: '',
    gender: '',
    age: null,
    birthdate: null,
    stayDays: null,
    phone: '',
    restrictions: ''
  }
  registerDialogVisible.value = true
  loginDialogVisible.value = false
}

const switchToRegister = () => {
  loginDialogVisible.value = false
  openRegisterDialog()
}

const switchToLogin = () => {
  registerDialogVisible.value = false
  openLoginDialog()
}

const handleLogin = async () => {
  if (!loginForm.value.username || !loginForm.value.password) {
    showMessage('请输入用户名和密码', 'danger', 'login')
    return
  }
  
  loading.value = true
  try {
    console.log('开始登录...')
    const response = await axios.post('/api/auth/login', {
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    
    console.log('登录响应:', response.data)
    const { access_token, user } = response.data
    
    console.log('用户信息:', user)
    localStorage.setItem('token', access_token)
    localStorage.setItem('user', JSON.stringify(user))
    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
    
    console.log('应用主题...')
    console.log('用户角色:', user.role)
    const theme = getThemeByRole(user.role)
    console.log('主题:', theme)
    applyTheme(theme)
    console.log('主题应用完成')
    
    console.log('显示成功消息...')
    showMessage('登录成功', 'success', 'login')
    
    console.log('准备跳转...')
    setTimeout(() => {
      console.log('执行跳转...')
      loginDialogVisible.value = false
      router.push('/dashboard')
    }, 1000)
  } catch (error: any) {
    console.error('登录错误:', error)
    showMessage(error.response?.data?.error || '登录失败，请检查用户名和密码', 'danger', 'login')
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!registerForm.value.username || !registerForm.value.password || !registerForm.value.name) {
    showMessage('请填写必要信息', 'danger', 'register')
    return
  }
  
  registerLoading.value = true
  try {
    await axios.post('/api/auth/register', {
      username: registerForm.value.username,
      password: registerForm.value.password,
      role: 'guest'
    })
    
    showMessage('注册成功，请登录', 'success', 'register')
    
    setTimeout(() => {
      registerDialogVisible.value = false
      loginForm.value.username = registerForm.value.username
      loginForm.value.password = ''
      loginDialogVisible.value = true
      usernameInput.value?.focus()
    }, 1000)
  } catch (error: any) {
    showMessage(error.response?.data?.error || '注册失败，请重试', 'danger', 'register')
  } finally {
    registerLoading.value = false
  }
}

const showMessage = (message: string, type: 'success' | 'danger', formType: 'login' | 'register' = 'login') => {
  const messageElement = document.getElementById(formType === 'register' ? 'register-message' : 'login-message')
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

/* 公司宣传横幅 */
.company-banner {
  padding: 60px 0;
  color: white;
}

.company-banner h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.company-banner .lead {
  font-size: 1.25rem;
  margin-bottom: 20px;
}

.company-banner p {
  font-size: 1.1rem;
  margin-bottom: 30px;
}

/* 服务项目展示 */
.services-section {
  padding: 60px 0;
  color: white;
}

.services-section h2 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 40px;
}

.service-card {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  transition: transform 0.3s ease;
}

.service-card:hover {
  transform: translateY(-10px);
  background-color: rgba(255, 255, 255, 0.15);
}

.service-card h3 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 15px;
}

/* 认证区域 */
.auth-section {
  padding: 60px 0;
  color: #333;
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
  color: #FF99A8;
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
  border-color: #FF99A8;
  box-shadow: 0 0 0 0.2rem rgba(255, 153, 168, 0.25);
}

/* 按钮样式 */
.btn-primary {
  font-size: 1rem;
  padding: 12px;
  margin-top: 10px;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-link {
  color: #FF99A8;
  text-decoration: none;
}

.btn-link:hover {
  color: #FF7788;
  text-decoration: underline;
}

/* 页脚 */
.footer {
  padding: 60px 0 30px;
  color: white;
}

.footer h3 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.footer-links {
  list-style: none;
  padding: 0;
}

.footer-links li {
  margin-bottom: 10px;
}

.footer-links a {
  color: white;
  text-decoration: none;
}

.footer-links a:hover {
  color: #f0f0f0;
  text-decoration: underline;
}

.social-icons {
  display: flex;
  gap: 20px;
}

.social-icon {
  color: white;
  transition: transform 0.3s ease;
}

.social-icon:hover {
  transform: scale(1.1);
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

.mb-5 {
  margin-bottom: 3rem;
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
  
  .company-banner h1 {
    font-size: 2rem;
  }
  
  .services-section h2 {
    font-size: 1.5rem;
  }
  
  .service-card {
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .social-icons {
    justify-content: center;
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
  background: #FF99A8;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #FF7788;
}
</style>