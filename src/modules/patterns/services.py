from src.utils import Utils

class PatternService:

    async def evaluate(self, code: str, pattern: str, patternList=None):
        # No hace falta generar inputs con POET en este caso
        payload = self._generate_payload(code, pattern, patternList)
        print("PAYLOAD:")
        print(payload)

        # Evaluar resultados
        return await Utils()._calculate_success_ratio(payload, "mc" if patternList else "wh_question")
        

    def _generate_payload(self, code, pattern, patternList=None): # Añadimos una lista que es opcional en el caso de utilizar el evaluador mc
        payload = [{
            "query": f"Given the following code: \"{code}\", which design pattern from these options is being applied?",
            "type": "mc_evaluator" if patternList else "wh_question",
            "expected_result": pattern
        }]
        if(patternList):
            options = " Option A) " + patternList[0] + " Option B) " + patternList[1] + " Option C) " + patternList[2] + ". Provide a response restricted with one of the values of the list including the letter of the option (A, B or C), whitout any explanation"
            payload[0]["query"] = payload[0]["query"] + options
            print(payload)
        return payload