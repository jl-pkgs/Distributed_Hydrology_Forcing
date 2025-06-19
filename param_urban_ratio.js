/**
 * 城市不透水界面比例, resample [30m -> 500m]
 * Dongdong Kong, 2025-06-19
 */
var img_urban = ee.Image("Tsinghua/FROM-GLC/GAIA/v10"); // 1985-2018;
var pkgs = require('users/kongdd/pkgs:pkgs');

var options = {
  type: "drive",
  // range: [-180, -60, 180, 90], // [73, 25, 105, 40], 
  range: [70, 15, 140, 55], // [73, 25, 105, 40], 
  cellsize: 1 / 120,
  crs: 'EPSG:4326', // 'SR-ORG:6974', // EPSG:4326
  folder: 'PMLV2'
};

// From 34 (year: 1985) to 1 (year: 2018)
var vis = { min: 1985, max: 2018, palette: ['red', 'white', 'blue'] };
pkgs.legend(vis, "Urban year");

var vis_ratio = { min: 0, max: 0.5, palette: ['green', 'white', 'red'] };
pkgs.legend(vis_ratio, "Urban Ratio");

var cellsize = 1 / 3600;
var targetScale = 1 / 240; // 

img_urban = img_urban.expression("35 - b() + 1984");
Map.addLayer(img_urban, vis, "origin");
Map.addLayer(points, {}, 'points');

// From 1 (year: 1985) to 34 (year: 2018)
// var years = [1985, 1990, 1995, 2000, 2005, 2010, 2015];
var years = [2018];
// var years = [1990];

var mask_small = false;
var n = years.length;
for (var i = 0; i < n; i++) {
  // var img_perc = img_urban.mask().multiply(1.0);
  var year = years[i];
  var mask = img_urban.lte(year).unmask(0); // bool: 0, 1

  if (mask_small) {
    var img_connect = mask.connectedPixelCount(1e3);
    var mask2 = img_connect.gt(500);
    mask = mask.updateMask(mask2);
    // img_connect = img_connect.updateMask(mask2);
    // Map.addLayer(img_connect, {min:0, max:1e3, palette:['blue', 'white', 'red']}, "connect");
  }
  // var img = img_urban.updateMask(mask);
  // var img_big = img.updateMask();

  var img_perc =
    mask.reduceResolution({ reducer: 'mean', maxPixels: 65536 })
      .reproject(ee.Projection('EPSG:4326').scale(targetScale, targetScale)).toFloat();
  // .reproject(ee.Projection('EPSG:4326').scale(targetScale, targetScale));
  var title = "" + year;
  // Map.addLayer(img, vis, "img", true);
  // Map.addLayer(img_big, vis, "img_big", true);
  // var img_perc = img_perc.updateMask(mask);
  // mask = mask.toFloat();
  // print(mask)
  // Map.addLayer(img_perc, vis_ratio, "perc");
  // options.cellsize = 1/120;
  // pkgs.ExportImg(mask, 'ChinaUrban_1km_'+year, options);

  options.cellsize = targetScale;
  var task = 'China_UrbanRatio_G' + 1 / targetScale + "_" + year; //+ "_con500"; 
  pkgs.ExportImg(img_perc, task, options);
}
