# Build Forcing for Wflow.jl

<https://deepwiki.com/jl-pkgs/Wflow-CUG.jl>


## Requirements

- ArcGIS


## 数据

| 变量             | 来源     |     | link                                                                          |
| ---------------- | -------- | --- | ----------------------------------------------------------------------------- |
| 城市不透水面比例 | Tsinghua |     | https://code.earthengine.google.com/3390857ccb75bc63d6f4527fac0c227d?noload=1 |
|                  |          |     |                                                                               |
|                  |          |     |                                                                               |


## ECMWF气象预报产品

```js
var date = ee.Date("2025-06-19");

// Get temperature forecasts created on 2025/03/26T12:00:00Z.
var forecasts = ee.ImageCollection('ECMWF/NRT_FORECAST/IFS/OPER')
    .filter(ee.Filter.gte('creation_time', date.millis()))
    // .select('temperature_2m_sfc')
    .sort('forecast_hours');
print(forecasts);
```
