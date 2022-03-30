import json
from datetime import datetime
from typing import Type, TypeVar

from mongoengine import QuerySet

from nleaser_models.tasks import TaskSchema, TaskModel
from nleaser_models.user import UserModel
from nleaser_sources.rabbit.producer import RabbitProducer


TaskClassType = TypeVar('TaskClassType', bound=TaskModel)


class BaseTaskService:
    schema: TaskSchema

    def __init__(self, user: UserModel, model: Type[TaskClassType], rabbit_queue: str):
        self.user = user
        self._producer = RabbitProducer(rabbit_queue)
        self._TaskModel = model

    def create(self, task_id: str):
        """
        Cada service deve gerar um modelo de Task valido,
        e passar o Id da tarefa gerado para ser enviado a fila do rabbit
        Args:
            task_id: Id da tarefa, será transmitida para o rabbit

        """
        self._producer.send_message(
            json.dumps({
                "task": task_id
            })
        )

    def list_current_tasks(self, datafile_id: str) -> QuerySet:
        tasks = self._TaskModel.objects(
            owner=self.user, datafile=datafile_id
        ).order_by("-created_at").limit(5)

        if tasks.count() == 0:
            raise FileNotFoundError("Não existe nenhuma tarefa em progresso")
        return tasks

    def list_failed_tasks(self, datafile_id: str, data_inicial: datetime):
        failed_tasks = self._TaskModel.objects(
            owner=self.user, datafile=datafile_id,
            created_at__gte=data_inicial, status="error"
        ).order_by("-created_at")

        return failed_tasks

