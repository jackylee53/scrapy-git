# scrapy-git

## 为scrapy的练习项目
### 1、爬取糗事百科(https://www.qiushibaike.com/)
#### (1)爬取"热门"、"24小时"、"热图"、"文字"、"穿越"、"糗图"、"新鲜"栏目所有内容
#### (2)通过LinkExtractor提取分页信息,爬取段子的作者、内容、投票数以及图片信息
#### (3)内容通过filepipeline保存在json文件中

### 2、爬取百度贴吧(https://tieba.baidu.com/)
#### (1)传入搜索关键字,如"python爬虫",然后爬取与该关键词相关的所有帖子及每个帖子的跟帖信息；
#### (2)爬取帖子内容通过filepipeline保存在json文件中