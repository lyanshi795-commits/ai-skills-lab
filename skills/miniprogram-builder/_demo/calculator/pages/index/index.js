Page({
  data: { title: "示例_calculator", a: '', b: '', result: '' },
  onInputA(e){ this.setData({ a: e.detail.value }) },
  onInputB(e){ this.setData({ b: e.detail.value }) },
  compute(){
    const a = parseFloat(this.data.a);
    const b = parseFloat(this.data.b);
    if (isNaN(a) || isNaN(b)) { wx.showToast({ title: '请输入数字', icon: 'none' }); return; }
    // TODO: 在此写你的核心计算公式（手册主张：输入 → 计算 → 展示，纯前端即可）
    const result = a + b;
    this.setData({ result: result.toString() });
  }
})
