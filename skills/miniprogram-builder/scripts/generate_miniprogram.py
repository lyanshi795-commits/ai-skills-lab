#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scaffold a minimal, valid WeChat mini-program project.

Usage:
  python generate_miniprogram.py --name mytool --title "BMI计算器" \
      --type calculator --out ./output/mytool
"""
import argparse
import json
import os

VALID_TYPES = ["calculator", "score", "quiz", "generator", "custom"]


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)


def make_app_json(title):
    return dump({
        "pages": ["pages/index/index"],
        "window": {
            "navigationBarBackgroundColor": "#F7F8FA",
            "navigationBarTitleText": title,
            "navigationBarTextStyle": "black",
            "backgroundColor": "#F7F8FA"
        },
        "style": "v2",
        "sitemapLocation": "sitemap.json"
    })


APP_JS = """App({
  onLaunch() {}
})
"""

APP_WXSS = """page { background: #F7F8FA; font-family: -apple-system, "PingFang SC", sans-serif; }
.container { padding: 32rpx; }
.title { font-size: 40rpx; font-weight: 600; color: #1a1a1a; margin-bottom: 24rpx; }
.subtitle { font-size: 26rpx; color: #888; margin-bottom: 32rpx; }
.input { background: #fff; border-radius: 12rpx; padding: 20rpx; margin-bottom: 20rpx; font-size: 30rpx; }
.btn { background: #3CAB6E; color: #fff; border-radius: 12rpx; padding: 22rpx; text-align: center; font-size: 32rpx; margin-top: 24rpx; }
.btn-ghost { background: #e8f5ee; color: #3CAB6E; }
.result { margin-top: 32rpx; padding: 24rpx; background: #fff; border-radius: 12rpx; font-size: 32rpx; color: #1a1a1a; }
.row { display: flex; justify-content: space-between; align-items: center; background: #fff; border-radius: 12rpx; padding: 20rpx; margin-bottom: 16rpx; }
"""

SITEMAP = dump({
    "desc": "关于本文件的更多信息，请参考文档 https://developers.weixin.qq.com/miniprogram/dev/framework/sitemap.html",
    "rules": [{"action": "allow", "page": "*"}]
})


def make_project_config(name, title):
    return dump({
        "description": title,
        "packOptions": {"ignore": [], "include": []},
        "setting": {
            "urlCheck": False,
            "es6": True,
            "enhance": True,
            "postcss": True,
            "minified": True
        },
        "compileType": "miniprogram",
        "libVersion": "3.0.0",
        "appid": "touristappid",
        "projectname": name,
        "miniprogramRoot": "./"
    })


# ---------- per-type index pages ----------

def page_calculator(title):
    js = """Page({
  data: { title: "%s", a: '', b: '', result: '' },
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
""" % title
    wxml = """<view class="container">
  <view class="title">{{title}}</view>
  <view class="subtitle">输入数值，点击计算</view>
  <input class="input" placeholder="请输入数值 A" type="digit" value="{{a}}" bindinput="onInputA"/>
  <input class="input" placeholder="请输入数值 B" type="digit" value="{{b}}" bindinput="onInputB"/>
  <view class="btn" bindtap="compute">计算</view>
  <view class="result" wx:if="{{result}}">结果：{{result}}</view>
</view>
"""
    return js, wxml


def page_score(title):
    js = """Page({
  data: { title: "%s", players: [ { name: '玩家1', score: 0 }, { name: '玩家2', score: 0 } ] },
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
""" % title
    wxml = """<view class="container">
  <view class="title">{{title}}</view>
  <view class="subtitle">点击 + / - 记分，天然裂变：一人用，同桌都用</view>
  <view class="row" wx:for="{{players}}" wx:key="name">
    <text>{{item.name}}</text>
    <view>
      <text class="btn btn-ghost" data-i="{{index}}" data-d="-1" bindtap="change" style="display:inline-block;padding:10rpx 24rpx;margin-right:12rpx;">-</text>
      <text style="font-size:36rpx;margin:0 16rpx;">{{item.score}}</text>
      <text class="btn btn-ghost" data-i="{{index}}" data-d="1" bindtap="change" style="display:inline-block;padding:10rpx 24rpx;">+</text>
    </view>
  </view>
  <view class="btn" bindtap="addPlayer">+ 添加玩家</view>
</view>
"""
    return js, wxml


def page_quiz(title):
    js = """Page({
  data: {
    title: "%s",
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
""" % title
    wxml = """<view class="container">
  <view class="title">{{title}}</view>
  <block wx:if="{{!result}}">
    <view class="subtitle">{{questions[step].q}}</view>
    <view class="btn" data-d="0" bindtap="choose">{{questions[step].options[0]}}</view>
    <view class="btn" data-d="1" bindtap="choose">{{questions[step].options[1]}}</view>
  </block>
  <view class="result" wx:else>{{result}}</view>
</view>
"""
    return js, wxml


def page_generator(title):
    js = """Page({
  data: { title: "%s", input: '', output: '' },
  onInput(e){ this.setData({ input: e.detail.value }) },
  generate(){
    if (!this.data.input) { wx.showToast({ title: '先输入内容', icon: 'none' }); return; }
    // TODO: 在此调用 AI 接口（或云函数）生成结果；离线先给占位
    this.setData({ output: '【AI 生成结果占位】' + this.data.input });
  }
})
""" % title
    wxml = """<view class="container">
  <view class="title">{{title}}</view>
  <textarea class="input" placeholder="输入内容，点击生成" value="{{input}}" bindinput="onInput" style="height:200rpx;"/>
  <view class="btn" bindtap="generate">生成</view>
  <view class="result" wx:if="{{output}}">{{output}}</view>
</view>
"""
    return js, wxml


def page_custom(title):
    js = """Page({
  data: { title: "%s", result: '' },
  run(){
    // TODO: 在此实现你的核心功能
    this.setData({ result: '功能待实现' });
  }
})
""" % title
    wxml = """<view class="container">
  <view class="title">{{title}}</view>
  <view class="subtitle">单一功能 · 清晰场景（手册铁律）</view>
  <view class="btn" bindtap="run">开始</view>
  <view class="result" wx:if="{{result}}">{{result}}</view>
</view>
"""
    return js, wxml


PAGE_BUILDERS = {
    "calculator": page_calculator,
    "score": page_score,
    "quiz": page_quiz,
    "generator": page_generator,
    "custom": page_custom,
}


def make_readme(name, title, ptype):
    return f"""# {title}（小程序项目）

由 miniprogram-builder 技能一键生成。类型：{ptype}

## 本地预览
1. 打开「微信开发者工具 Stable」。
2. 导入项目，目录选本文件夹；AppID 选「测试号」即可（无需先注册）。
3. 编译后左侧模拟器即可看到效果。

## 开发原则（来自实战手册）
- 功能单一：只解决一个问题。
- 场景清晰：用户什么情况下会打开它？
- 纯前端优先：计算/记分/测试类无需登录与数据库。

## 上线前流程
1. 微信公众平台 mp.weixin.qq.com 注册小程序（个人 30 元认证）。
2. 提交备案（3–15 工作日）+ 认证（1–3 工作日），两者可同时提交。
3. 在开发者工具里「上传」代码 → 后台「提交审核」→ 通过后「发布」。
4. 审核被拒常见原因：功能太简单/不完整、名称简介太虚、隐私类目对不上；按驳回逐条改。
5. 发布后 1–2 天可被搜索到。

## 变现
- 个人主体：累计独立访客 ≥ 500 后开通「流量主」放广告（Banner/插屏/激励）。
- 企业/个体户：可接微信支付做付费/订阅。

## 下一步
- 需要第二个页面/底部 tabBar、云函数存数据、或接入 AI，回复继续让 WorkBuddy 帮你加。
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True, help="英文项目名，如 mytool")
    ap.add_argument("--title", required=True, help="中文显示名，如 BMI计算器")
    ap.add_argument("--type", required=True, choices=VALID_TYPES)
    ap.add_argument("--out", required=True, help="输出目录")
    args = ap.parse_args()

    root = os.path.abspath(args.out)
    pages_dir = os.path.join(root, "pages", "index")
    os.makedirs(pages_dir, exist_ok=True)

    # app level
    with open(os.path.join(root, "app.json"), "w", encoding="utf-8") as f:
        f.write(make_app_json(args.title))
    with open(os.path.join(root, "app.js"), "w", encoding="utf-8") as f:
        f.write(APP_JS)
    with open(os.path.join(root, "app.wxss"), "w", encoding="utf-8") as f:
        f.write(APP_WXSS)
    with open(os.path.join(root, "sitemap.json"), "w", encoding="utf-8") as f:
        f.write(SITEMAP)
    with open(os.path.join(root, "project.config.json"), "w", encoding="utf-8") as f:
        f.write(make_project_config(args.name, args.title))

    # index page
    js, wxml = PAGE_BUILDERS[args.type](args.title)
    with open(os.path.join(pages_dir, "index.js"), "w", encoding="utf-8") as f:
        f.write(js)
    with open(os.path.join(pages_dir, "index.wxml"), "w", encoding="utf-8") as f:
        f.write(wxml)
    with open(os.path.join(pages_dir, "index.wxss"), "w", encoding="utf-8") as f:
        f.write(APP_WXSS)
    with open(os.path.join(pages_dir, "index.json"), "w", encoding="utf-8") as f:
        f.write(dump({}))

    # readme
    with open(os.path.join(root, "README.md"), "w", encoding="utf-8") as f:
        f.write(make_readme(args.name, args.title, args.type))

    print(f"项目已生成：{root}")
    print(f"类型：{args.type}  名称：{args.title}")
    print("接下来：用微信开发者工具导入该目录（测试号即可预览）。")


if __name__ == "__main__":
    main()
