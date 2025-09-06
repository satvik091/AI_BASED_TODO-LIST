import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict
import random

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'completed_tasks' not in st.session_state:
    st.session_state.completed_tasks = []
if 'user_points' not in st.session_state:
    st.session_state.user_points = 0
if 'streak_days' not in st.session_state:
    st.session_state.streak_days = 0
if 'achievements' not in st.session_state:
    st.session_state.achievements = []

class AIToDoApp:
    def __init__(self):
        self.emojis = {
            "Work": "💼", "Personal": "🏠", "Health": "💪", 
            "Learning": "📚", "Finance": "💰", "Other": "⭐",
            "High": "🔴", "Medium": "🟡", "Low": "🟢"
        }
        
        # Accessible color scheme
        self.chart_colors = {
            'category_colors': ['#2563eb', '#0d9488', '#059669', '#d97706', '#dc2626', '#7c3aed'],
            'priority_colors': ['#dc2626', '#d97706', '#059669'],
            'success_colors': ['#059669', '#10b981', '#34d399']
        }
        
        self.fun_messages = [
            "You're doing amazing! Keep it up!",
            "Every small step counts!",
            "You're on fire today!",
            "Productivity wizard at work!",
            "Crushing those goals!",
            "Making magic happen!",
            "Champion mindset activated!"
        ]
        
        self.productivity_tips = [
            "Try the Pomodoro technique: 25 minutes focus, 5 minutes break",
            "Listen to focus music or nature sounds while working",
            "Start with the easiest task to build momentum",
            "Take deep breaths before starting difficult tasks",
            "Use colorful sticky notes for visual reminders",
            "Set a timer and race against it",
            "Reward yourself with healthy snacks after completing tasks",
            "Celebrate every small win - you deserve it!"
        ]
        
        self.achievements = [
            {"name": "First Steps", "desc": "Complete your first task", "emoji": "👶", "points": 10},
            {"name": "Getting Started", "desc": "Complete 5 tasks", "emoji": "🌱", "points": 25},
            {"name": "Task Master", "desc": "Complete 20 tasks", "emoji": "🏆", "points": 50},
            {"name": "Streak Starter", "desc": "Complete tasks for 3 days", "emoji": "🔥", "points": 30},
            {"name": "Week Warrior", "desc": "Complete tasks for 7 days", "emoji": "⚡", "points": 70},
            {"name": "Priority Pro", "desc": "Complete 5 high priority tasks", "emoji": "🎯", "points": 40}
        ]

    def get_accessible_css(self):
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-blue: #2563eb;
            --primary-blue-light: #3b82f6;
            --secondary-teal: #0d9488;
            --success-green: #059669;
            --warning-amber: #d97706;
            --error-red: #dc2626;
            --neutral-50: #f8fafc;
            --neutral-100: #f1f5f9;
            --neutral-200: #e2e8f0;
            --neutral-700: #334155;
            --neutral-800: #1e293b;
        }
        
        .stApp {
            font-family: 'Inter', 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: var(--neutral-700);
        }
        
        .main-header {
            background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-teal) 100%);
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
            color: white;
            font-size: 2.25rem;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .metric-card {
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            margin: 0.5rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            font-family: 'Inter', sans-serif;
        }
        
        .metric-primary { background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-blue-light) 100%); }
        .metric-success { background: linear-gradient(135deg, var(--success-green) 0%, #10b981 100%); }
        .metric-info { background: linear-gradient(135deg, var(--secondary-teal) 0%, #14b8a6 100%); }
        .metric-warning { background: linear-gradient(135deg, var(--warning-amber) 0%, #f59e0b 100%); }
        
        .task-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            border-left: 4px solid var(--secondary-teal);
            border: 1px solid var(--neutral-200);
        }
        
        .fun-card {
            background: linear-gradient(135deg, var(--primary-blue-light) 0%, var(--secondary-teal) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            color: white;
            margin: 1rem 0;
            line-height: 1.7;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-teal) 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        </style>
        """

    def check_achievements(self):
        completed_count = len(st.session_state.completed_tasks)
        new_achievements = []
        
        achievement_checks = [
            (completed_count >= 1, "First Steps"),
            (completed_count >= 5, "Getting Started"),
            (completed_count >= 20, "Task Master"),
            (st.session_state.streak_days >= 3, "Streak Starter"),
            (st.session_state.streak_days >= 7, "Week Warrior")
        ]
        
        for condition, achievement_name in achievement_checks:
            if condition and achievement_name not in st.session_state.achievements:
                st.session_state.achievements.append(achievement_name)
                new_achievements.append(achievement_name)
                
        return new_achievements

    def generate_ai_guidance(self, task_title: str, priority: str, category: str) -> str:
        guidance_templates = {
            "High": f"Mission Critical! '{task_title}' needs immediate attention. Focus and conquer!",
            "Medium": f"Steady progress on '{task_title}' will lead to success. Take your time!",
            "Low": f"'{task_title}' is perfect for a relaxed approach. Enjoy the process!"
        }
        
        base_guidance = guidance_templates.get(priority, guidance_templates["Medium"])
        tip = random.choice(self.productivity_tips)
        
        return f"{base_guidance}\\n\\nTip: {tip}"

    def calculate_priority_score(self, priority: str, days_until_due: int, category: str) -> float:
        priority_weights = {"High": 10, "Medium": 6, "Low": 3}
        base_score = priority_weights.get(priority, 6)
        
        if days_until_due <= 1:
            urgency_multiplier = 2.0
        elif days_until_due <= 3:
            urgency_multiplier = 1.5
        else:
            urgency_multiplier = 1.0
            
        return base_score * urgency_multiplier

    def get_productivity_insights(self, tasks: List[Dict], completed_tasks: List[Dict]) -> Dict:
        total_tasks = len(tasks) + len(completed_tasks)
        completion_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        
        category_counts = {}
        priority_counts = {}
        
        for task in tasks + completed_tasks:
            category = task.get('category', 'Other')
            priority = task.get('priority', 'Medium')
            category_counts[category] = category_counts.get(category, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        overdue_count = 0
        today = datetime.now().date()
        
        for task in tasks:
            if task.get('due_date'):
                due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                if due_date < today:
                    overdue_count += 1
        
        return {
            "total_tasks": total_tasks,
            "completion_rate": completion_rate,
            "overdue_count": overdue_count,
            "category_distribution": category_counts,
            "priority_distribution": priority_counts,
            "active_tasks": len(tasks)
        }

    def run(self):
        st.set_page_config(
            page_title="AI Task Adventure",
            page_icon="🎯",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.markdown(self.get_accessible_css(), unsafe_allow_html=True)
        
        st.markdown('<div class="main-header">AI Task Adventure<br><small>Where Productivity Meets Fun!</small></div>', unsafe_allow_html=True)
        
        # Sidebar
        st.sidebar.markdown("### Your Progress")
        st.sidebar.metric("Points", st.session_state.user_points)
        st.sidebar.metric("Streak", f"{st.session_state.streak_days} days")
        st.sidebar.metric("Achievements", len(st.session_state.achievements))
        
        page = st.sidebar.selectbox("Navigate:", 
                                   ["Task Manager", "AI Insights", "Analytics", "Achievements"])
        
        if page == "Task Manager":
            self.task_manager_page()
        elif page == "AI Insights":
            self.ai_insights_page()
        elif page == "Analytics":
            self.analytics_page()
        else:
            self.achievements_page()

    def task_manager_page(self):
        st.markdown("## Task Command Center")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        stats = [
            (col1, "🎯", len(st.session_state.tasks), "Active Tasks", "metric-primary"),
            (col2, "✅", len(st.session_state.completed_tasks), "Completed", "metric-success"),
            (col3, "📈", f"{(len(st.session_state.completed_tasks) / max(1, len(st.session_state.tasks) + len(st.session_state.completed_tasks)) * 100):.1f}%", "Success Rate", "metric-info"),
            (col4, "⭐", st.session_state.user_points, "Points", "metric-warning")
        ]
        
        for col, emoji, value, label, css_class in stats:
            with col:
                st.markdown(f'''
                <div class="metric-card {css_class}">
                    <div style="font-size: 2rem;">{emoji}</div>
                    <div style="font-size: 1.6rem; font-weight: 600; margin: 0.5rem 0;">{value}</div>
                    <div style="font-size: 1rem;">{label}</div>
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Add new task
        st.markdown("### Create New Task")
        
        col1, col2 = st.columns(2)
        with col1:
            task_title = st.text_input("Task Title", placeholder="Enter your task...")
            category = st.selectbox("Category", ["Work", "Personal", "Health", "Learning", "Finance", "Other"])
            
        with col2:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            due_date = st.date_input("Due Date", min_value=datetime.now().date())
        
        task_description = st.text_area("Description (Optional)")
        
        if st.button("Create Task", type="primary"):
            if task_title:
                days_until_due = (due_date - datetime.now().date()).days
                
                new_task = {
                    "id": len(st.session_state.tasks) + len(st.session_state.completed_tasks) + 1,
                    "title": task_title,
                    "description": task_description,
                    "category": category,
                    "priority": priority,
                    "due_date": due_date.strftime('%Y-%m-%d'),
                    "created_date": datetime.now().strftime('%Y-%m-%d %H:%M'),
                    "priority_score": self.calculate_priority_score(priority, days_until_due, category),
                    "ai_guidance": self.generate_ai_guidance(task_title, priority, category)
                }
                
                st.session_state.tasks.append(new_task)
                st.success(f"Task '{task_title}' created successfully!")
                st.rerun()
            else:
                st.error("Please enter a task title!")
        
        # Display tasks
        st.markdown("---")
        st.markdown("### Your Active Tasks")
        
        if st.session_state.tasks:
            sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x['priority_score'], reverse=True)
            
            for task in sorted_tasks:
                with st.expander(f"{self.emojis[task['priority']]} {self.emojis[task['category']]} {task['title']}"):
                    st.write(f"**Priority:** {task['priority']}")
                    st.write(f"**Due Date:** {task['due_date']}")
                    if task['description']:
                        st.write(f"**Description:** {task['description']}")
                    
                    st.markdown("#### AI Guidance:")
                    st.markdown(f'<div class="fun-card">{task["ai_guidance"]}</div>', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button("Complete", key=f"complete_{task['id']}"):
                            points = {"High": 15, "Medium": 10, "Low": 5}[task['priority']]
                            st.session_state.user_points += points
                            
                            completed_task = task.copy()
                            completed_task['completed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                            st.session_state.completed_tasks.append(completed_task)
                            st.session_state.tasks.remove(task)
                            
                            new_achievements = self.check_achievements()
                            st.success(f"Task completed! +{points} points!")
                            
                            if new_achievements:
                                for achievement in new_achievements:
                                    st.success(f"Achievement unlocked: {achievement}!")
                            
                            st.rerun()
                    
                    with col3:
                        if st.button("Delete", key=f"delete_{task['id']}"):
                            st.session_state.tasks.remove(task)
                            st.warning(f"Task '{task['title']}' deleted.")
                            st.rerun()
        else:
            st.info("No active tasks. Create your first task above!")

    def ai_insights_page(self):
        st.markdown("## AI Insights Hub")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'''
            <div class="fun-card">
                <h3>Today's Motivation</h3>
                <p>{random.choice(self.fun_messages)}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="fun-card">
                <h3>Productivity Tip</h3>
                <p>{random.choice(self.productivity_tips)}</p>
            </div>
            ''', unsafe_allow_html=True)
        
        insights = self.get_productivity_insights(st.session_state.tasks, st.session_state.completed_tasks)
        
        st.markdown("### Task Suggestions")
        suggestions = [
            "Take a 10-minute walk",
            "Organize your workspace",
            "Review your goals",
            "Learn something new",
            "Connect with a friend"
        ]
        
        suggested_task = random.choice(suggestions)
        st.info(f"Suggestion: {suggested_task}")

    def analytics_page(self):
        st.markdown("## Analytics Dashboard")
        
        insights = self.get_productivity_insights(st.session_state.tasks, st.session_state.completed_tasks)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Category Distribution")
            if insights['category_distribution']:
                fig = px.pie(
                    values=list(insights['category_distribution'].values()),
                    names=list(insights['category_distribution'].keys()),
                    color_discrete_sequence=self.chart_colors['category_colors']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available yet.")
        
        with col2:
            st.markdown("### Priority Levels")
            if insights['priority_distribution']:
                fig = px.bar(
                    x=list(insights['priority_distribution'].keys()),
                    y=list(insights['priority_distribution'].values()),
                    color=list(insights['priority_distribution'].keys()),
                    color_discrete_sequence=self.chart_colors['priority_colors']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available yet.")

    def achievements_page(self):
        st.markdown("## Achievement Gallery")
        
        st.markdown("### Progress Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Points", st.session_state.user_points)
        col2.metric("Streak", f"{st.session_state.streak_days} days")
        col3.metric("Achievements", f"{len(st.session_state.achievements)}/{len(self.achievements)}")
        
        st.markdown("### Your Achievements")
        
        cols = st.columns(3)
        for i, achievement in enumerate(self.achievements):
            col_idx = i % 3
            with cols[col_idx]:
                is_earned = achievement["name"] in st.session_state.achievements
                status = "ACHIEVED" if is_earned else "LOCKED"
                bg_color = "metric-success" if is_earned else "metric-info"
                
                st.markdown(f'''
                <div class="metric-card {bg_color}">
                    <div style="font-size: 2.5rem;">{achievement["emoji"]}</div>
                    <h4>{achievement["name"]}</h4>
                    <p>{achievement["desc"]}</p>
                    <div style="margin-top: 1rem;">+{achievement["points"]} points</div>
                    <div style="font-weight: bold; margin-top: 0.5rem;">{status}</div>
                </div>
                ''', unsafe_allow_html=True)

# Create the app instance and run
if __name__ == "__main__":
    app = AIToDoApp()
    app.run()
