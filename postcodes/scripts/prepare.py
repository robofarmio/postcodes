import geojson
import shapely.geometry


def main(args):
    with args.postcodes.open() as fp:
        collection = geojson.load(fp)

    features = []

    for feature in collection["features"]:
        prop = feature["properties"]
        code = prop["postcode"]

        geom = feature["geometry"]
        assert geom["type"] == "MultiPolygon"

        geom = shapely.geometry.mapping(geom)
        assert geom.is_valid

        geom = shapely.geometry.shape(geom)
        assert geom.is_valid

        box = geom.bounds
        box = shapely.geometry.box(*box)
        box = shapely.geometry.mapping(box)
        box = geojson.Polygon(box["coordinates"])

        feat = geojson.Feature(geometry=box, properties={"postcode": code})

        features.append(feat)

    collection = geojson.FeatureCollection(features)

    with args.out.open("w") as fp:
        geojson.dump(collection, fp)
