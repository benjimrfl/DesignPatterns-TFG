from src.utils import Utils

class PatternService:

    async def evaluate(self, code: str, pattern: str):
        # No hace falta generar inputs con POET en este caso
        payload = self._generate_payload(code, pattern)
        print("PAYLOAD:")
        print(payload)

        # Evaluar resultados
        return await Utils()._calculate_success_ratio(payload, "wh_question")
        

    def _generate_payload(self, code, pattern, patternList=None): # Añadimos una lista que es opcional en el caso de utilizar el evaluador mc
        payload = [{
            "query": f"Given the following code: \"{code}\", which design pattern is being applied?",
            "type": "Pattern_Identification",
            "expected_result": pattern
        }]
        if(patternList):
            options = " Option A)" + patternList[0] + " Option B)" + patternList[1] + " Option C)" + patternList[2]
            payload["query"] = payload["query"] + options
            print(payload)
        return payload