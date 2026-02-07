// 主题管理工具

// 主题类型
export type ThemeType = 'light' | 'dark' | 'system'

// 默认主题
const DEFAULT_THEME: ThemeType = 'light'

// 主题存储键名
const THEME_STORAGE_KEY = 'meal_management_system_theme'

/**
 * 获取当前主题
 * @returns 当前主题
 */
export const getCurrentTheme = (): ThemeType => {
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY) as ThemeType
  return storedTheme || DEFAULT_THEME
}

/**
 * 保存主题设置
 * @param theme 主题类型
 */
export const saveTheme = (theme: ThemeType): void => {
  localStorage.setItem(THEME_STORAGE_KEY, theme)
}

/**
 * 应用主题
 * @param theme 主题类型
 */
export const applyTheme = (theme: ThemeType): void => {
  // 移除所有主题类
  document.documentElement.classList.remove('theme-light', 'theme-dark')
  
  // 应用新主题
  if (theme === 'dark') {
    document.documentElement.classList.add('theme-dark')
  } else {
    document.documentElement.classList.add('theme-light')
  }
}

/**
 * 切换主题
 * @returns 新主题
 */
export const toggleTheme = (): ThemeType => {
  const currentTheme = getCurrentTheme()
  const newTheme = currentTheme === 'light' ? 'dark' : 'light'
  saveTheme(newTheme)
  applyTheme(newTheme)
  return newTheme
}

/**
 * 初始化主题
 */
export const initTheme = (): void => {
  const theme = getCurrentTheme()
  applyTheme(theme)
}
