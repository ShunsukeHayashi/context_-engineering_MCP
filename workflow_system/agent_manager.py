import logging
from typing import List, Dict, Optional, Any
from datetime import datetime
import json
import google.generativeai as genai

from workflow_models import Workflow, Task, Agent, AgentType, TaskStatus

logger = logging.getLogger(__name__)

class AgentManager:
    def __init__(self, gemini_api_key: str):
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    async def assign_tasks(self, workflow: Workflow) -> Dict[str, str]:
        """
        ワークフロー内のタスクを最適なエージェントにアサイン
        """
        assignments = {}
        ready_tasks = workflow.get_ready_tasks()
        available_agents = workflow.get_available_agents()
        
        for task in ready_tasks:
            best_agent = await self._find_best_agent(task, available_agents, workflow)
            if best_agent:
                self._assign_task_to_agent(task, best_agent)
                assignments[task.id] = best_agent.id
                
                # エージェントが満杯になったら除外
                if not best_agent.is_available:
                    available_agents.remove(best_agent)
        
        return assignments
    
    async def _find_best_agent(self, task: Task, agents: List[Agent], workflow: Workflow) -> Optional[Agent]:
        """
        タスクに最適なエージェントを選択
        """
        if not agents:
            return None
        
        try:
            # Gemini AIを使って最適なエージェントを選択
            prompt = self._create_agent_selection_prompt(task, agents, workflow)
            response = self.model.generate_content(prompt)
            selection_data = json.loads(response.text)
            
            selected_agent_id = selection_data.get('selected_agent_id')
            reasoning = selection_data.get('reasoning', '')
            
            # 選択されたエージェントを見つける
            for agent in agents:
                if agent.id == selected_agent_id:
                    logger.info(f"Assigned task '{task.title}' to agent '{agent.name}': {reasoning}")
                    return agent
            
            # フォールバック: 最初の利用可能なエージェント
            return agents[0] if agents else None
            
        except Exception as e:
            logger.error(f"Agent selection failed: {str(e)}")
            # フォールバック: 最初の利用可能なエージェント
            return agents[0] if agents else None
    
    def _create_agent_selection_prompt(self, task: Task, agents: List[Agent], workflow: Workflow) -> str:
        """エージェント選択用のプロンプトを作成"""
        
        agents_info = []
        for agent in agents:
            agents_info.append({
                'id': agent.id,
                'name': agent.name,
                'type': agent.type.value,
                'capabilities': agent.capabilities,
                'current_load': f"{len(agent.current_tasks)}/{agent.max_concurrent_tasks}",
                'load_percentage': agent.load_percentage
            })
        
        return f"""
        Task to assign:
        Title: {task.title}
        Description: {task.description}
        Priority: {task.priority}
        Estimated Duration: {task.estimated_duration} minutes

        Available Agents:
        {json.dumps(agents_info, indent=2)}

        Workflow Context:
        Title: {workflow.title}
        Total Tasks: {len(workflow.tasks)}
        Progress: {workflow.progress_percentage:.1f}%

        Select the best agent for this task considering:
        1. Agent capabilities matching task requirements
        2. Current workload and availability
        3. Agent type suitability for the task
        4. Overall workflow efficiency

        Return JSON in this format:
        {{
            "selected_agent_id": "agent_id_here",
            "reasoning": "Explanation of why this agent was selected",
            "confidence": 0.85
        }}

        Return only valid JSON.
        """
    
    def _assign_task_to_agent(self, task: Task, agent: Agent):
        """タスクをエージェントにアサイン"""
        task.assigned_agent_id = agent.id
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()
        agent.current_tasks.append(task.id)
    
    async def reassign_task(self, task: Task, workflow: Workflow, reason: str = "") -> Optional[Agent]:
        """
        タスクを別のエージェントに再アサイン
        """
        # 現在のエージェントから解除
        if task.assigned_agent_id:
            current_agent = next((a for a in workflow.agents if a.id == task.assigned_agent_id), None)
            if current_agent and task.id in current_agent.current_tasks:
                current_agent.current_tasks.remove(task.id)
        
        # 新しいエージェントを見つけて再アサイン
        available_agents = workflow.get_available_agents()
        new_agent = await self._find_best_agent(task, available_agents, workflow)
        
        if new_agent:
            self._assign_task_to_agent(task, new_agent)
            logger.info(f"Reassigned task '{task.title}' to agent '{new_agent.name}'. Reason: {reason}")
            return new_agent
        
        return None
    
    def get_agent_performance_metrics(self, agent: Agent, workflow: Workflow) -> Dict[str, Any]:
        """エージェントのパフォーマンス指標を取得"""
        agent_tasks = [task for task in workflow.tasks if task.assigned_agent_id == agent.id]
        
        completed_tasks = [task for task in agent_tasks if task.status == TaskStatus.COMPLETED]
        failed_tasks = [task for task in agent_tasks if task.status == TaskStatus.FAILED]
        
        total_estimated_time = sum(task.estimated_duration or 0 for task in completed_tasks)
        total_actual_time = sum(task.duration_minutes or 0 for task in completed_tasks)
        
        return {
            'agent_id': agent.id,
            'agent_name': agent.name,
            'total_tasks': len(agent_tasks),
            'completed_tasks': len(completed_tasks),
            'failed_tasks': len(failed_tasks),
            'success_rate': len(completed_tasks) / len(agent_tasks) if agent_tasks else 0,
            'current_load': len(agent.current_tasks),
            'load_percentage': agent.load_percentage,
            'average_task_duration': sum(task.duration_minutes or 0 for task in completed_tasks) / len(completed_tasks) if completed_tasks else 0,
            'efficiency_ratio': total_estimated_time / total_actual_time if total_actual_time > 0 else 1.0
        }

