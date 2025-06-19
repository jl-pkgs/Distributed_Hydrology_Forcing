var img = ee.ImageCollection("ESA/WorldCover/v200");


/**
 * Construct parameters depend on landcover type
 *
 * @param  {ee.Image} landcover [description]
 * @param  {ee.List}  list      [description]
 * @return {ee.Image}           [description]
 */
pkg_ET.propByLand = function (landcover, list) {
  function iter_sum(i, prev) {
    i = ee.Number(i);
    var land = landcover.eq(i).float();
    var prop = ee.Number(list.get(i));
    prop = land.multiply(prop);

    prev = ee.Image(prev).add(prop);
    return prev;
  }
  var prev = ee.List.sequence(0, 17).iterate(iter_sum, ee.Image(0));
  return ee.Image(prev);
}
