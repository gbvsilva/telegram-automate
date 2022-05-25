from tools.timezone import TZ
from datetime import datetime

class Rule():
    
    def __init__(self, rule):
        if rule == 'ate_tres_horas':
            self.rule_func = self.regra_ate_tres_horas
        elif rule == 'entre_8_14':
            self.rule_func = self.regra_entre_8_14
        else:
            self.rule_func = self.regra_sem

    async def execute(self):
        return await self.rule_func()

    async def regra_sem(self):
        return True

    async def regra_ate_tres_horas(self):
        agora = datetime.now(TZ)
        tres_horas = agora.replace(hour=15, minute=0, second=0, microsecond=0)
        return agora <= tres_horas

    async def regra_entre_8_14(self):
        agora = datetime.now(TZ)
        oito_horas = agora.replace(hour=8, minute=0, second=0, microsecond=0)
        duas_horas = agora.replace(hour=14, minute=0, second=0, microsecond=0)
        return agora >= oito_horas and agora <= duas_horas