class WorkflowExecutor:
    def __init__(self, gemini_api_key: str):
        self.agent_manager = AgentManager(gemini_api_key)
        
    async def execute_workflow(self, workflow: Workflow) -> None:
        """
        ワークフローを実行
        """
        workflow.status = WorkflowStatus.EXECUTING
        workflow.started_at = datetime.now()
        
        while workflow.progress_percentage < 100:
            # 準備完了のタスクをアサイン
            assignments = await self.agent_manager.assign_tasks(workflow)
            
            if not assignments:
                # アサインできるタスクがない場合は、完了を待つかブロックされたタスクを処理
                blocked_tasks = [task for task in workflow.tasks if task.status == TaskStatus.BLOCKED]
                if blocked_tasks:
                    await self._handle_blocked_tasks(blocked_tasks, workflow)
                break
            
            # ここで実際のタスク実行ロジックを呼び出す
            # （実際の実装では、エージェントが非同期でタスクを実行）
            
        if workflow.progress_percentage == 100:
            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.now()
    
    async def _handle_blocked_tasks(self, blocked_tasks: List[Task], workflow: Workflow) -> None:
        """ブロックされたタスクを処理"""
        for task in blocked_tasks:
            # 依存関係を再チェック
            completed_task_ids = {t.id for t in workflow.tasks if t.status == TaskStatus.COMPLETED}
            
            if all(dep_id in completed_task_ids for dep_id in task.dependencies):
                task.status = TaskStatus.PENDING
                logger.info(f"Unblocked task '{task.title}'")
    
    def get_workflow_status(self, workflow: Workflow) -> Dict[str, Any]:
        """ワークフローの現在の状態を取得"""
        return {
            'workflow_id': workflow.id,
            'title': workflow.title,
            'status': workflow.status.value,
            'progress_percentage': workflow.progress_percentage,
            'task_distribution': {status.value: count for status, count in workflow.task_distribution.items()},
            'total_tasks': len(workflow.tasks),
            'total_agents': len(workflow.agents),
            'created_at': workflow.created_at.isoformat(),
            'started_at': workflow.started_at.isoformat() if workflow.started_at else None,
            'completed_at': workflow.completed_at.isoformat() if workflow.completed_at else None,
            'estimated_completion': self._estimate_completion_time(workflow)
        }
    
    def _estimate_completion_time(self, workflow: Workflow) -> Optional[str]:
        """完了予定時刻を推定"""
        if workflow.status == WorkflowStatus.COMPLETED:
            return None
        
        remaining_tasks = [task for task in workflow.tasks if task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]]
        if not remaining_tasks:
            return None
        
        total_remaining_time = sum(task.estimated_duration or 30 for task in remaining_tasks)
        available_agents = len(workflow.get_available_agents())
        
        if available_agents > 0:
            estimated_minutes = total_remaining_time / available_agents
            estimated_completion = datetime.now() + timedelta(minutes=estimated_minutes)
            return estimated_completion.isoformat()
        
        return None