import streamlit as st
import time

# Sample detailed feedback data
feedback = {
    "Effectiveness": {
        "score": 8,
        "points": [
            "Goal achieved (leave approved)",
            "Quick resolution due to good preparation",
            "Could have been more detailed in response about deadlines"
        ]
    },
    "Preparedness": {
        "score": 9,
        "points": [
            "Had coverage plan ready",
            "Team already briefed",
            "Handover document mentioned",
            "Specific backup person identified"
        ]
    },
    "Assertiveness": {
        "score": 7,
        "points": [
            "Direct in stating needs",
            "Could have provided more context about the family emergency (if comfortable)",
            "Brief responses could be expanded for better engagement"
        ]
    },
    "Confidence": {
        "score": 6,
        "points": [
            "Showed certainty in team's ability",
            "Some typing errors suggest possible rushing/anxiety",
            "Could have presented information more structured"
        ]
    },
    "Flexibility": {
        "score": 8,
        "points": [
            "Demonstrated willingness to provide necessary documentation",
            "Open to manager's questions",
            "Ready to fulfill reasonable requests"
        ]
    }
}

# Function to display progress bars and scores for each metric
def display_feedback(feedback):
    st.title("Feedback Analysis")
    for metric, data in feedback.items():
        score = data["score"]

        # Display the metric name and score
        st.markdown(f"**{metric} ({score}/10)**")

        # Display a moving progress bar filling up to the score
        my_bar = st.progress(0)
        for percent_complete in range(int(score * 10)):  # Multiply by 10 to scale the score to 100%
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1)

# Function to generate action items based on feedback scores and points
def generate_action_items(feedback):
    action_items = []
    for key, data in feedback.items():
        score = data["score"]
        points = data["points"]
        if score < 8:
            for point in points:
                action_items.append(f"Consider improving: {point.lower()}")
    return action_items

# Function to generate a summary based on feedback scores
def generate_summary(feedback):
    summary = []
    total_score = sum(data["score"] for data in feedback.values())
    average_score = total_score / len(feedback)
    
    if average_score >= 8:
        summary.append("Overall, you performed excellently, showcasing great preparation and effectiveness.")
    elif 6 <= average_score < 8:
        summary.append("Overall, you did well, but there is room for improvement, especially in areas like communication clarity and confidence.")
    else:
        summary.append("Overall, you need to focus on enhancing your preparation and assertiveness for better outcomes.")
    
    return summary

# Display the feedback summary in Streamlit
st.title("Feedback Summary")
summary = generate_summary(feedback)
for item in summary:
    st.write(item)

# Display detailed feedback with moving progress bars and scores
display_feedback(feedback)

# Display the action items in Streamlit
st.title("Action Items")
action_items = generate_action_items(feedback)
for item in action_items:
    st.write(f"- {item}")
