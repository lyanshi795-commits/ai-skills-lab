Page({
  data: {
    title: "示例_quiz",
    questions: [
      { q: '示例题1：你更喜欢？', options: ['A. 安静', 'B. 热闹'] },
      { q: '示例题2：周末你通常？', options: ['A. 宅家', 'B. 出门'] }
    ],
    step: 0,
    score: 0,
    result: ''
  },
  choose(e){
    const d = e.currentTarget.dataset.d;
    let score = this.data.score + (d === 1 ? 1 : 0);
    let step = this.data.step + 1;
    if (step >= this.data.questions.length) {
      // TODO: 根据分数给出结果文案
      this.setData({ result: '你的得分：' + score + '（在此写你的解读）' });
    } else {
      this.setData({ step, score });
    }
  }
})
