import collections

import geojson
import shapely.ops
import shapely.geometry


def main(args):
    with args.boxes.open() as fp:
        collection = geojson.load(fp)

    levels = collections.defaultdict(list)

    for feature in collection["features"]:
        prop = feature["properties"]
        code = prop["postcode"]

        geom = feature["geometry"]
        assert geom["type"] == "Polygon"

        geom = shapely.geometry.mapping(geom)
        assert geom.is_valid

        geom = shapely.geometry.shape(geom)
        assert geom.is_valid

        assert code not in levels, "one area per post code"
        assert len(code) == 5, "german post codes are five characters long"

        for i in range(5):
            levels[code[0: i + 1]].append(geom)

    # Note: building up the levels from the bottom up would be more
    # efficient; but also requires multiple passes over the features.

    features = []

    for prefix, boxes in levels.items():
        box = shapely.ops.unary_union(boxes)
        box = box.bounds
        box = shapely.geometry.box(*box)
        box = shapely.geometry.mapping(box)
        box = geojson.Polygon(box["coordinates"])

        feat = geojson.Feature(geometry=box, properties={"postcode": prefix})

        features.append(feat)

    collection = geojson.FeatureCollection(features)

    with args.out.open("w") as fp:
        geojson.dump(collection, fp)
