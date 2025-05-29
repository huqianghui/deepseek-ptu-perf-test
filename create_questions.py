#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random

# Categories for question generation
categories = [
    "Technology", "Science", "Health", "Business", "Education", 
    "Environment", "Arts", "Programming", "Data Science", "Cloud Computing"
]

# Topics for each category
topics = {
    "Technology": ["blockchain", "IoT", "5G", "quantum computing", "virtual reality"],
    "Science": ["gene editing", "space exploration", "quantum physics", "climate science"],
    "Health": ["telemedicine", "precision medicine", "mental health", "genomics"],
    "Business": ["digital marketing", "remote work", "business analytics", "e-commerce"],
    "Education": ["online learning", "education technology", "personalized learning"],
    "Environment": ["climate change", "renewable energy", "circular economy"],
    "Arts": ["digital art", "film production", "design thinking", "creative writing"],
    "Programming": ["functional programming", "microservices", "API design", "DevOps"],
    "Data Science": ["machine learning", "natural language processing", "deep learning"],
    "Cloud Computing": ["serverless", "multi-cloud", "cloud security", "edge computing"]
}

# Question templates
templates = [
    "What is {}?",
    "How does {} work?",
    "Why is {} important?",
    "Explain the concept of {}.",
    "Describe the benefits of {}.",
    "What are the challenges of implementing {}?",
    "How has {} evolved over time?",
    "Compare {} and {} approaches.",
    "What are the best practices for {}?",
    "How would you implement {} in a real-world scenario?",
    "What's the relationship between {} and {}?",
    "How does {} affect business outcomes?",
    "Explain how {} can be optimized.",
    "What are the security implications of {}?",
    "How would you measure success in {}?",
    "What tools are commonly used for {}?",
    "Describe a use case for {} in {}.",
    "What are the ethical considerations around {}?",
    "How does {} integrate with existing systems?",
    "What are the future trends in {}?"
]

# Create 1000 unique questions
questions = []

# First, add the existing default questions from main.py
default_questions = [
    "What are the main attractions in Paris?",
    "Explain the concept of machine learning in simple terms.",
    "What are the benefits of cloud computing?",
    "How does photosynthesis work?",
    "What are the key principles of effective communication?",
    "Describe the process of software development lifecycle.",
    "What are the advantages of renewable energy?",
    "How do neural networks function?",
    "What are the main components of a computer system?",
    "Explain the importance of data security.",
    "What are the different types of databases?",
    "How does artificial intelligence impact society?",
    "What are the principles of good user interface design?",
    "Describe the concept of microservices architecture.",
    "What are the key factors in project management?",
    "How does encryption protect data?",
    "What are the benefits of agile methodology?",
    "Explain the role of APIs in modern software development.",
    "What are the challenges of distributed systems?",
    "How does version control help in software development?"
]

questions.extend(default_questions)

# Then generate additional unique questions
while len(questions) < 1000:
    category = random.choice(categories)
    template = random.choice(templates)
    
    # Select topics for placeholders
    if "{}" in template:
        placeholders = template.count("{}")
        if placeholders == 1:
            topic = random.choice(topics[category])
            question = template.format(topic)
        else:
            # For comparing two topics
            topic1 = random.choice(topics[category])
            # Ensure topic2 is different from topic1
            available = [t for t in topics[category] if t != topic1]
            if available:
                topic2 = random.choice(available)
            else:
                # If no other topic available in same category, pick from another category
                other_category = random.choice([c for c in categories if c != category])
                topic2 = random.choice(topics[other_category])
            question = template.format(topic1, topic2)
    else:
        # No placeholders
        question = template
    
    # Add if unique
    if question not in questions:
        questions.append(question)

# Generate some specific technical and non-technical questions
specific_questions = [
    "How would you design a scalable web architecture?",
    "Explain the difference between REST and GraphQL APIs.",
    "What are the pros and cons of microservices vs. monolithic architecture?",
    "How does blockchain ensure transaction security?",
    "Explain the concept of containers and containerization.",
    "What are the key components of a CI/CD pipeline?",
    "How would you handle database scaling for millions of users?",
    "What strategies would you use to optimize website performance?",
    "Explain the concept of eventual consistency in distributed systems.",
    "What are the main advantages of using Kubernetes?",
    "How would you implement authentication and authorization in a web app?",
    "What is the difference between supervised and unsupervised learning?",
    "How do recommendation engines work?",
    "Explain the concept of transfer learning in AI.",
    "How would you detect and prevent SQL injection attacks?",
    "What are design patterns and why are they important?",
    "Explain the principles of responsive web design.",
    "What is the importance of code reviews?",
    "How would you approach refactoring a legacy codebase?",
    "What are the key principles of DevOps culture?"
]

# Add specific questions, ensuring we don't exceed 1000 total
for question in specific_questions:
    if question not in questions and len(questions) < 1000:
        questions.append(question)

# Ensure we have exactly 1000 questions
while len(questions) > 1000:
    questions.pop()

# Shuffle the questions for randomness
random.shuffle(questions)

# Save to JSON file
with open('test_questions_1000.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Generated {len(questions)} unique test questions and saved to test_questions_1000.json")

# Print some sample questions
print("\nSample questions:")
for i, question in enumerate(random.sample(questions, min(10, len(questions)))):
    print(f"{i+1}. {question}")
