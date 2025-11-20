#!/usr/bin/env python3
# grade-generator.py
import csv
from datetime import datetime

def get_valid_input(prompt, input_type, valid_range=None, valid_options=None):
    """Get and validate user input"""
    while True:
        try:
            user_input = input(prompt).strip()
            
            if input_type == "string":
                return user_input
            
            elif input_type == "category":
                if user_input.upper() in ['FA', 'SA']:
                    return user_input.upper()
                else:
                    print("Error: Category must be 'FA' or 'SA'")
            
            elif input_type == "number":
                number = float(user_input)
                if valid_range and (number < valid_range[0] or number > valid_range[1]):
                    print(f"Error: Number must be between {valid_range[0]} and {valid_range[1]}")
                else:
                    return number
            
        except ValueError:
            print("Error: Please enter a valid input")

def calculate_weighted_grade(grade, weight):
    """Calculate weighted grade"""
    return (grade / 100) * weight

def main():
    print("=== Grade Generator Calculator ===")
    print()
    
    assignments = []
    
    # Collect assignment data
    while True:
        print(f"Assignment #{len(assignments) + 1}")
        print("-" * 20)
        
        # Get assignment details
        name = get_valid_input("Assignment Name: ", "string")
        category = get_valid_input("Category (FA/SA): ", "category")
        grade = get_valid_input("Grade (0-100): ", "number", (0, 100))
        weight = get_valid_input("Weight: ", "number", (0, 100))
        
        # Calculate weighted grade
        weighted_grade = calculate_weighted_grade(grade, weight)
        
        # Store assignment data
        assignment = {
            'name': name,
            'category': category,
            'grade': grade,
            'weight': weight,
            'weighted_grade': weighted_grade
        }
        assignments.append(assignment)
        
        # Ask if user wants to add another assignment
        another = input("Add another assignment? (y/n): ").strip().lower()
        if another != 'y':
            break
        print()
    
    # Calculate totals
    total_formative = 0
    total_summative = 0
    total_weight_formative = 0
    total_weight_summative = 0
    
    for assignment in assignments:
        if assignment['category'] == 'FA':
            total_formative += assignment['weighted_grade']
            total_weight_formative += assignment['weight']
        else:  # SA
            total_summative += assignment['weighted_grade']
            total_weight_summative += assignment['weight']
    
    # Final calculations
    total_grade = total_formative + total_summative
    gpa = (total_grade / 100) * 5.0
    
    # Pass/Fail logic
    pass_fa = total_formative >= (total_weight_formative * 0.5)
    pass_sa = total_summative >= (total_weight_summative * 0.5)
    passed = pass_fa and pass_sa
    
    # Console Output
    print("\n" + "=" * 50)
    print("GRADE SUMMARY")
    print("=" * 50)
    
    print("\nAssignments:")
    print("-" * 40)
    for i, assignment in enumerate(assignments, 1):
        print(f"{i}. {assignment['name']} ({assignment['category']}): "
              f"Grade: {assignment['grade']}%, Weight: {assignment['weight']}%")
    
    print("\nCategory Totals:")
    print("-" * 20)
    print(f"Formative (FA): {total_formative:.2f} / {total_weight_formative:.2f}")
    print(f"Summative (SA): {total_summative:.2f} / {total_weight_summative:.2f}")
    
    print("\nFinal Results:")
    print("-" * 20)
    print(f"Total Grade: {total_grade:.2f}%")
    print(f"GPA: {gpa:.2f}")
    print(f"Status: {'PASS' if passed else 'FAIL'}")
    
    if not passed:
        if not pass_fa:
            print("  - Need to improve Formative assignments")
        if not pass_sa:
            print("  - Need to improve Summative assignments")
    
    # CSV Output
    filename = "grades.csv"
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Assignment', 'Category', 'Grade', 'Weight'])
        
        # Write assignment data
        for assignment in assignments:
            writer.writerow([
                assignment['name'],
                assignment['category'],
                assignment['grade'],
                assignment['weight']
            ])
    
    print(f"\nData saved to {filename}")

if __name__ == "__main__":
    main()
