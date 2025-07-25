import json
from fastapi import HTTPException
import requests


class EvaAPI:
    # BASE_URL = "http://150.214.230.39:8082/api/v1"
    BASE_URL = "http://localhost:8001/api/v1"

    def __init__(self, base_url=None):
        if base_url:
            self.BASE_URL = base_url

    def evaluate_output(self, evaluation_type, outputs, default):
        try:
            """
            Evaluate outputs generated by LLM.

            :param evaluation_type: Type of evaluation ("yes_no", "three_reasons", or "wh_question").
            :param outputs: List or single Output object (dict) with expected and generated results.
            :return: Evaluation results.
            """

            params = {"evaluation_type": evaluation_type, "default": default}
            headers = {"Content-Type": "application/json", "Accept": "application/json"}
            req = requests.Request(
                "POST",
                f"{self.BASE_URL}/evaluate",
                params=params,
                json=outputs,
                headers=headers,
            )

            prepared = req.prepare()
            response = requests.Session().send(prepared)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
