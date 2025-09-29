"""
Performia Performance Management Agent
A custom MCP server for performance management workflows
"""

from fastmcp import FastMCP
from datetime import datetime, timedelta
import json
import sqlite3
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

# Initialize the MCP server
mcp = FastMCP("performia-agent")

# Data models
class Employee(BaseModel):
    id: str
    name: str
    department: str
    role: str
    manager_id: Optional[str]

class PerformanceMetric(BaseModel):
    employee_id: str
    metric_name: str
    value: float
    date: datetime
    category: str  # productivity, quality, collaboration, etc.

class PerformanceReview(BaseModel):
    employee_id: str
    reviewer_id: str
    period_start: datetime
    period_end: datetime
    overall_rating: float
    feedback: str
    goals: List[str]

# Initialize database
def init_db():
    conn = sqlite3.connect('performia.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        department TEXT,
        role TEXT,
        manager_id TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        metric_name TEXT,
        value REAL,
        date TEXT,
        category TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT,
        reviewer_id TEXT,
        period_start TEXT,
        period_end TEXT,
        overall_rating REAL,
        feedback TEXT,
        goals TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Tool: Collect Performance Data
@mcp.tool()
async def collect_performance_data(
    employee_id: str,
    metric_name: str,
    value: float,
    category: str = "general"
) -> Dict[str, Any]:
    """
    Collect and store performance metric for an employee
    """
    conn = sqlite3.connect('performia.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO metrics (employee_id, metric_name, value, date, category)
    VALUES (?, ?, ?, ?, ?)
    ''', (employee_id, metric_name, value, datetime.now().isoformat(), category))
    
    conn.commit()
    metric_id = cursor.lastrowid
    conn.close()
    
    return {
        "status": "success",
        "metric_id": metric_id,
        "employee_id": employee_id,
        "metric": metric_name,
        "value": value,
        "category": category,
        "timestamp": datetime.now().isoformat()
    }

# Tool: Analyze Performance Trends
@mcp.tool()
async def analyze_performance_trends(
    employee_id: str,
    days: int = 30,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """
    Analyze performance trends for an employee over a specified period
    """
    conn = sqlite3.connect('performia.db')
    cursor = conn.cursor()
    
    start_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    if category:
        cursor.execute('''
        SELECT metric_name, AVG(value) as avg_value, COUNT(*) as count,
               MIN(value) as min_value, MAX(value) as max_value
        FROM metrics
        WHERE employee_id = ? AND date >= ? AND category = ?
        GROUP BY metric_name
        ''', (employee_id, start_date, category))
    else:
        cursor.execute('''
        SELECT metric_name, AVG(value) as avg_value, COUNT(*) as count,
               MIN(value) as min_value, MAX(value) as max_value
        FROM metrics
        WHERE employee_id = ? AND date >= ?
        GROUP BY metric_name
        ''', (employee_id, start_date))
    
    results = cursor.fetchall()
    conn.close()
    
    trends = []
    for row in results:
        trends.append({
            "metric": row[0],
            "average": row[1],
            "data_points": row[2],
            "minimum": row[3],
            "maximum": row[4]
        })
    
    return {
        "employee_id": employee_id,
        "period_days": days,
        "category": category,
        "trends": trends,
        "analysis_date": datetime.now().isoformat()
    }

# Tool: Generate Performance Feedback
@mcp.tool()
async def generate_performance_feedback(
    employee_id: str,
    period_days: int = 30
) -> Dict[str, Any]:
    """
    Generate AI-assisted performance feedback based on collected metrics
    """
    # First get the trends
    trends = await analyze_performance_trends(employee_id, period_days)
    
    # Generate feedback based on trends
    feedback_points = []
    strengths = []
    improvements = []
    
    for trend in trends["trends"]:
        avg = trend["average"]
        metric = trend["metric"]
        
        # Simple logic for demo - in production, this would use ML models
        if avg >= 80:
            strengths.append(f"Excellent performance in {metric} (avg: {avg:.1f})")
        elif avg >= 60:
            feedback_points.append(f"Good progress in {metric} (avg: {avg:.1f})")
        else:
            improvements.append(f"Focus area: {metric} (current avg: {avg:.1f})")
    
    return {
        "employee_id": employee_id,
        "period_days": period_days,
        "strengths": strengths,
        "feedback_points": feedback_points,
        "areas_for_improvement": improvements,
        "generated_at": datetime.now().isoformat(),
        "recommendation": "Schedule 1:1 to discuss progress" if improvements else "Keep up the excellent work!"
    }

# Tool: Schedule Performance Review
@mcp.tool()
async def schedule_performance_review(
    employee_id: str,
    reviewer_id: str,
    review_date: str,
    preparation_tasks: List[str] = None
) -> Dict[str, Any]:
    """
    Schedule and prepare for a performance review
    """
    if preparation_tasks is None:
        preparation_tasks = [
            "Collect 360 feedback",
            "Review previous goals",
            "Analyze performance metrics",
            "Prepare development plan"
        ]
    
    # In production, this would integrate with calendar systems
    return {
        "employee_id": employee_id,
        "reviewer_id": reviewer_id,
        "scheduled_date": review_date,
        "preparation_tasks": preparation_tasks,
        "status": "scheduled",
        "notifications_sent": True,
        "meeting_link": f"https://meet.performia.com/review/{employee_id}",
        "created_at": datetime.now().isoformat()
    }

# Tool: Create Development Plan
@mcp.tool()
async def create_development_plan(
    employee_id: str,
    goals: List[str],
    timeline_days: int = 90
) -> Dict[str, Any]:
    """
    Create a personalized development plan for an employee
    """
    milestones = []
    for i, goal in enumerate(goals, 1):
        milestone_date = datetime.now() + timedelta(days=(timeline_days // len(goals)) * i)
        milestones.append({
            "goal": goal,
            "target_date": milestone_date.isoformat(),
            "milestone": i,
            "status": "pending"
        })
    
    return {
        "employee_id": employee_id,
        "plan_id": f"DEV-{employee_id}-{datetime.now().strftime('%Y%m%d')}",
        "goals": goals,
        "milestones": milestones,
        "timeline_days": timeline_days,
        "created_at": datetime.now().isoformat(),
        "next_checkpoint": milestones[0]["target_date"] if milestones else None
    }

# Tool: Team Performance Dashboard
@mcp.tool()
async def get_team_dashboard(
    department: str,
    period_days: int = 30
) -> Dict[str, Any]:
    """
    Get performance dashboard for an entire team/department
    """
    conn = sqlite3.connect('performia.db')
    cursor = conn.cursor()
    
    start_date = (datetime.now() - timedelta(days=period_days)).isoformat()
    
    # Get team metrics
    cursor.execute('''
    SELECT e.name, AVG(m.value) as avg_performance, COUNT(m.id) as metric_count
    FROM employees e
    LEFT JOIN metrics m ON e.id = m.employee_id
    WHERE e.department = ? AND m.date >= ?
    GROUP BY e.id, e.name
    ORDER BY avg_performance DESC
    ''', (department, start_date))
    
    team_metrics = cursor.fetchall()
    conn.close()
    
    team_data = []
    for row in team_metrics:
        team_data.append({
            "employee_name": row[0],
            "average_performance": row[1],
            "metrics_collected": row[2]
        })
    
    return {
        "department": department,
        "period_days": period_days,
        "team_size": len(team_data),
        "team_members": team_data,
        "team_average": sum(m["average_performance"] for m in team_data) / len(team_data) if team_data else 0,
        "generated_at": datetime.now().isoformat()
    }

# Resource: Performance Management Best Practices
@mcp.resource("performance-best-practices")
async def get_best_practices() -> str:
    """
    Performance management best practices and guidelines
    """
    return """
# Performance Management Best Practices

## Regular Feedback
- Provide feedback weekly, not just annually
- Focus on specific behaviors and outcomes
- Balance positive recognition with constructive feedback

## Goal Setting
- Use SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
- Align individual goals with team and company objectives
- Review and adjust goals quarterly

## Development Focus
- Identify strengths and leverage them
- Create actionable development plans
- Provide learning opportunities and resources

## Data-Driven Decisions
- Track multiple performance metrics
- Look for trends, not just snapshots
- Use both quantitative and qualitative data

## Continuous Improvement
- Regular 1:1 meetings
- 360-degree feedback
- Career development discussions
"""

# Prompt: Performance Review Assistant
@mcp.prompt()
async def performance_review_prompt(employee_name: str) -> str:
    """
    Generate a performance review prompt for an employee
    """
    return f"""
You are conducting a performance review for {employee_name}.

Please help me:
1. Analyze their recent performance metrics
2. Identify key strengths and achievements
3. Highlight areas for development
4. Create actionable goals for the next quarter
5. Suggest development opportunities

Use the available tools to:
- Collect and analyze performance data
- Generate feedback based on trends
- Create a development plan
- Schedule follow-up reviews

Remember to be constructive, specific, and forward-looking in your feedback.
"""

if __name__ == "__main__":
    # Run the server
    mcp.run()
