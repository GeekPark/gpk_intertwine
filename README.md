Web service for suggesting related articles.

## API

### Add article

`POST /index/add`,

example request body:

```json
{
  "article":  {
    "title": "从百度李彦宏到首次登月者巴兹·奥尔德林，这么多嘉宾是如何准时来到极客公园的？",
    "body": "1969 年 7 月 16 日，尼尔·阿姆斯特朗与巴兹·奥尔德林乘坐着阿波罗 11 号的土星 5 号火箭从地球起飞，在几天之后成功降落在了月球表面。站在整个人类历史上来说这无疑是开启了一个新的时代。\n\n而这位人类的太空英雄今年已经 86 岁了，在最近来到了北京，来到极客公园，为我们阐释他心目中太空探索能对社会、对科技带来的新变革。除此之外，李彦宏、雷军、罗永浩等科技领域先锋大佬也都来到极客公园，为我们带来这一年最值得期待的科技盛宴。\n《登月者奥尔德林自述：「冒险」就是我的宿命》\n\n《雷军：小米 MIX 压根就是玩儿，因为最坏的时候已经过去了》\n\n《一年提了513次人工智能的李彦宏和他的AI观》\n\n《罗永浩：春天一定会给大家惊喜，秋天会发布空气净化器》\n他们在商业、科技和文化等领域各有建树，是这个时代的创新驱动力，不受固有观念的束缚，用创新思维解读和应对一切事物与挑战。他们个性坚毅且充满激情，虽身处喧嚣世界，却依旧坚守心中的理想与情怀。\n而这与英菲尼迪 Q70L 这辆车所倡导的精神力量的回归，助力具有独立思想的创造者勇敢前行不谋而合，于是英菲尼迪与「极客公园创新大会」合作，共同对创新思维进行解读。\n\n 2017 年 1 月 14 日巴兹·奥尔德林是乘坐英菲尼迪 Q70L 来到北京极客公园现场的。这也许就能回答题目中的疑惑，没错，他们都是乘坐这款 2017 款英菲尼迪 Q70L 来到现场。\n\n另一方面，极客公园选择携手英菲尼迪也并不是因为简单的气质和所倡导的精神相似，更重要的是通过这款车的多项「黑科技」同样能够为我们的嘉宾保驾护航，并且提供高品质的乘坐体验，甚至是已经 86 岁的首次登月者巴兹·奥尔德林。\n来到北京，这辆车首先当然要能够「抵御生物攻击」，也就是「雾霾」，这款 Q70L 具有的独特的森林空调系统，可显著降低 PM 2.5，还能释放树木和绿叶的清香，为嘉宾带来清新空气和惬意感受，好在这两天北京天气都还不错，但有备无患。\n Google Assistant 的产品经理 Anantica Singh\n\n安全方面，超视距前端碰撞预警系统（PFCW）、倒车碰撞预防系统（BCI）、全速段智能巡航系统 (ICC)、车距控制辅助系统 (DCA)、车道偏离警告系统 (LDW) 及车道偏离修正系统 (LDP) 等，搭载了这些同级领先安全科技 Q70L 也许才能打动曾经乘坐过登月火箭的巴兹·奥尔德林。\n Google Daydream 的沉浸感设计总监 Jon Wiley\n3.5 升 V6 高性能混合动力系统，也是为了保证顺利按时穿过北京这个「赌城」准时来到大会的现场。VQ35HR V6 自然吸气发动机和单电机双离合器，以性能为导向，零至百公里/小时加速仅 5.1 秒。此外，得益于同级领先的锂电池混动技术，全新 Q70L 实现了车速高达 100km/h 下的纯电动行驶能力。\n\n拥有定制级 16 扬声器 Bose 音响系统等等这些细节之处同样比比皆是，总之作为同级唯一加长轴距的进口车型，全新 Q70L 不仅拥有至高品质，同样能够完美的把这些独立思想创造者和他们的思想一同精准的送达现场。\n而同时，坐落于三里屯的英菲尼迪品牌体验中心也设立了「极客公园创新大会」分会，将更多具有创新的思想与建树分享与众，并始终激励具有独立思想的创造者敢爱前行。\n\n每天都有 10 个幸运参会者到英菲尼迪三里屯品牌体验中心参与彩蛋任务，最终获胜者独享极客公园提供价值两千元的奖品。\n\n在这里，你看到的「创新」不只是科技圈的专属，「变革」不再只被程序员所引领，所有的一切也许都是气质相投。",
    "id": 217745,
    "tags": [
      "英菲尼迪"
    ]
  }
}
```

### Update article

`POST /index/update/<article_id>`

the request body is the same as that for adding articles.

### Delete article

`DELETE /index/<article_id>`

### Check related articles

`GET /related_to/<article_id>?count=100`

The request parameter `count` is optional, defaults to `10` if not specified.

example response:

```
{
  "ok": true,
  "result": [
    [
      217745,
      2.1894496615611327
    ],
    [
      217756,
      0.7561912361564439
    ],
    ...
  ]
}
```

### Inspect article record

`GET /inspect/article/<article_id>`

### Inspect meta data

`GET /inspect/meta`

### Force (re)train the model

`GET /train`

*This will probably take a few minutes to run.*

All related services will not be working before training.

The text corpus is acquired from article contents, so it is only useful to invoke this api when you have added enought articles.


## Copyright

Copyright (c) GeekPark Inc.


