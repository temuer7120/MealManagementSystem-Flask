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
  // 设置CSS变量
  document.documentElement.style.setProperty('--primary-color', theme.primary);
  
  // 更新导航栏背景色
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    navbar.style.backgroundColor = theme.primary;
  }
  
  // 更新按钮颜色
  const buttons = document.querySelectorAll('.btn-primary');
  buttons.forEach(button => {
    button.style.backgroundColor = theme.primary;
    button.style.borderColor = theme.primary;
  });
  
  // 更新卡片头部颜色
  const cardHeaders = document.querySelectorAll('.card-header');
  cardHeaders.forEach(header => {
    header.style.backgroundColor = theme.primary;
  });
  
  // 更新页面标题颜色
  const pageTitles = document.querySelectorAll('.page-title');
  pageTitles.forEach(title => {
    title.style.color = theme.primary;
  });
  
  // 更新链接颜色
  const links = document.querySelectorAll('.btn-link');
  links.forEach(link => {
    link.style.color = theme.primary;
  });
  
  // 更新输入框聚焦颜色
  const style = document.createElement('style');
  style.textContent = `
    .form-control:focus {
      border-color: ${theme.primary};
      box-shadow: 0 0 0 0.2rem rgba(${hexToRgb(theme.primary)}, 0.25);
    }
  `;
  document.head.appendChild(style);
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