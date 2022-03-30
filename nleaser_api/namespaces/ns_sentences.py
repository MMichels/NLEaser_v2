from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource, Model, fields

from nleaser_api.error_handler import error_handler
from nleaser_api.request_models.sentences_models import get_model, get_response_model, sentence_model

from nleaser_models.sentence import SentenceSchema

from nleaser_sources.app_services.datafile import DataFileAppService

from nleaser_sources.logger import create_logger

logger = create_logger(__name__)

ns_sentences = Namespace(
    "Sentences",
    "Namespace para manipular as sentenças de um arquivo"
)

# GET
list_sentendes_response_model = get_response_model.copy()
list_sentendes_response_model["sentences"] = fields.Nested(
    ns_sentences.model("sentence_model", sentence_model, mask=None),
    as_list=True, mask=None
)
list_sentendes_response_model: Model = ns_sentences.model(
    "list_sentences_response_model",
    list_sentendes_response_model,
    mask=None
)


@ns_sentences.route("")
class SentencesResource(Resource):
    schema = SentenceSchema()

    @ns_sentences.expect(get_model, validate=False)
    @ns_sentences.marshal_with(list_sentendes_response_model)
    @error_handler(logger)
    @jwt_required
    def get(self):
        args = get_model.parse_args()
        datafile_service = DataFileAppService()
        sentences, total = datafile_service.get_sentences(**args)

        return {
            "datafile_id": args["datafile_id"],
            "skip": args["skip"],
            "limit": args["limit"],
            "total": sentences.count(),
            "sentences": self.schema.dump(sentences, many=True)
        }
