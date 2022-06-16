# heroku-degiro-app
Automatic trading for setting stop-losses and stock picking. The underlying trading
platform is DeGiro. The app will be run on daily basis and be hosted on heroku.

## 1. App make-up
### 1.1 Database
Using postgresql database which is a managed service from heroku. The etf's will be 
saved per asset class.

### 1.2 Portfolio
Will be focussing on etf's that can be freely traded to prevent trading cost from being
a factor to consider. Hope is to follow a momentum strategy with some automatic stop-loss
setting to prevent large portfolio loses.

## 2. Goal
I would like to be able to get an idea of which assets are performing well in the past. 
Find particular etf's that have a decent momentum. ETF picking will be done at my
discretion but setting of risk mitigating measure's should be automated, e.g. set
stop-loss at a certain statistically significant loss. 