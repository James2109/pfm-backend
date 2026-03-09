from typing import List
from google import genai
from google.genai import types

from src.models.plans import PlanLLmInput, PlanLLmOutput
from src.core.config import settings

import asyncio
import json
import yaml
from pathlib import Path

class GeminiService:
    def __init__(self, api_key: str, 
                 model: str = 'gemini-3-flash-preview'):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.prompt_template = self.load_prompt_template(settings.PROMPTS_DIR / "llm_prompt.yaml")

    def load_prompt_template(self, template_path: Path) -> dict:
        with open(template_path, 'r') as file:
            template = yaml.safe_load(file)
        return template

    async def generate_plan(self, plan_input: PlanLLmInput) -> PlanLLmOutput:
        user_prompt = self.prompt_template["user_prompt"].format(
            age=plan_input.age,
            position=plan_input.position.value,
            height=plan_input.height,
            weight=plan_input.weight,
            strength=plan_input.strength,
            weakness=plan_input.weakness,
            note=plan_input.note,
            frequency=plan_input.frequency.value,
            training_sessions=plan_input.training_sessions,
            cost_per_meal=plan_input.cost_per_meal,
        )
        system_prompt = self.prompt_template["system_prompt"]
        response_schema = self.prompt_template["response_schema"]

        response = await asyncio.to_thread(
            self.client.models.generate_content,
            model=self.model,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=response_schema,
            ),
        )

        result = json.loads(response.text)
        return PlanLLmOutput(**result)