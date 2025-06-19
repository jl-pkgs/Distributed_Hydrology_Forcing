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
ngrid = sum(!is.na(x)) # 1079 rids
ngrid/length(x)
