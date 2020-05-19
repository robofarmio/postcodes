import osmium
import geojson


class Postcodes(osmium.SimpleHandler):
    geom = osmium.geom.GeoJSONFactory()

    def __init__(self):
        super().__init__()
        self.features = []

    def area(self, a):
        tags = a.tags

        if "boundary" not in tags or tags["boundary"] != "postal_code":
            return

        if "postal_code" not in tags:
            return

        code = tags["postal_code"]

        if len(code) != 5:
            return

        geom = self.geom.create_multipolygon(a)
        geom = geojson.loads(geom)
        geom = geom["coordinates"]
        geom = geojson.MultiPolygon(geom)

        feat = geojson.Feature(geometry=geom, properties={"postcode": code})

        self.features.append(feat)


def main(args):
    postcodes = Postcodes()
    postcodes.apply_file(str(args.osm), locations=True)

    collection = geojson.FeatureCollection(postcodes.features)

    with args.out.open("w") as fp:
        geojson.dump(collection, fp)
