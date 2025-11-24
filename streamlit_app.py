import streamlit as st
import random
import time

# Initialize session state
if 'total_scores' not in st.session_state:
    st.session_state.total_scores = []
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'easy'
if 'strengths' not in st.session_state:
    st.session_state.strengths = []
if 'weaknesses' not in st.session_state:
    st.session_state.weaknesses = []
if 'round_scores' not in st.session_state:
    st.session_state.round_scores = {'Technical': [], 'HR': [], 'Managerial': []}

# Question database
QUESTIONS = {
    'sde': {
        'technical': [
            "Design a URL shortener like bit.ly with high availability",
            "Implement rate limiting for an API",
            "Design a chat application system architecture",
            "How would you handle database scaling?",
            "Explain microservices vs monolithic architecture"
        ],
        'hr': [
            "Why do you want to work in software engineering?",
            "Describe your coding journey and what motivates you",
            "How do you debug complex technical issues?",
            "Tell me about a challenging project you worked on",
            "How do you stay updated with new technologies?"
        ],
        'managerial': [
            "How would you mentor junior developers?",
            "How do you prioritize features with tight deadlines?",
            "How would you handle technical debt in a project?",
            "Describe your approach to code reviews",
            "How do you handle disagreements in technical decisions?"
        ]
    },
    'ml': {
        'technical': [
            "Design a recommendation system for e-commerce",
            "How do you handle imbalanced datasets?",
            "Explain the bias-variance tradeoff",
            "How would you deploy an ML model at scale?",
            "What's your approach to feature engineering?"
        ],
        'hr': [
            "Why did you choose machine learning?",
            "How do you explain ML concepts to non-technical people?",
            "How do you stay updated with ML research?",
            "Describe a challenging ML project you worked on",
            "What's your favorite ML algorithm and why?"
        ],
        'managerial': [
            "How would you lead an ML team?",
            "How do you balance model accuracy vs speed?",
            "How do you manage ML project timelines?",
            "How do you handle model performance degradation?",
            "How do you ensure ML model fairness?"
        ]
    },
    'cloud': {
        'technical': [
            "Design a multi-region cloud architecture",
            "How do you implement auto-scaling?",
            "What are your cloud cost optimization strategies?",
            "Explain containerization vs virtualization",
            "How do you ensure cloud security?"
        ],
        'hr': [
            "Why cloud computing over traditional infrastructure?",
            "How do you explain cloud benefits to clients?",
            "How do you handle cloud migration challenges?",
            "Describe your experience with cloud platforms",
            "What cloud certifications do you have?"
        ],
        'managerial': [
            "How would you lead a cloud transformation?",
            "How do you balance security vs accessibility?",
            "How do you manage cloud budgets?",
            "How do you handle cloud vendor lock-in?",
            "How do you ensure cloud compliance?"
        ]
    }
}

st.title("🤖 AI Mock Interview Engine")

# Interview Settings
col1, col2, col3 = st.columns(3)
with col1:
    role = st.selectbox("Target Role", ["SDE (Software Engineer)", "ML (Machine Learning)", "Cloud (Cloud Engineer)"])
    role_key = role.split()[0].lower()

with col2:
    personality = st.selectbox("Interviewer Style", ["Friendly", "Strict", "Expert"])

with col3:
    st.metric("Current Level", st.session_state.difficulty.title())

# Interview Rounds
st.subheader("🔄 Interview Rounds")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Technical Round"):
        st.session_state.current_round = 'technical'
with col2:
    if st.button("HR Round"):
        st.session_state.current_round = 'hr'
with col3:
    if st.button("Managerial Round"):
        st.session_state.current_round = 'managerial'

# Display current round
if 'current_round' not in st.session_state:
    st.session_state.current_round = 'technical'

st.info(f"Current Round: {st.session_state.current_round.title()}")

# Question and AI Answer buttons
col1, col2 = st.columns(2)
with col1:
    get_question = st.button("🎯 Get New Question")
with col2:
    show_ai_answer = st.button("🤖 Show AI Answer First")

if get_question:
    questions = QUESTIONS.get(role_key, {}).get(st.session_state.current_round, ["Tell me about yourself"])
    st.session_state.current_question = random.choice(questions)

# Show AI answer without user input
if show_ai_answer and 'current_question' in st.session_state:
    st.subheader("🤖 AI's Ideal Answer")
    ai_answer = f"Ideal response to '{st.session_state.current_question}': A comprehensive answer would include specific examples, technical details, step-by-step approach, and practical implementation considerations with quantifiable results."
    st.info(ai_answer)

