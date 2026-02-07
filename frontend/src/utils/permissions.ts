// 权限检查工具

// 路由权限配置
const routePermissions = {
  admin: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'Customer', 'Employee', 'Finance', 'Report', 'DataEntry'],
  admin_staff: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'Customer', 'Employee', 'Finance', 'Report', 'DataEntry'],
  nutritionist: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'Report', 'DataEntry'],
  nutr: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'Report', 'DataEntry'],
  chef: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'DataEntry'],
  head_nurse: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'Customer', 'Report', 'DataEntry'],
  nurse: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order'],
  caregiver: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order'],
  cust: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order'],
  guest: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order'],
  user: ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order']
}

/**
 * 检查用户是否有权限访问指定路由
 * @param role 用户角色
 * @param routeName 路由名称
 * @returns 是否有权限
 */
export const hasRoutePermission = (role: string, routeName: string): boolean => {
  if (!role || !routePermissions[role as keyof typeof routePermissions]) {
    const defaultRoutes = ['Dashboard', 'ServiceBooking', 'Menu', 'Dish', 'Ingredient', 'Order', 'Customer', 'Employee', 'Finance', 'Report', 'DataEntry']
    return defaultRoutes.includes(routeName)
  }
  return routePermissions[role as keyof typeof routePermissions].includes(routeName)
}

/**
 * 检查用户是否有权限访问指定路径
 * @param role 用户角色
 * @param path 路由路径
 * @returns 是否有权限
 */
export const hasPathPermission = (role: string, path: string): boolean => {
  // 简单的路径到路由名称的映射
  const pathToRouteName: Record<string, string> = {
    '/dashboard': 'Dashboard',
    '/service-booking': 'ServiceBooking',
    '/menu': 'Menu',
    '/dish': 'Dish',
    '/ingredient': 'Ingredient',
    '/order': 'Order',
    '/customer': 'Customer',
    '/employee': 'Employee',
    '/finance': 'Finance',
    '/report': 'Report',
    '/data-entry': 'DataEntry'
  }
  
  const routeName = pathToRouteName[path] || path.split('/')[1].charAt(0).toUpperCase() + path.split('/')[1].slice(1)
  return hasRoutePermission(role, routeName)
}
