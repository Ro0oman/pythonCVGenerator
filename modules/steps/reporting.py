from modules.pipeline import PipelineStep
from modules.cost_controller import CostController

class CostReportingStep(PipelineStep):
    """
    Final step to report the total cost of the pipeline execution.
    """
    def __init__(self):
        self.cost_controller = CostController()

    async def execute(self, state: dict) -> dict:
        total_session = self.cost_controller.current_session_cost
        total_historical = self.cost_controller.get_total_historical_cost()
        
        print("\n" + "="*40)
        print("📊 REPORTE DE PROCESAMIENTO (V6.3)")
        print(f"💰 Coste esta sesión:  ${round(total_session, 6)}")
        print(f"🏦 Coste acumulado:    ${round(total_historical, 6)}")
        
        if state.get('github_missing'):
            print("\n" + "!"*40)
            print("⚠️ RECOMENDACIÓN CRÍTICA:")
            print("No se ha detectado una URL de GitHub en tu CV.")
            print("Es ALTAMENTE RECOMENDABLE incluir un portfolio")
            print("técnico para superar los filtros de reclutamiento.")
            print("!"*40)
            
        print("="*40 + "\n")
        
        return {"total_session_cost": total_session}
