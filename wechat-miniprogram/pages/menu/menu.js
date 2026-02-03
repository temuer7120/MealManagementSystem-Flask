// menu.js
Page({
  data: {
    menus: [],
    loading: true,
    searchKey: ''
  },
  
  onLoad() {
    this.loadMenus();
  },
  
  loadMenus() {
    const app = getApp();
    
    this.setData({ loading: true });
    
    app.request('/menus')
      .then(res => {
        this.setData({
          menus: res,
          loading: false
        });
      })
      .catch(err => {
        console.error('Error loading menus:', err);
        this.setData({ loading: false });
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        });
      });
  },
  
  searchMenu(e) {
    this.setData({ searchKey: e.detail.value });
    // 这里可以添加搜索逻辑
  },
  
  viewMenuDetail(e) {
    const menuId = e.currentTarget.dataset.id;
    wx.showToast({
      title: `查看菜单ID: ${menuId}`,
      icon: 'none'
    });
    // 这里可以添加查看菜单详情的逻辑
  },
  
  onPullDownRefresh() {
    this.loadMenus();
    wx.stopPullDownRefresh();
  }
})
