// index.js
Page({
  data: {
    serverStatus: '检查中...',
    dbStatus: '检查中...',
    lastUpdateTime: '未知'
  },
  
  onLoad() {
    this.checkSystemStatus();
  },
  
  checkSystemStatus() {
    const app = getApp();
    
    // 检查后端服务状态
    app.request('/menus')
      .then(res => {
        this.setData({
          serverStatus: '正常',
          lastUpdateTime: new Date().toLocaleString()
        });
      })
      .catch(err => {
        this.setData({
          serverStatus: '异常',
          lastUpdateTime: new Date().toLocaleString()
        });
      });
    
    // 检查数据库状态
    app.request('/dishes')
      .then(res => {
        this.setData({
          dbStatus: '正常'
        });
      })
      .catch(err => {
        this.setData({
          dbStatus: '异常'
        });
      });
  },
  
  onPullDownRefresh() {
    this.checkSystemStatus();
    wx.stopPullDownRefresh();
  }
})
