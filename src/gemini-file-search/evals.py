from google import genai
from google.genai import types
import time
import os
import csv
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

store_name = os.getenv('STORE_NAME')

client = genai.Client()

# Read questions and expected answers from CSV file (skipping header)
eval_data = []
with open('evals.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        if row and len(row) >= 2:  # Check if row has both question and answer
            eval_data.append({'question': row[0], 'expected_answer': row[1]})

# Open output CSV file
with open('eval-results.csv', 'w', newline='', encoding='utf-8') as outfile:
    fieldnames = ['question', 'generated_answer', 'expected_answer', 'response_time_seconds', 'score', 'reasoning']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for item in eval_data:
        question = item['question']
        expected_answer = item['expected_answer']
        
        # Generate answer using file search and measure time
        start_time = time.time()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[store_name]
                        )
                    )
                ]
            )
        )
        end_time = time.time()
        response_time = round(end_time - start_time, 2)
        
        generated_answer = response.text
        
        # Score the answer using LLM
        scoring_prompt = f"""You are an expert evaluator. Compare the generated answer with the expected answer and score it on a scale of 1-10 where:
- 1-3: Poor - Incorrect or missing key information
- 4-6: Fair - Partially correct but missing important details
- 7-8: Good - Mostly correct with minor omissions
- 9-10: Excellent - Accurate and comprehensive

Question: {question}

Expected Answer: {expected_answer}

Generated Answer: {generated_answer}

Provide your response in the following format:
Score: [number]
Reasoning: [brief explanation]"""

        scoring_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=scoring_prompt
        )
        
        # Parse the scoring response
        scoring_text = scoring_response.text
        score = None
        reasoning = ""
        
        for line in scoring_text.split('\n'):
            if line.startswith('Score:'):
                score = line.replace('Score:', '').strip()
            elif line.startswith('Reasoning:'):
                reasoning = line.replace('Reasoning:', '').strip()
        
        # Write result to CSV
        writer.writerow({
            'question': question,
            'generated_answer': generated_answer,
            'expected_answer': expected_answer,
            'response_time_seconds': response_time,
            'score': score,
            'reasoning': reasoning
        })
        
        print(f"Q: {question[:100]}...")
        print(f"Response time: {response_time}s")
        print(f"Score: {score}")
        print(f"Reasoning: {reasoning[:100]}...")
        print("-----")

print(f"\nEvaluation complete. Results saved to eval-results.csv")



