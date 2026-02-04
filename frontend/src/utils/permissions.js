// 权限配置文件

// 菜单权限配置
// 格式：{ 角色: [允许访问的路由名称] }
export const menuPermissions = {
  admin: ['Dashboard', 'Menu', 'Dish', 'Customer', 'Order', 'System', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  nutritionist: ['Dashboard', 'Menu', 'Dish', 'Customer', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  chef: ['Dashboard', 'Dish', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  admin_staff: ['Dashboard', 'Customer', 'Order', 'System', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  head_nurse: ['Dashboard', 'Customer', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  nurse: ['Dashboard', 'Customer', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  caregiver: ['Dashboard', 'Customer', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  customer: ['Dashboard', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  guest: ['Dashboard', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition']
};

// 仪表盘内容权限配置
// 格式：{ 角色: { 内容项: 布尔值/权限级别 } }
export const dashboardPermissions = {
  admin: {
    menuCount: true,
    dailyMenu: true,
    customerCount: true,
    activeVisitors: true,
    scheduleType: 'management',
    notificationType: 'all'
  },
  nutritionist: {
    menuCount: true,
    dailyMenu: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nutrition',
    notificationType: 'nutrition'
  },
  chef: {
    menuCount: false,
    dailyMenu: true,
    customerCount: false,
    activeVisitors: false,
    scheduleType: 'kitchen',
    notificationType: 'kitchen'
  },
  admin_staff: {
    menuCount: false,
    dailyMenu: true,
    customerCount: true,
    activeVisitors: true,
    scheduleType: 'administrative',
    notificationType: 'administrative'
  },
  head_nurse: {
    menuCount: false,
    dailyMenu: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nursing',
    notificationType: 'nursing'
  },
  nurse: {
    menuCount: false,
    dailyMenu: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nursing',
    notificationType: 'nursing'
  },
  caregiver: {
    menuCount: false,
    dailyMenu: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nursing',
    notificationType: 'nursing'
  },
  customer: {
    menuCount: false,
    dailyMenu: true,
    customerCount: false,
    activeVisitors: false,
    scheduleType: 'customer',
    notificationType: 'customer'
  },
  guest: {
    menuCount: false,
    dailyMenu: true,
    customerCount: false,
    activeVisitors: false,
    scheduleType: 'guest',
    notificationType: 'guest'
  }
};

// 检查用户是否有权限访问指定路由
export const hasRoutePermission = (role, routeName) => {
  if (!role) return false;
  
  const allowedRoutes = menuPermissions[role] || [];
  return allowedRoutes.includes(routeName);
};

// 获取用户的仪表盘权限
export const getDashboardPermissions = (role) => {
  return dashboardPermissions[role] || dashboardPermissions.guest;
};