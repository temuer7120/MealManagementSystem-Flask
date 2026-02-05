// 权限配置文件

// 菜单权限配置
// 格式：{ 角色: [允许访问的路由名称] }
export const menuPermissions = {
  admin: ['Dashboard', 'Menu', 'Dish', 'Ingredient', 'Customer', 'Order', 'ServiceBooking', 'Employee', 'Finance', 'Report', 'System', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  nutritionist: ['Dashboard', 'Menu', 'Dish', 'Ingredient', 'Customer', 'Order', 'ServiceBooking', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  chef: ['Dashboard', 'Menu', 'Dish', 'Ingredient', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  admin_staff: ['Dashboard', 'Customer', 'Order', 'ServiceBooking', 'Employee', 'Finance', 'Report', 'System', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  head_nurse: ['Dashboard', 'Customer', 'Order', 'ServiceBooking', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  nurse: ['Dashboard', 'Customer', 'ServiceBooking', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  caregiver: ['Dashboard', 'Customer', 'ServiceBooking', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  customer: ['Dashboard', 'ServiceBooking', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  user: ['Dashboard', 'ServiceBooking', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition'],
  guest: ['Dashboard', 'ServiceBooking', 'ConfinementMeal', 'Health', 'Appointment', 'Nutrition']
};

// 仪表盘内容权限配置
// 格式：{ 角色: { 内容项: 布尔值/权限级别 } }
export const dashboardPermissions = {
  admin: {
    orderCount: true,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: true,
    activeVisitors: true,
    scheduleType: 'management',
    notificationType: 'all'
  },
  nutritionist: {
    orderCount: true,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nutrition',
    notificationType: 'nutrition'
  },
  chef: {
    orderCount: true,
    dailyMenu: true,
    serviceProjects: false,
    customerCount: false,
    activeVisitors: false,
    scheduleType: 'kitchen',
    notificationType: 'kitchen'
  },
  admin_staff: {
    orderCount: true,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: true,
    activeVisitors: true,
    scheduleType: 'administrative',
    notificationType: 'administrative'
  },
  head_nurse: {
    orderCount: true,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nursing',
    notificationType: 'nursing'
  },
  nurse: {
    orderCount: true,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nursing',
    notificationType: 'nursing'
  },
  caregiver: {
    orderCount: true,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: true,
    activeVisitors: false,
    scheduleType: 'nursing',
    notificationType: 'nursing'
  },
  customer: {
    orderCount: false,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: false,
    activeVisitors: false,
    scheduleType: 'customer',
    notificationType: 'customer'
  },
  user: {
    orderCount: false,
    dailyMenu: true,
    serviceProjects: true,
    customerCount: false,
    activeVisitors: false,
    scheduleType: 'customer',
    notificationType: 'customer'
  },
  guest: {
    orderCount: false,
    dailyMenu: true,
    serviceProjects: true,
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
