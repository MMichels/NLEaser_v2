from importlib.resources import Resource


class NerResource(Resource):
    def post(self, datafile_id):
        return datafile_id