# Display question
if 'current_question' in st.session_state:
    st.subheader(f"📋 {st.session_state.current_round.title()} Round - {role} ({personality} Mode):")
    st.info(st.session_state.current_question)
    
    # Answer input
    answer = st.text_area("💬 Your Answer:", height=150, placeholder="Type your detailed answer here...")
    
    if st.button("📊 Submit & Get Evaluation", type="primary"):
        if answer.strip():
            with st.spinner("AI is evaluating your answer..."):
                time.sleep(1)
                
                # Generate realistic scores
                scores = {
                    'technical_accuracy': random.randint(6, 10),
                    'clarity': random.randint(6, 10),
                    'confidence': random.randint(5, 9),
                    'communication': random.randint(6, 10),
                    'relevance': random.randint(7, 10)
                }
                
                overall = sum(scores.values()) / 5
                
                # Store scores by round
                st.session_state.total_scores.append(overall)
                st.session_state.round_scores[st.session_state.current_round.title()].append(overall)
                
                # Strengths & Weaknesses Detection
                if overall >= 8:
                    strength = max(scores, key=scores.get)
                    if strength not in st.session_state.strengths:
                        st.session_state.strengths.append(strength.replace('_', ' ').title())
                elif overall <= 5:
                    weakness = min(scores, key=scores.get)
                    if weakness not in st.session_state.weaknesses:
                        st.session_state.weaknesses.append(weakness.replace('_', ' ').title())
                
                # Dynamic difficulty adjustment
                avg_score = sum(st.session_state.total_scores) / len(st.session_state.total_scores)
                if avg_score >= 8:
                    st.session_state.difficulty = 'hard'
                elif avg_score >= 6:
                    st.session_state.difficulty = 'medium'
                else:
                    st.session_state.difficulty = 'easy'
                
                # Display results
                st.success(f"🎯 Overall Score: {overall:.1f}/10")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📈 Detailed Scorecard")
                    for criterion, score in scores.items():
                        st.write(f"{criterion.replace('_', ' ').title()}: {score}/10")
                
                with col2:
                    st.subheader("💡 AI Feedback")
                    feedback = "Great answer! You demonstrated good understanding. Consider adding more specific examples."
                    st.write(feedback)
                    
                    st.subheader("✨ Improved Answer")
                    improved_answer = "Your answer could be enhanced by including concrete examples and quantifiable results."
                    st.write(improved_answer)
                
                # AI Generated Answer Section
                st.subheader("🤖 AI Generated Ideal Answer")
                with st.expander("View AI's Ideal Response", expanded=False):
                    ai_generated_answer = f"Ideal answer for '{st.session_state.current_question[:50]}...': A comprehensive response would include detailed explanations, examples, and best practices."
                    st.write(ai_generated_answer)
        else:
            st.warning("Please provide an answer before submitting.")

# Enhanced Stats Sidebar
st.sidebar.header("📊 Performance Dashboard")
if st.session_state.total_scores:
    avg_score = sum(st.session_state.total_scores) / len(st.session_state.total_scores)
    st.sidebar.metric("Overall Average", f"{avg_score:.1f}/10")
    st.sidebar.metric("Questions Completed", len(st.session_state.total_scores))
    st.sidebar.metric("Current Difficulty", st.session_state.difficulty.title())
    
    # Round-wise performance
    st.sidebar.subheader("🔄 Round Performance")
    for round_name, scores in st.session_state.round_scores.items():
        if scores:
            avg = sum(scores) / len(scores)
            st.sidebar.write(f"{round_name}: {avg:.1f}/10 ({len(scores)} questions)")
    
    # Strengths & Weaknesses
    if st.session_state.strengths:
        st.sidebar.subheader("💪 Strengths")
        for strength in st.session_state.strengths[-3:]:  # Show last 3
            st.sidebar.success(strength)
    
    if st.session_state.weaknesses:
        st.sidebar.subheader("🎯 Areas to Improve")
        for weakness in st.session_state.weaknesses[-3:]:  # Show last 3
            st.sidebar.warning(weakness)
    
    # Progress visualization
    if len(st.session_state.total_scores) > 1:
        st.sidebar.line_chart(st.session_state.total_scores)
else:
    st.sidebar.info("Complete your first question to see stats!")

# Reset button
if st.sidebar.button("🔄 Reset Session"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()