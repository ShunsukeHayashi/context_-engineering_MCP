import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import google.generativeai as genai

from workflow_models import Workflow, Task, Agent, AgentType, TaskStatus, WorkflowStatus

logger = logging.getLogger(__name__)

class WorkflowGenerator:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    async def generate_workflow(self, user_input: str, context: Optional[Dict] = None) -> Workflow:
        """
        ユーザーインプットからワークフローを自動生成
        """
        try:
            # プロンプトを作成
            prompt = self._create_workflow_prompt(user_input, context)
            
            # Geminiでワークフロー構造を生成
            response = self.model.generate_content(prompt)
            workflow_data = json.loads(response.text)
            
            # ワークフローオブジェクトを作成
            workflow = self._create_workflow_object(workflow_data, user_input)
            
            logger.info(f"Generated workflow '{workflow.title}' with {len(workflow.tasks)} tasks")
            return workflow
            
        except Exception as e:
            logger.error(f"Workflow generation failed: {str(e)}")
            raise
    
    def _create_workflow_prompt(self, user_input: str, context: Optional[Dict] = None) -> str:
        """ワークフロー生成用のプロンプトを作成"""
        
        context_info = ""
        if context:
            context_info = f"Context: {json.dumps(context, indent=2)}\n\n"
        
        return f"""
        {context_info}User Request: {user_input}

        Based on the user request above, generate a comprehensive workflow with the following structure:

        {{
            "workflow": {{
                "title": "Clear, descriptive title",
                "description": "Detailed description of what this workflow accomplishes",
                "estimated_duration_hours": 2.5
            }},
            "tasks": [
                {{
                    "title": "Task title",
                    "description": "Detailed task description",
                    "estimated_duration_minutes": 30,
                    "priority": 8,
                    "required_skills": ["skill1", "skill2"],
                    "dependencies": [], // array of task indices that must complete first
                    "agent_type": "researcher|analyst|developer|reviewer|coordinator|specialist"
                }}
            ],
            "agents": [
                {{
                    "name": "Agent Name",
                    "type": "researcher|analyst|developer|reviewer|coordinator|specialist",
                    "capabilities": ["capability1", "capability2"],
                    "max_concurrent_tasks": 3
                }}
            ]
        }}

        Guidelines:
        1. Break down the request into logical, manageable tasks
        2. Consider dependencies between tasks
        3. Assign appropriate agent types based on required skills
        4. Provide realistic time estimates
        5. Set priorities (1-10, where 10 is highest priority)
        6. Ensure the workflow is comprehensive and actionable

        Return only valid JSON without any additional text or markdown formatting.
        """
    
    def _create_workflow_object(self, workflow_data: Dict, user_input: str) -> Workflow:
        """生成されたデータからワークフローオブジェクトを作成"""
        
        # エージェントを作成
        agents = []
        for agent_data in workflow_data.get('agents', []):
            agent = Agent(
                name=agent_data['name'],
                type=AgentType(agent_data['type']),
                capabilities=agent_data.get('capabilities', []),
                max_concurrent_tasks=agent_data.get('max_concurrent_tasks', 3)
            )
            agents.append(agent)
        
        # タスクを作成
        tasks = []
        for i, task_data in enumerate(workflow_data.get('tasks', [])):
            # 依存関係を処理（インデックスからタスクIDに変換）
            dependencies = []
            for dep_index in task_data.get('dependencies', []):
                if 0 <= dep_index < len(tasks):
                    dependencies.append(tasks[dep_index].id)
            
            task = Task(
                title=task_data['title'],
                description=task_data['description'],
                estimated_duration=task_data.get('estimated_duration_minutes', 30),
                priority=task_data.get('priority', 5),
                dependencies=dependencies
            )
            tasks.append(task)
        
        # ワークフローを作成
        workflow_info = workflow_data.get('workflow', {})
        workflow = Workflow(
            title=workflow_info.get('title', f'Generated from: {user_input[:50]}...'),
            description=workflow_info.get('description', f'Workflow generated from user input: {user_input}'),
            input_data={'original_request': user_input, 'generated_at': datetime.now().isoformat()},
            status=WorkflowStatus.PLANNING,
            tasks=tasks,
            agents=agents
        )
        
        return workflow

class TaskDecomposer:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    async def decompose_task(self, task: Task, max_subtasks: int = 5) -> List[Task]:
        """
        大きなタスクを小さなサブタスクに分解
        """
        try:
            prompt = f"""
            Task to decompose:
            Title: {task.title}
            Description: {task.description}
            Estimated Duration: {task.estimated_duration} minutes
            Priority: {task.priority}

            Break this task down into {max_subtasks} or fewer smaller, more manageable subtasks.
            Each subtask should be:
            1. Specific and actionable
            2. Can be completed independently
            3. Takes 15-60 minutes
            4. Has clear success criteria

            Return JSON in this format:
            {{
                "subtasks": [
                    {{
                        "title": "Subtask title",
                        "description": "Detailed description with success criteria",
                        "estimated_duration_minutes": 30,
                        "priority": 7,
                        "dependencies": [] // indices of other subtasks this depends on
                    }}
                ]
            }}

            Return only valid JSON.
            """
            
            response = self.model.generate_content(prompt)
            subtask_data = json.loads(response.text)
            
            subtasks = []
            for i, subtask_info in enumerate(subtask_data.get('subtasks', [])):
                # 依存関係を処理
                dependencies = []
                for dep_index in subtask_info.get('dependencies', []):
                    if 0 <= dep_index < len(subtasks):
                        dependencies.append(subtasks[dep_index].id)
                
                subtask = Task(
                    title=subtask_info['title'],
                    description=subtask_info['description'],
                    estimated_duration=subtask_info.get('estimated_duration_minutes', 30),
                    priority=subtask_info.get('priority', task.priority),
                    dependencies=dependencies
                )
                subtasks.append(subtask)
            
            logger.info(f"Decomposed task '{task.title}' into {len(subtasks)} subtasks")
            return subtasks
            
        except Exception as e:
            logger.error(f"Task decomposition failed: {str(e)}")
            return [task]  # Return original task if decomposition fails