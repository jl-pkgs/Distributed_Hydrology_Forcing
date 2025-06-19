# using Ipaper, Ipaper.sf, ArchGDAL
pacman::p_load(sf, sf2, terra)

ra = rast("./Project_Hubei_500m/flowdir.tif")
shp = read_sf("./shp/shed_湖北三市_[005]_八亩地.shp")

## 500m
range = st_range(shp, 1/10) # 
poly = st_rect(range) %>% vect()

r = crop(ra, poly) %>% mask(shp)

plot(r)
plot(shp, add = TRUE)

x = as.vector(r)
ngrid = sum(!is.na(x)) # 1079 grids
ngrid/length(x)

## Forcing_urban
ra = rast("data/ChinaUrban_500m_2018.tif")
ra2 = aggregate(ra, fact=2)
writeRaster(ra2, "data/ChinaUrban_1km_2018.tif")

ra_urban = rast("data/ChinaUrban_500m_2018.tif")
ra = crop(ra_urban, poly)
