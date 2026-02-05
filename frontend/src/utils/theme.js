// 主题管理工具

// 角色对应的颜色主题
const ROLE_THEMES = {
  admin: {
    primary: '#3498db',
    name: '蓝色'
  },
  nutritionist: {
    primary: '#3498db',
    name: '蓝色'
  },
  chef: {
    primary: '#27ae60',
    name: '绿色'
  },
  admin_staff: {
    primary: '#27ae60',
    name: '绿色'
  },
  head_nurse: {
    primary: '#27ae60',
    name: '绿色'
  },
  nurse: {
    primary: '#27ae60',
    name: '绿色'
  },
  caregiver: {
    primary: '#27ae60',
    name: '绿色'
  },
  customer: {
    primary: '#FF99A8',
    name: '浅粉色'
  },
  user: {
    primary: '#FF99A8',
    name: '浅粉色'
  },
  guest: {
    primary: '#FF99A8',
    name: '浅粉色'
  }
};

// 获取角色对应的主题
export const getThemeByRole = (role) => {
  return ROLE_THEMES[role] || ROLE_THEMES.guest;
};

// 获取当前用户的主题
export const getCurrentTheme = () => {
  const userStr = localStorage.getItem('user');
  if (userStr) {
    try {
      const user = JSON.parse(userStr);
      return getThemeByRole(user.role);
    } catch (error) {
      console.error('Error parsing user from localStorage:', error);
    }
  }
  return ROLE_THEMES.guest;
};

// 应用主题到DOM
export const applyTheme = (theme) => {
  console.log('开始应用主题:', theme);
  
  // 设置CSS变量
  document.documentElement.style.setProperty('--primary-color', theme.primary);
  console.log('CSS变量设置完成:', theme.primary);
  
  // 更新导航栏背景色
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    navbar.style.backgroundColor = theme.primary;
    console.log('导航栏背景色更新完成');
  } else {
    console.log('未找到导航栏元素');
  }
  
  // 更新按钮颜色
  const buttons = document.querySelectorAll('.btn-primary');
  buttons.forEach(button => {
    button.style.backgroundColor = theme.primary;
    button.style.borderColor = theme.primary;
  });
  console.log('按钮颜色更新完成:', buttons.length, '个按钮');
  
  // 更新卡片头部颜色
  const cardHeaders = document.querySelectorAll('.card-header');
  cardHeaders.forEach(header => {
    header.style.backgroundColor = theme.primary;
  });
  console.log('卡片头部颜色更新完成:', cardHeaders.length, '个卡片');
  
  // 更新页面标题颜色
  const pageTitles = document.querySelectorAll('.page-title');
  pageTitles.forEach(title => {
    title.style.color = theme.primary;
  });
  console.log('页面标题颜色更新完成:', pageTitles.length, '个标题');
  
  // 更新链接颜色
  const links = document.querySelectorAll('.btn-link');
  links.forEach(link => {
    link.style.color = theme.primary;
  });
  console.log('链接颜色更新完成:', links.length, '个链接');
  
  // 更新输入框聚焦颜色
  const style = document.createElement('style');
  style.textContent = `
    .form-control:focus {
      border-color: ${theme.primary};
      box-shadow: 0 0 0 0.2rem rgba(${hexToRgb(theme.primary)}, 0.25);
    }
  `;
  document.head.appendChild(style);
  console.log('输入框聚焦颜色更新完成');
  
  console.log('主题应用完成');
};

// 辅助函数：将十六进制颜色转换为RGB
const hexToRgb = (hex) => {
  // 移除#号
  hex = hex.replace('#', '');
  
  // 解析RGB值
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  
  return `${r}, ${g}, ${b}`;
};
