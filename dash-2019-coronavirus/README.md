# 2019 Novel Coronavirus (COVID-19) Dashboard Monitor and Data Repository
[![license](https://img.shields.io/github/license/Perishleaf/data-visualisation-scripts)](https://github.com/Perishleaf/data-visualisation-scripts/blob/master/LICENSE)

English | [中文](https://github.com/Perishleaf/data-visualisation-scripts/blob/master/dash-2019-coronavirus/markdown_chinese/HowTo.md)

This public repository achives data and source code for building a dashboard for tracking spread of COVID-19 globally.

Tools used include python, dash, and plotly.

Data sourced from 
* [丁香园](https://ncov.dxy.cn/ncovh5/view/pneumonia?scene=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0)
* [Tencent News](https://news.qq.com//zt2020/page/feiyan.htm#charts)
* [Australia Government Department of Health](https://www.health.gov.au/news/coronavirus-update-at-a-glance)
* [worldometers](https://www.worldometers.info/coronavirus/)
* [National Health Commission of the People's Republic of China](http://www.nhc.gov.cn/)
* [JCU-CSSE](https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/htmlview?usp=sharing&sle=true#)

Dashboard is deployed on Heroku and can be accessed from https://dash-coronavirus-2020.herokuapp.com/

Additional details about how to build this dashboard can be accessed from [here](https://towardsdatascience.com/build-a-dashboard-to-track-the-spread-of-coronavirus-using-dash-90364f016764) and [here](https://towardsdatascience.com/elevate-your-dashboard-interactivity-in-dash-b655a0f45067)

__To-do list:__

- [x] Code optimisation for importing excel sheets data
- [x] Add donation widge
- [x] Add share slide
- [x] Code optimisation for calling coordinates using opencage geocoder
- [x] Code optimisation for scrapping data from various sources
- [x] Code optimisation for generating overview lineplot/reduce response time
- [ ] Layout and design

![App screenshot](./app_screenshot.gif)


