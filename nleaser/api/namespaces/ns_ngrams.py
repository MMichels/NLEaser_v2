from flask_jwt_extended import jwt_required
from flask_restplus import Namespace, Resource

from nleaser.api.error_handler import error_handler
from nleaser.api.request_models.ngram_models import post_model, post_response_model
from nleaser.models.ngrams import NGramsSchema
from nleaser.sources.logger import create_logger
from nleaser.sources.ngrams import NGramsService

logger = create_logger(__name__)
ns_ngrams = Namespace(
    "NGrams",
    "Namespace para criar, verificar e excluir modelos de NGrams dos conjuntos de texto")

# POST
create_ngram_response_model = ns_ngrams.model(
    "create_ngram_response_model", post_response_model
)


@ns_ngrams.route("/<string:datafile_id>", methods=["POST", "GET", "DELETE"])
class NGramsResource(Resource):
    ngrams_schema = NGramsSchema()

    @ns_ngrams.expect(post_model, validate=False)
    @ns_ngrams.marshal_with(create_ngram_response_model, code=201)
    @error_handler(logger)
    @jwt_required
    def post(self, datafile_id: str):
        """
            Solicita um novo NGram
        """
        args = post_model.parse_args()
        service = NGramsService(datafile_id)
        create_ngram_task = service.create_ngram(**args)
        return {
            "create_ngram_task_id": create_ngram_task.id
        }
