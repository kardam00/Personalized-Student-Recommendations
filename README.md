# Personalized-Student-Recommendations

## Project Overview
This project analyzes quiz data, submission responses, and historical performance to provide actionable insights and recommendations. The system fetches data from APIs, processes quiz results, generates performance summaries, and visualizes historical trends.

### Features:
1. Fetches data from APIs (quiz questions, user responses, and historical performance).
2. Processes and evaluates user responses against correct answers.
3. Provides topic-wise performance analysis and recommendations.
4. Visualizes historical performance (score and accuracy trends).

## Setup Instructions

### Prerequisites:
1. Python 3.7 or higher.
2. Libraries: `pandas`, `requests`, `matplotlib`, `seaborn`, `urllib3`.

### Installation:
1. Clone the repository:
   ```bash
   git clone [repository-url](https://github.com/kardam00/Personalized-Student-Recommendations)
   ```
2. Install dependencies:
   ```bash
   pip install pandas requests matplotlib seaborn
   ```

### Running the Project:
1. Update the API URLs in the `main()` function with valid endpoints for:
   - Quiz data
   - Submission data
   - Historical performance data
2. Execute the script:
   ```bash
   python main.py
   ```

3. The script outputs:
   - Performance summaries
   - Historical performance trends (visualized graph)
   - Recommendations for improvement

4. The visualization chart will open automatically.

### Notes:
- Ensure internet connectivity for API calls.
- Suppress SSL warnings if needed (handled in the script).

---

# Output Analysis

## Performance Summary
This section aggregates quiz results by topic and difficulty level:

### Example:
| Topic                            | Difficulty Level | Total Questions | Correct Answers | Total Marks |
|---------------------------------|-----------------|-----------------|-----------------|-------------|
| Structural Organisation In Animals | Unknown Level   | 128             | 8               | -88         |

- **Interpretation**: Out of 128 questions on "Structural Organisation In Animals," only 8 were answered correctly, resulting in a negative total score of -88.

## Historical Performance
Tracks scores and accuracy over multiple quiz submissions:

| Submission Order | Score | Accuracy |
|------------------|-------|----------|
| 1                | 108   | 90 %     |
| 2                |  92   | 100 %    |
| 3                | 116   | 96 %     |
| 4                |  36   | 90 %     |
| 5                |  36   | 31 %     |
| 6                |  40   | 38 %     |
| 7                |  36   | 50 %     |
| 8                |  12   | 30 %     |
| 9                |  76   | 100 %    |
| 10               |  40   | 100 %    |
| 11               | 112   | 93 %     |
| 12               |  64   | 84 %     |
| 13               |  52   | 43 %     |
| 14               |  24   | 66 %     |

- **Key Observations:**
  - Performance fluctuates significantly across attempts.
  - Some submissions exhibit high scores and perfect accuracy (e.g., Submission 2).
  - Declining trends indicate the need for targeted intervention on weaker topics.

## Recommendations
1. **Topic Focus:**
   - Focus on "Structural Organisation In Animals," particularly questions at "Unknown Level" difficulty, to improve performance.
2. **Historical Trends:**
   - Address inconsistencies in recent quizzes where average scores drop below 50%.
   - Leverage improvement opportunities observed in some submissions (e.g., Submission 11).

## Visualization Explanation
The graph illustrates score and accuracy trends across 14 submissions:
- **X-Axis:** Quiz submission order.
- **Y-Axis:** Percentage (Score and Accuracy).
- **Key Insights:**
  - Spikes in performance demonstrate capability but lack consistency.
  - Alignment between score and accuracy indicates that low scores are due to incorrect answers rather than unanswered questions.

---

