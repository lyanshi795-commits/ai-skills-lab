Page({
  data: { title: "示例_generator", input: '', output: '' },
  onInput(e){ this.setData({ input: e.detail.value }) },
  generate(){
    if (!this.data.input) { wx.showToast({ title: '先输入内容', icon: 'none' }); return; }
    // TODO: 在此调用 AI 接口（或云函数）生成结果；离线先给占位
    this.setData({ output: '【AI 生成结果占位】' + this.data.input });
  }
})
