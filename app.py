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

class AIToDoApp:
    def __init__(self):
        self.productivity_tips = [
            "Break large tasks into smaller, manageable chunks",
            "Use the 2-minute rule: if it takes less than 2 minutes, do it now",
            "Time-block your calendar for focused work sessions",
            "Batch similar tasks together to maintain focus",
            "Take regular breaks using the Pomodoro technique",
            "Review and adjust your priorities weekly",
            "Eliminate or delegate low-priority tasks",
            "Set specific deadlines for open-ended tasks"
        ]
        
        self.motivation_quotes = [
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "You don't have to be great to get started, but you have to get started to be great. - Les Brown",
            "Success is the sum of small efforts repeated day in and day out. - Robert Collier"
        ]

    def generate_ai_guidance(self, task_title: str, priority: str, category: str) -> str:
        """Generate AI-based guidance for task completion"""
        guidance_templates = {
            "High": [
                f"🎯 **High Priority Alert**: '{task_title}' requires immediate attention. Consider dedicating your peak energy hours to this task.",
                f"⚡ **Focus Strategy**: For '{task_title}', eliminate distractions and use time-blocking. Set a specific deadline and break it into 25-minute focus sessions.",
                f"🔥 **Urgent Task**: '{task_title}' should be your top priority today. Consider what you can delegate or postpone to focus on this."
            ],
            "Medium": [
                f"📋 **Balanced Approach**: '{task_title}' is important but manageable. Schedule it during your moderately productive hours.",
                f"⏰ **Time Management**: For '{task_title}', set a realistic timeline and consider batching it with similar tasks in your {category.lower()} category.",
                f"📊 **Strategic Planning**: '{task_title}' contributes to your goals. Plan specific steps and allocate adequate time."
            ],
            "Low": [
                f"🌱 **When Time Permits**: '{task_title}' can be done during low-energy periods or as a break from more intensive tasks.",
                f"🔄 **Batch Processing**: Consider grouping '{task_title}' with other {category.lower()} tasks for efficiency.",
                f"📝 **Quick Wins**: '{task_title}' might be a good warm-up task to build momentum for your day."
            ]
        }
        
        category_specific_tips = {
            "Work": "💼 Consider your work environment, deadlines, and team dependencies.",
            "Personal": "🏠 Think about your personal energy levels and home environment.",
            "Health": "💪 Remember that consistency is key for health-related goals.",
            "Learning": "📚 Use active learning techniques and spaced repetition.",
            "Finance": "💰 Consider long-term impact and set measurable milestones.",
            "Other": "🎯 Define clear success criteria and next steps."
        }
        
        base_guidance = random.choice(guidance_templates.get(priority, guidance_templates["Medium"]))
        category_tip = category_specific_tips.get(category, category_specific_tips["Other"])
        
        return f"{base_guidance}\n\n{category_tip}"

    def calculate_priority_score(self, priority: str, days_until_due: int, category: str) -> float:
        """Calculate smart priority score based on multiple factors"""
        priority_weights = {"High": 10, "Medium": 6, "Low": 3}
        category_weights = {"Work": 1.2, "Health": 1.1, "Personal": 1.0, "Learning": 0.9, "Finance": 1.15, "Other": 0.8}
        
        base_score = priority_weights.get(priority, 6)
        category_multiplier = category_weights.get(category, 1.0)
        
        # Urgency factor based on due date
        if days_until_due <= 1:
            urgency_multiplier = 2.0
        elif days_until_due <= 3:
            urgency_multiplier = 1.5
        elif days_until_due <= 7:
            urgency_multiplier = 1.2
        else:
            urgency_multiplier = 1.0
            
        return base_score * category_multiplier * urgency_multiplier

    def get_productivity_insights(self, tasks: List[Dict], completed_tasks: List[Dict]) -> Dict:
        """Generate productivity analytics and insights"""
        total_tasks = len(tasks) + len(completed_tasks)
        completion_rate = (len(completed_tasks) / total_tasks * 100) if total_tasks > 0 else 0
        
        # Category analysis
        all_tasks = tasks + completed_tasks
        category_counts = {}
        priority_counts = {}
        
        for task in all_tasks:
            category = task.get('category', 'Other')
            priority = task.get('priority', 'Medium')
            
            category_counts[category] = category_counts.get(category, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Overdue tasks
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
            page_title="AI-Powered To-Do List",
            page_icon="📋",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        st.title("🤖 AI-Powered To-Do List Manager")
        st.markdown("*Intelligent task management with AI guidance and analytics*")
        
        # Sidebar for navigation
        st.sidebar.title("📋 Navigation")
        page = st.sidebar.selectbox("Choose a page:", 
                                   ["Task Manager", "AI Insights", "Analytics Dashboard"])
        
        if page == "Task Manager":
            self.task_manager_page()
        elif page == "AI Insights":
            self.ai_insights_page()
        else:
            self.analytics_page()

    def task_manager_page(self):
        st.header("📝 Task Management")
        
        # Add new task section
        st.subheader("➕ Add New Task")
        col1, col2 = st.columns(2)
        
        with col1:
            task_title = st.text_input("Task Title", placeholder="Enter your task...")
            category = st.selectbox("Category", 
                                   ["Work", "Personal", "Health", "Learning", "Finance", "Other"])
            
        with col2:
            priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            due_date = st.date_input("Due Date", min_value=datetime.now().date())
        
        task_description = st.text_area("Description (Optional)", 
                                       placeholder="Additional details about the task...")
        
        if st.button("🎯 Add Task with AI Guidance", type="primary"):
            if task_title:
                # Calculate days until due
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
                st.success(f"✅ Task '{task_title}' added successfully with AI guidance!")
                st.rerun()
            else:
                st.error("Please enter a task title!")
        
        # Display current tasks
        st.subheader("📋 Current Tasks")
        
        if st.session_state.tasks:
            # Sort tasks by priority score
            sorted_tasks = sorted(st.session_state.tasks, key=lambda x: x['priority_score'], reverse=True)
            
            for i, task in enumerate(sorted_tasks):
                with st.expander(f"{'🔴' if task['priority'] == 'High' else '🟡' if task['priority'] == 'Medium' else '🟢'} {task['title']} - {task['category']}", 
                                expanded=i < 3):  # Expand top 3 priority tasks
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**Priority:** {task['priority']}")
                        st.write(f"**Due Date:** {task['due_date']}")
                        if task['description']:
                            st.write(f"**Description:** {task['description']}")
                        
                        # AI Guidance
                        st.markdown("### 🤖 AI Guidance")
                        st.info(task['ai_guidance'])
                    
                    with col2:
                        if st.button("✅ Complete", key=f"complete_{task['id']}"):
                            completed_task = task.copy()
                            completed_task['completed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                            st.session_state.completed_tasks.append(completed_task)
                            st.session_state.tasks.remove(task)
                            st.success(f"Task '{task['title']}' completed! 🎉")
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_{task['id']}"):
                            st.session_state.tasks.remove(task)
                            st.warning(f"Task '{task['title']}' deleted.")
                            st.rerun()
        else:
            st.info("No active tasks. Add a new task to get started! 🚀")

    def ai_insights_page(self):
        st.header("🧠 AI Insights & Recommendations")
        
        insights = self.get_productivity_insights(st.session_state.tasks, st.session_state.completed_tasks)
        
        # Daily motivation
        st.subheader("💪 Daily Motivation")
        st.markdown(f"> {random.choice(self.motivation_quotes)}")
        
        # Smart recommendations
        st.subheader("🎯 Smart Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Task Analysis")
            if insights['overdue_count'] > 0:
                st.warning(f"⚠️ You have {insights['overdue_count']} overdue task(s). Consider reviewing your schedule!")
            
            if insights['active_tasks'] > 10:
                st.info("📝 You have many active tasks. Consider using the Eisenhower Matrix to prioritize.")
            elif insights['active_tasks'] == 0:
                st.success("🎉 Great job! No active tasks. Time to plan your next goals!")
            
            completion_rate = insights['completion_rate']
            if completion_rate >= 80:
                st.success(f"🌟 Excellent completion rate: {completion_rate:.1f}%!")
            elif completion_rate >= 60:
                st.info(f"👍 Good completion rate: {completion_rate:.1f}%. Keep it up!")
            else:
                st.warning(f"📈 Completion rate: {completion_rate:.1f}%. Consider breaking tasks into smaller chunks.")
        
        with col2:
            st.markdown("### 🎯 Productivity Tips")
            tip = random.choice(self.productivity_tips)
            st.info(f"💡 **Today's Tip:** {tip}")
            
            # Category insights
            if insights['category_distribution']:
                most_common_category = max(insights['category_distribution'], key=insights['category_distribution'].get)
                st.write(f"📊 **Most Active Category:** {most_common_category}")
        
        # AI Task Suggestions
        st.subheader("🤖 AI Task Suggestions")
        
        suggestion_categories = [
            ("Health & Wellness", ["Take a 10-minute walk", "Drink 8 glasses of water today", "Practice 5 minutes of meditation"]),
            ("Professional Growth", ["Update your LinkedIn profile", "Read one industry article", "Network with one colleague"]),
            ("Personal Development", ["Learn something new for 15 minutes", "Practice a hobby", "Call a friend or family member"]),
            ("Organization", ["Declutter your workspace", "Review your goals", "Plan tomorrow's priorities"])
        ]
        
        selected_category = st.selectbox("Choose suggestion category:", [cat[0] for cat in suggestion_categories])
        
        for cat_name, suggestions in suggestion_categories:
            if cat_name == selected_category:
                suggested_task = random.choice(suggestions)
                st.success(f"💡 **Suggested Task:** {suggested_task}")
                
                if st.button("➕ Add Suggested Task"):
                    new_task = {
                        "id": len(st.session_state.tasks) + len(st.session_state.completed_tasks) + 1,
                        "title": suggested_task,
                        "description": "AI-suggested task for personal growth",
                        "category": "Personal",
                        "priority": "Medium",
                        "due_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                        "created_date": datetime.now().strftime('%Y-%m-%d %H:%M'),
                        "priority_score": 6.0,
                        "ai_guidance": self.generate_ai_guidance(suggested_task, "Medium", "Personal")
                    }
                    st.session_state.tasks.append(new_task)
                    st.success("✅ Suggested task added to your list!")
                    st.rerun()

    def analytics_page(self):
        st.header("📊 Analytics Dashboard")
        
        insights = self.get_productivity_insights(st.session_state.tasks, st.session_state.completed_tasks)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Tasks", insights['total_tasks'])
        
        with col2:
            st.metric("Completion Rate", f"{insights['completion_rate']:.1f}%")
        
        with col3:
            st.metric("Active Tasks", insights['active_tasks'])
        
        with col4:
            st.metric("Overdue Tasks", insights['overdue_count'])
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Tasks by Category")
            if insights['category_distribution']:
                fig_category = px.pie(
                    values=list(insights['category_distribution'].values()),
                    names=list(insights['category_distribution'].keys()),
                    title="Task Distribution by Category"
                )
                st.plotly_chart(fig_category, use_container_width=True)
            else:
                st.info("No task data available for category analysis.")
        
        with col2:
            st.subheader("⚡ Tasks by Priority")
            if insights['priority_distribution']:
                colors = {'High': '#FF6B6B', 'Medium': '#FFE66D', 'Low': '#4ECDC4'}
                fig_priority = px.bar(
                    x=list(insights['priority_distribution'].keys()),
                    y=list(insights['priority_distribution'].values()),
                    title="Task Distribution by Priority",
                    color=list(insights['priority_distribution'].keys()),
                    color_discrete_map=colors
                )
                st.plotly_chart(fig_priority, use_container_width=True)
            else:
                st.info("No task data available for priority analysis.")
        
        # Productivity timeline (mock data for demonstration)
        st.subheader("📈 Productivity Timeline")
        
        # Generate sample productivity data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
        productivity_data = pd.DataFrame({
            'Date': dates,
            'Tasks_Completed': [random.randint(0, 5) for _ in dates],
            'Tasks_Added': [random.randint(0, 3) for _ in dates]
        })
        
        fig_timeline = go.Figure()
        fig_timeline.add_trace(go.Scatter(
            x=productivity_data['Date'],
            y=productivity_data['Tasks_Completed'],
            mode='lines+markers',
            name='Tasks Completed',
            line=dict(color='green')
        ))
        fig_timeline.add_trace(go.Scatter(
            x=productivity_data['Date'],
            y=productivity_data['Tasks_Added'],
            mode='lines+markers',
            name='Tasks Added',
            line=dict(color='blue')
        ))
        
        fig_timeline.update_layout(
            title='30-Day Productivity Overview',
            xaxis_title='Date',
            yaxis_title='Number of Tasks',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Export options
        st.subheader("💾 Export Data")
        
        if st.button("📥 Export Tasks to CSV"):
            all_tasks_data = st.session_state.tasks + st.session_state.completed_tasks
            if all_tasks_data:
                df = pd.DataFrame(all_tasks_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"tasks_export_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No tasks to export.")

# Run the app
if __name__ == "__main__":
    app = AIToDoApp()
    app.run()
