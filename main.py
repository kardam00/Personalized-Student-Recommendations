import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fetch Data from APIs
def fetch_data(quiz_url, submission_url, historical_url):
  try:
    quiz_data = requests.get(quiz_url, verify=False).json()
    submission_data = requests.get(submission_url, verify=False).json()
    historical_data = requests.get(historical_url, verify=False).json()
    return quiz_data, submission_data, historical_data
  except Exception as e:
    print("Error fetching data:", e)
    return None, None, None

# Process Current Quiz Data
def process_quiz_data(quiz_data, submission_data):
  # Extract questions and responses
  questions_df = pd.DataFrame(quiz_data['quiz']['questions'])
  response_map = submission_data['response_map']
  submission_df = pd.DataFrame([
    {'question_id': question_id, 'selected_option': selected_option}
    for question_id, selected_option in response_map.items()
  ])
    
  # Merge questions and responses
  questions_df['question_id'] = questions_df['id'].astype(str)
  submission_df['question_id'] = submission_df['question_id'].astype(str)
  merged_df = pd.merge(questions_df, submission_df, on='question_id', how='left')
  merged_df['selected_option'].fillna('Unanswered', inplace=True)
    
  # Add correctness and marks
  correct_marks = float(quiz_data['quiz']['correct_answer_marks'])
  negative_marks = float(quiz_data['quiz']['negative_marks'])
  merged_df['is_correct'] = merged_df.apply(
    lambda row: row['selected_option'] == next(
      (o['id'] for o in row['options'] if o['is_correct']), None
    ) if row['selected_option'] != 'Unanswered' else False,
    axis=1
  )
  merged_df['marks'] = merged_df['is_correct'].apply(
    lambda x: correct_marks if x else -negative_marks if x is False else 0
  )
  merged_df['topic'] = merged_df['topic'].fillna('Unknown Topic').str.strip().str.title()
  merged_df['difficulty_level'] = merged_df['difficulty_level'].fillna('Unknown Level').str.strip().str.title()
    
  return merged_df

# Analyze Performance
def analyze_performance(merged_df):
  performance_summary = merged_df.groupby(['topic', 'difficulty_level']).agg(
    total_questions=('question_id', 'count'),
    correct_answers=('is_correct', 'sum'),
    total_marks=('marks', 'sum')
  ).reset_index()
  return performance_summary

# Process Historical Data
def process_historical_data(historical_data):
  historical_df = pd.DataFrame(historical_data)
  historical_df['score'] = pd.to_numeric(historical_df['score'].astype(str).str.rstrip('%'), errors='coerce')
  historical_df['accuracy'] = pd.to_numeric(historical_df['accuracy'].astype(str).str.rstrip('%'), errors='coerce')
  historical_df['submission_order'] = range(1, len(historical_df) + 1)
  return historical_df

# Generate Recommendations
def generate_recommendations(performance_summary, historical_df):
  recommendations = []
    
  # Weak topics
  weak_topics = performance_summary[
    performance_summary['correct_answers'] < performance_summary['total_questions'] * 0.5
  ]
  for _, row in weak_topics.iterrows():
    recommendations.append(f"Focus on topic '{row['topic']}' at difficulty level '{row['difficulty_level']}'.")
    
  # Strong topics
  strong_topics = performance_summary[
    performance_summary['correct_answers'] > performance_summary['total_questions'] * 0.8
  ]
  for _, row in strong_topics.iterrows():
    recommendations.append(f"Maintain your strength in topic '{row['topic']}' at difficulty level '{row['difficulty_level']}'.")
    
  # Historical trends
  if len(historical_df) > 1:
    recent_scores = historical_df.tail(5)['score']
    if recent_scores.mean() < 50:
      recommendations.append("Consistent improvement needed across recent quizzes.")
    elif recent_scores.is_monotonic_increasing:
      recommendations.append("Great job! Your scores are steadily improving.")
    
  return recommendations

# Visualize Historical Performance
def visualize_historical_performance(historical_df):
  plt.figure(figsize=(10, 6))
  sns.lineplot(
    data=historical_df, x='submission_order', y='score', marker='o', label='Score'
  )
  sns.lineplot(
    data=historical_df, x='submission_order', y='accuracy', marker='o', label='Accuracy'
  )
  plt.title('Historical Performance Trends')
  plt.xlabel('Quiz Submission Order')
  plt.ylabel('Percentage')
  plt.legend()
  plt.tight_layout()
  plt.show()

# Main Function
def main():
  quiz_url = "https://jsonkeeper.com/b/LLQT"
  submission_url = "https://api.jsonserve.com/rJvd7g"
  historical_url = "https://api.jsonserve.com/XgAgFJ"
    
  # Fetch data
  quiz_data, submission_data, historical_data = fetch_data(quiz_url, submission_url, historical_url)
  if not quiz_data or not submission_data or not historical_data:
    return
    
  # Process data
  merged_df = process_quiz_data(quiz_data, submission_data)
  performance_summary = analyze_performance(merged_df)
  historical_df = process_historical_data(historical_data)
    
  # Generate recommendations
  recommendations = generate_recommendations(performance_summary, historical_df)
    
  # Display results
  print("\nPerformance Summary:")
  print(performance_summary)
  print("\nHistorical Performance:")
  print(historical_df[['submission_order', 'score', 'accuracy']])
  print("\nRecommendations:")
  for rec in recommendations:
    print(f"- {rec}")
    
  # Visualize historical performance
  visualize_historical_performance(historical_df)

# Run the script
if __name__ == "__main__":
  main()
