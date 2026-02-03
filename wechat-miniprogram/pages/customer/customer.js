// customer.js
Page({
  data: {
    customers: [],
    loading: true,
    searchKey: ''
  },
  
  onLoad() {
    this.loadCustomers();
  },
  
  loadCustomers() {
    const app = getApp();
    
    this.setData({ loading: true });
    
    app.request('/customers')
      .then(res => {
        this.setData({
          customers: res,
          loading: false
        });
      })
      .catch(err => {
        console.error('Error loading customers:', err);
        this.setData({ loading: false });
        wx.showToast({
          title: '加载失败',
          icon: 'none'
        });
      });
  },
  
  searchCustomer(e) {
    this.setData({ searchKey: e.detail.value });
    // 这里可以添加搜索逻辑
  },
  
  viewCustomerDetail(e) {
    const customerId = e.currentTarget.dataset.id;
    wx.showToast({
      title: `查看客户ID: ${customerId}`,
      icon: 'none'
    });
    // 这里可以添加查看客户详情的逻辑
  },
  
  onPullDownRefresh() {
    this.loadCustomers();
    wx.stopPullDownRefresh();
  }
})
