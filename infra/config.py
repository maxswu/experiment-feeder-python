from pydantic import BaseModel, Field


class KafkaSettings(BaseModel):
    """
    Kafka settings
    """

    # Broker
    bootstrap_servers: str = Field(default=None, title='Bootstrap Servers')

    # Producer
    producer_client_id: str = Field(
        default='experiment-feeder-python', title='Client id for Producer'
    )

    @property
    def _broker_config_dict(self) -> dict:
        return {
            'bootstrap.servers': self.bootstrap_servers,
        }

    @property
    def producer_config_dict(self) -> dict:
        return self._broker_config_dict | {
            'client.id': self.producer_client_id,
        }
