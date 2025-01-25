import streamlit as st
import requests
from datetime import datetime

# Set page configuration and styling
st.set_page_config(
    page_title="Product Feedback Hub",
    page_icon="📊",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
    <style>
            
    .st-at {
            background-color: #000000;
            }
    /* uOttawa Colors */
    :root {
        --uottawa-garnet: #8f001a;
        --uottawa-grey: #2d2d2d;
        --uottawa-light-grey: #f8f9fa;
        --uottawa-white: #ffffff;
        --uottawa-black: #000000;
        --uottawa-link: #0066cc;
        --uottawa-success: #28a745;
        --uottawa-error: #dc3545;
    }

    /* Main Container */
    .main {
        padding: 2rem;
       font-family: "Work Sans", sans-serif;
        color: var(--uottawa-grey);
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Header Styling */
    .feedback-header {
        color: var(--uottawa-garnet);
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5em;
        line-height: 1.2;
    }

    /* Buttons */
    .stButton button {
        background-color: var(--uottawa-garnet);
        color: var(--uottawa-white);
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 4px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: background-color 0.3s ease;
        position: relative;
        bottom: -20px;
        border-radius: 25px / 50%;
    }

    .stButton button:hover {
        background-color: #6b0013;
    }

    .stButton button:focus {
        outline: 3px solid #d4001f;
        outline-offset: 2px;
    }

    /* Form Controls */
    .stTextArea textarea,
    .stSelectbox select,
    .stTextInput input {
        border: 2px solid #e9ecef;
        border-radius: 4px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }

    .stTextArea textarea:focus,
    .stSelectbox select:focus,
    .stTextInput input:focus {
        border-color: var(--uottawa-garnet);
        outline: none;
        box-shadow: 0 0 0 3px rgba(143, 0, 26, 0.1);
    }

    /* Question Text */
    .question-text {
        font-size: 1.25rem;
        color: var(--uottawa-grey);
        margin-bottom: 1.5em;
        font-weight: 500;
        line-height: 1.4;
    }

    /* Progress Bar */
            
    .stProgress > div > div > div {
        background-color: var(--uottawa-garnet);
    }

    .progress-bar {
        padding: 1em 0;
        margin-bottom: 2em;
        color: var(--uottawa-grey);
    }

    /* Summary Box */
    .summary-box {
        background-color: var(--uottawa-light-grey);
        padding: 2em;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 2em 0;
    }

    /* Messages */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        padding: 1em;
        border-radius: 4px;
        text-align: center;
        margin: 1em 0;
    }

    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
        padding: 1em;
        border-radius: 4px;
        text-align: center;
        margin: 1em 0;
    }

    /* Slider */
    .stSlider div[data-baseweb="slider"] {
        margin-top: 2em;
    }

    .stSlider div[data-baseweb="slider"] div[role="slider"] {
        background-color: var(--uottawa-garnet);
    }

    /* Labels */
    label {
        font-weight: 500;
        color: var(--uottawa-grey);
        margin-bottom: 0.5em;
    }

    /* Links */
    a {
        color: var(--uottawa-link);
        text-decoration: none;
        transition: color 0.3s ease;
    }

    a:hover {
        color: #004999;
        text-decoration: underline;
    }

    /* Section Headers */
    h3 {
        color: var(--uottawa-garnet);
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1.5em 0 1em 0;
    }

    /* Form Groups */
    .form-group {
        margin-bottom: 2em;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .feedback-header {
            font-size: 2rem;
        }
        
        .question-text {
            font-size: 1.1rem;
        }
        
        .summary-box {
            padding: 1.5em;
        }
    }

    /* Update header styling to use h1 */
    h1.feedback-header {
        color: var(--uottawa-garnet);
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5em;
        line-height: 1.2;
        font-family: "Work Sans", sans-serif;
    }

    /* Responsive h1 */
    @media (max-width: 768px) {
        h1.feedback-header {
            font-size: 2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

def init_session_state():
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'current_flow' not in st.session_state:
        st.session_state.current_flow = []

def next_step():
    st.session_state.step += 1

def reset_chat():
    st.session_state.step = 0
    st.session_state.responses = {}
    st.session_state.current_flow = []

def get_question_flow(feedback_type):
    # Base questions that appear first for all types
    base_questions = [
        {
            "question": "What type of feedback would you like to provide?",
            "type": "selectbox",
            "key": "feedback_type",
            "options": ["Satisfaction", "Feature", "Bug", "Team Feedback", "Process Feedback", "General"]
        },
        {
            "question": "Which product/service are you providing feedback about?",
            "type": "text_input",
            "key": "product_name"
        },
        {
            "question": "What is your role in relation to this product?",
            "type": "selectbox",
            "key": "user_role",
            "options": ["End User", "Developer", "Product Manager", "Stakeholder", "Other"]
        }
    ]
    
    type_specific_questions = {
        "Satisfaction": [
            {
                "question": "How satisfied are you with the product?",
                "type": "slider",
                "key": "satisfaction_score",
                "min_value": 1,
                "max_value": 5
            },
            {
                "question": "What do you like most about the product?",
                "type": "text_area",
                "key": "positive_feedback"
            },
            {
                "question": "What are your main pain points?",
                "type": "text_area",
                "key": "pain_points"
            },
            {
                "question": "Would you recommend this product to others?",
                "type": "selectbox",
                "key": "nps",
                "options": ["Definitely", "Probably", "Not Sure", "Probably Not", "Definitely Not"]
            }
        ],
        "Feature": [
            {
                "question": "What new feature would you like to suggest?",
                "type": "text_area",
                "key": "feature_description"
            },
            {
                "question": "What problem would this feature solve?",
                "type": "text_area",
                "key": "problem_solution"
            },
            {
                "question": "How often would you use this feature?",
                "type": "selectbox",
                "key": "usage_frequency",
                "options": ["Multiple times daily", "Daily", "Weekly", "Monthly", "Occasionally"]
            },
            {
                "question": "What is the business impact of this feature?",
                "type": "selectbox",
                "key": "business_impact",
                "options": ["Revenue Increase", "Cost Reduction", "User Satisfaction", "Efficiency Improvement", "Competitive Advantage", "Other"]
            },
            {
                "question": "How urgent is this feature request?",
                "type": "selectbox",
                "key": "urgency",
                "options": ["Critical - Blocking Work", "High - Major Impact", "Medium - Significant Value", "Low - Nice to Have"]
            }
        ],
        "Bug": [
            {
                "question": "What is the severity of this issue?",
                "type": "selectbox",
                "key": "severity",
                "options": ["Critical - System Unusable", "High - Major Feature Broken", "Medium - Feature Partially Working", "Low - Minor Issue"]
            },
            {
                "question": "Please describe the issue:",
                "type": "text_area",
                "key": "bug_description"
            },
            {
                "question": "What steps can reproduce this issue?",
                "type": "text_area",
                "key": "reproduction_steps"
            },
            {
                "question": "What is the impact on your work?",
                "type": "text_area",
                "key": "impact_description"
            },
            {
                "question": "How often does this occur?",
                "type": "selectbox",
                "key": "frequency",
                "options": ["Every time", "Frequently", "Sometimes", "Rarely", "First time"]
            }
        ],
        "General": [
            {
                "question": "Which aspect would you like to discuss?",
                "type": "selectbox",
                "key": "feedback_area",
                "options": ["User Experience", "Performance", "Documentation", "Support", "Pricing", "Other"]
            },
            {
                "question": "Please provide your feedback:",
                "type": "text_area",
                "key": "general_feedback"
            },
            {
                "question": "How could we improve your experience?",
                "type": "text_area",
                "key": "improvement_suggestions"
            },
            {
                "question": "Would you be interested in discussing this further?",
                "type": "selectbox",
                "key": "follow_up",
                "options": ["Yes", "Maybe", "No"]
            }
        ],
        "Team Feedback": [
            {
                "question": "Which team are you providing feedback about?",
                "type": "selectbox",
                "key": "team_type",
                "options": ["Development Team", "Product Team", "Design Team", "QA Team", "Cross-functional Team"]
            },
            {
                "question": "How would you rate the team's technical expertise?",
                "type": "slider",
                "key": "technical_expertise",
                "min_value": 1,
                "max_value": 5
            },
            {
                "question": "How would you rate the team's communication?",
                "type": "slider",
                "key": "communication_rating",
                "min_value": 1,
                "max_value": 5
            },
            {
                "question": "How well does the team meet deadlines?",
                "type": "slider",
                "key": "deadline_adherence",
                "min_value": 1,
                "max_value": 5
            },
            {
                "question": "What are the team's strongest points?",
                "type": "text_area",
                "key": "team_strengths"
            },
            {
                "question": "What areas could the team improve?",
                "type": "text_area",
                "key": "team_improvements"
            },
            {
                "question": "How well does the team handle feedback and criticism?",
                "type": "selectbox",
                "key": "feedback_handling",
                "options": ["Very Well", "Well", "Neutral", "Needs Improvement", "Poor"]
            },
            {
                "question": "How would you rate the team's documentation practices?",
                "type": "selectbox",
                "key": "documentation_quality",
                "options": ["Excellent", "Good", "Adequate", "Needs Improvement", "Poor"]
            }
        ],
        "Process Feedback": [
            {
                "question": "Which process area are you providing feedback about?",
                "type": "selectbox",
                "key": "process_area",
                "options": ["Sprint Planning", "Product Roadmap", "Release Process", "Development Workflow", "Code Review", "Testing Process", "Other"]
            },
            {
                "question": "How efficient is the current process?",
                "type": "slider",
                "key": "process_efficiency",
                "min_value": 1,
                "max_value": 5
            },
            {
                "question": "What are the main bottlenecks in the current process?",
                "type": "text_area",
                "key": "process_bottlenecks"
            },
            {
                "question": "How well are requirements communicated?",
                "type": "selectbox",
                "key": "requirements_clarity",
                "options": ["Very Clear", "Clear", "Somewhat Clear", "Unclear", "Very Unclear"]
            },
            {
                "question": "How would you rate the decision-making process?",
                "type": "selectbox",
                "key": "decision_making",
                "options": ["Very Efficient", "Efficient", "Neutral", "Inefficient", "Very Inefficient"]
            },
            {
                "question": "How well are project priorities communicated?",
                "type": "selectbox",
                "key": "priority_communication",
                "options": ["Excellent", "Good", "Fair", "Poor", "Very Poor"]
            },
            {
                "question": "What process improvements would you suggest?",
                "type": "text_area",
                "key": "process_improvements"
            },
            {
                "question": "How well does the current process handle:",
                "type": "selectbox",
                "key": "process_handling",
                "options": ["Change Requests", "Resource Allocation", "Risk Management", "Quality Assurance", "Stakeholder Communication"]
            },
            {
                "question": "What metrics would you suggest tracking to improve the process?",
                "type": "text_area",
                "key": "suggested_metrics"
            }
        ]
    }
    
    return base_questions + type_specific_questions.get(feedback_type, [])

def chat_interface():
    # Header
    st.markdown("""
        <h1 class="feedback-header">Product Feedback Hub</h1>
        """, unsafe_allow_html=True)
    
    # Subtitle
    st.markdown("""
        <p style='text-align: center; color: #666; margin-bottom: 2em;'>
            Help us improve our product by sharing your valuable feedback
        </p>
    """, unsafe_allow_html=True)
    
    # Initialize flow if it's the first question
    if st.session_state.step == 0:
        st.session_state.current_flow = get_question_flow("general")
    
    # Progress bar
    if st.session_state.step < len(st.session_state.current_flow):
        progress = st.session_state.step / len(st.session_state.current_flow)
        st.markdown('<div class="progress-bar">', unsafe_allow_html=True)
        st.progress(progress)
        st.markdown(f'Question {st.session_state.step + 1} of {len(st.session_state.current_flow)}')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Get current step
    if st.session_state.step < len(st.session_state.current_flow):
        current_step = st.session_state.current_flow[st.session_state.step]
        
        # Display question with styling
        st.markdown(f'<p class="question-text">{current_step["question"]}</p>', unsafe_allow_html=True)
        
        # Create columns for better layout
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Display appropriate input type
            if current_step["type"] == "selectbox":
                response = st.selectbox(
                    "Select an option:",
                    current_step["options"],
                    key=f"input_{current_step['key']}"
                )
            elif current_step["type"] == "slider":
                response = st.slider(
                    "Select a value:",
                    current_step["min_value"],
                    current_step["max_value"],
                    key=f"input_{current_step['key']}"
                )
            elif current_step["type"] == "text_area":
                response = st.text_area(
                    "Your response:",
                    key=f"input_{current_step['key']}",
                    height=150
                )
            elif current_step["type"] == "text_input":
                response = st.text_input(
                    "Your response:",
                    key=f"input_{current_step['key']}"
                )
        
        with col2:
            # Next button
            if st.button("Next →"):
                st.session_state.responses[current_step["key"]] = response
                
                # Update flow if feedback type is selected
                if current_step["key"] == "feedback_type":
                    st.session_state.current_flow = get_question_flow(response)
                
                next_step()
                st.rerun()
            
    else:
        # Show summary in a nice box
        st.markdown('<div class="summary-box">', unsafe_allow_html=True)
        st.markdown("### Summary of Your Feedback")
        for key, value in st.session_state.responses.items():
            st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Create columns for buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("← Start Over"):
                reset_chat()
                st.rerun()
        
        with col2:
            if st.button("Submit Feedback →"):
                submit_feedback()

def submit_feedback():
    try:
        response = requests.post(
            "http://localhost:8000/feedback",
            json={
                "text": str(st.session_state.responses),  # Convert full responses to string
                "feedback_type": st.session_state.responses.get('feedback_type', 'general'),
                "responses": st.session_state.responses,  # Send full response data
                "created_at": datetime.now().isoformat()
            }
        )
        
        if response.status_code == 200:
            st.markdown(
                '<div class="success-message">Thank you for your valuable feedback!</div>',
                unsafe_allow_html=True
            )
            if st.button("Provide More Feedback"):
                reset_chat()
        else:
            st.markdown(
                f'<div class="error-message">Error submitting feedback. Status code: {response.status_code}</div>',
                unsafe_allow_html=True
            )
            st.error(f"Response content: {response.text}")  # Debug info
            
    except Exception as e:
        st.markdown(
            f'<div class="error-message">Error: {str(e)}</div>',
            unsafe_allow_html=True
        )
        st.error(f"Exception details: {str(e)}")  # Debug info

def main():
    init_session_state()
    chat_interface()

if __name__ == "__main__":
    main() 