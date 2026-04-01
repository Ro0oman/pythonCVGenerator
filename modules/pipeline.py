import asyncio
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class PipelineStep(ABC):
    """
    Base class for all pipeline steps.
    Each step must implement the 'execute' method.
    """
    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__

class JobPipeline:
    """
    Orchestrates the execution of multiple PipelineSteps.
    Maintains a shared state and handles errors.
    """
    def __init__(self, steps: List[PipelineStep]):
        self.steps = steps
        self.state = {}

    async def run(self, initial_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self.state = initial_state or {}
        print(f"🚀 Iniciando Pipeline: {len(self.steps)} pasos...")
        
        for step in self.steps:
            print(f"[*] Ejecutando: {step.name}...")
            try:
                # Update state with the result of the step
                result = await step.execute(self.state)
                self.state.update(result)
            except Exception as e:
                print(f"[!] Error crítico en {step.name}: {e}")
                raise e
        
        return self.state
