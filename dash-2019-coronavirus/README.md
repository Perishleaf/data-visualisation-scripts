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
* [2020 coronavirus pandemic in Australia](https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Australia)
* [COVID-19 in US and Canada by 1Point3Acres](https://coronavirus.1point3acres.com/en)

Dashboard is deployed on Heroku and can be accessed from https://dash-coronavirus-2020.herokuapp.com/

Additional details about how to build this dashboard can be accessed from [here](https://towardsdatascience.com/build-a-dashboard-to-track-the-spread-of-coronavirus-using-dash-90364f016764) and [here](https://towardsdatascience.com/elevate-your-dashboard-interactivity-in-dash-b655a0f45067)

__To-do list:__

- [x] Code optimisation for importing excel sheets data 2020/03/01
- [x] Add donation widge 2020/03/02
- [x] Add share slide 2020/03/03
- [x] Code optimisation for calling coordinates using opencage geocoder 2020/03/05
- [x] Code optimisation for scrapping data from various sources 2020/03/15
- [x] Code optimisation for generating overview lineplot/reduce response time 2020/03/18
- [x] Clicking table tab now triggers corresponding changes in the plots 2020/03/24
- [x] Adding support for plots of Province/States 2020/03/24
- [ ] Layout and design

![App screenshot](./app_screenshot.gif)

###### DISCLAIMER
###### This website and its contents herein, including all data, mapping, and analysis, is provided to the public strictly for general information purposes only. All the information was collected from multiple publicly available data sources that do not always agree. While I'll try my best to keep the information up to date and correct, I make no representations or warranties of any kind, express or implied, about the completeness, accuracy, reliability, with respect to the website or the information. I do not bear any legal responsibility for any consequence caused by the use of the information provided. Reliance on the website for medical guidance or use of the website in commerce is strongly not recommended. Any action you take upon the information on this website is strictly at your own risk. and I will not be liable for any losses and damages in connection with the use of our website. Screenshots of the website are permissible so long as you provide appropriate credit.
