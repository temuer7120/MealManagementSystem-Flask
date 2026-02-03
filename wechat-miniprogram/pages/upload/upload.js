// upload.js
Page({
  data: {
    fileName: '',
    filePath: '',
    loading: false,
    message: '',
    messageType: ''
  },
  
  chooseFile() {
    const that = this;
    
    wx.chooseMessageFile({
      count: 1,
      type: 'file',
      extension: ['.xlsx', '.xls'],
      success(res) {
        const file = res.tempFiles[0];
        that.setData({
          fileName: file.name,
          filePath: file.path
        });
      }
    });
  },
  
  uploadFile() {
    if (!this.data.filePath) {
      this.showMessage('请先选择文件', 'alert-danger');
      return;
    }
    
    const that = this;
    const app = getApp();
    
    that.setData({
      loading: true,
      message: '',
      messageType: ''
    });
    
    app.uploadFile('/upload/excel', this.data.filePath, 'file')
      .then(res => {
        that.setData({
          loading: false,
          message: res.message,
          messageType: 'alert-success',
          fileName: '',
          filePath: ''
        });
        
        // 3秒后清空消息
        setTimeout(() => {
          that.setData({
            message: '',
            messageType: ''
          });
        }, 3000);
      })
      .catch(err => {
        that.setData({
          loading: false,
          message: err.error || '上传失败',
          messageType: 'alert-danger'
        });
        
        // 3秒后清空消息
        setTimeout(() => {
          that.setData({
            message: '',
            messageType: ''
          });
        }, 3000);
      });
  },
  
  showMessage(message, type) {
    this.setData({
      message: message,
      messageType: type
    });
    
    // 3秒后清空消息
    setTimeout(() => {
      this.setData({
        message: '',
        messageType: ''
      });
    }, 3000);
  }
})
