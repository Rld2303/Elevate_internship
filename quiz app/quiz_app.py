import random
import time
from threading import Timer

quiz_questions = [
    {
        "question": "What is the capital of France?",
        "choices": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
        "correct": "C",
        "explanation": "The capital of France is Paris.",
        "difficulty": "easy"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "choices": ["A. Earth", "B. Jupiter", "C. Mars", "D. Saturn"],
        "correct": "B",
        "explanation": "Jupiter is the largest planet in our solar system.",
        "difficulty": "medium"
    },
    {
        "question": "Who wrote 'To Kill a Mockingbird'?",
        "choices": ["A. Harper Lee", "B. J.K. Rowling", "C. Ernest Hemingway", "D. F. Scott Fitzgerald"],
        "correct": "A",
        "explanation": "Harper Lee wrote 'To Kill a Mockingbird'.",
        "difficulty": "medium"
    },
    {
        "question": "What is the boiling point of water?",
        "choices": ["A. 90°C", "B. 100°C", "C. 110°C", "D. 120°C"],
        "correct": "B",
        "explanation": "The boiling point of water is 100°C.",
        "difficulty": "easy"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "choices": ["A. Vincent van Gogh", "B. Pablo Picasso", "C. Leonardo da Vinci", "D. Claude Monet"],
        "correct": "C",
        "explanation": "The Mona Lisa was painted by Leonardo da Vinci.",
        "difficulty": "hard"
    }
]

def ask_question(question_data, time_limit=10):
    def timeout():
        print("\nTime's up! Moving to the next question.")
    
    print(question_data["question"])
    for choice in question_data["choices"]:
        print(choice)
    
    timer = Timer(time_limit, timeout)
    timer.start()
    
    answer = input("Enter your choice (A, B, C, or D): ").strip().upper()
    
    timer.cancel()
    return answer

def main():
    difficulty = input("Choose difficulty (easy, medium, hard): ").strip().lower()
    filtered_questions = [q for q in quiz_questions if q["difficulty"] == difficulty]

    if not filtered_questions:
        print("No questions available for this difficulty level.")
        return

    random.shuffle(filtered_questions)

    score = 0
    for question_data in filtered_questions:
        while True:
            user_answer = ask_question(question_data)
            if user_answer in ["A", "B", "C", "D"]:
                break
            else:
                print("Invalid choice. Please enter A, B, C, or D.")

        if user_answer == question_data["correct"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is {question_data['correct']}.")
        print(f"Explanation: {question_data['explanation']}")
        print()

    print(f"Your final score is {score} out of {len(filtered_questions)}.")

if __name__ == "__main__":
    main()
