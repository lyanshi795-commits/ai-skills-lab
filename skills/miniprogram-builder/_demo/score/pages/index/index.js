Page({
  data: { title: "示例_score", players: [ { name: '玩家1', score: 0 }, { name: '玩家2', score: 0 } ] },
  change(e){
    const i = e.currentTarget.dataset.i;
    const d = e.currentTarget.dataset.d;
    const key = `players[${i}].score`;
    const val = this.data.players[i].score + d;
    this.setData({ [key]: val });
  },
  addPlayer(){
    const players = this.data.players.concat({ name: '玩家' + (this.data.players.length + 1), score: 0 });
    this.setData({ players });
  }
})
