#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random

# Define categories for diverse question generation
categories = [
    "Technology",
    "Science",
    "Health",
    "Business",
    "Education",
    "Environment",
    "Arts",
    "History",
    "Philosophy",
    "Society",
    "Programming",
    "Data Science",
    "Cloud Computing",
    "AI Ethics",
    "Cybersecurity"
]

# Templates for generating diverse question types
question_templates = {
    "what": [
        "What is {}?",
        "What are the key components of {}?",
        "What are the benefits of {}?",
        "What are the challenges facing {}?",
        "What technologies are used in {}?",
        "What principles underlie {}?",
        "What are the most important developments in {} recently?",
        "What are the differences between {} and {}?",
        "What strategies work best for {}?",
        "What are the implications of {} for society?"
    ],
    "how": [
        "How does {} work?",
        "How can {} be implemented effectively?",
        "How has {} evolved over time?",
        "How can businesses leverage {}?",
        "How do experts measure success in {}?",
        "How will {} change in the next decade?",
        "How can beginners get started with {}?",
        "How does {} compare to {}?",
        "How do you troubleshoot issues with {}?",
        "How can {} improve efficiency in organizations?"
    ],
    "why": [
        "Why is {} important?",
        "Why do organizations invest in {}?",
        "Why has {} become more relevant recently?",
        "Why should students learn about {}?",
        "Why do some approaches to {} fail while others succeed?",
        "Why is there debate surrounding {}?",
        "Why might {} be considered controversial?",
        "Why is {} essential for modern development?"
    ],
    "explain": [
        "Explain the concept of {} in simple terms.",
        "Explain how {} relates to {}.",
        "Explain the process of implementing {}.",
        "Explain the history and evolution of {}.",
        "Explain the key challenges in {}.",
        "Explain the benefits of adopting {}.",
        "Explain the role of {} in modern society.",
        "Explain how to get started with {}.",
        "Explain the underlying principles of {}."
    ],
    "describe": [
        "Describe the architecture of {}.",
        "Describe the best practices for {}.",
        "Describe the workflow of {}.",
        "Describe the main components of {}.",
        "Describe how {} and {} interact.",
        "Describe the future trends in {}.",
        "Describe the impact of {} on {}.",
        "Describe the key metrics for measuring {} success.",
        "Describe how to implement {} in a real-world scenario."
    ],
    "compare": [
        "Compare and contrast {} and {}.",
        "Compare the benefits of {} versus {}.",
        "Compare different approaches to {}.",
        "Compare how {} is implemented across different industries.",
        "Compare the evolution of {} over the past decade.",
        "Compare the key features of {} and {}.",
        "Compare traditional and modern approaches to {}."
    ]
}

# Specific topics related to each category for more concrete questions
topics = {
    "Technology": [
        "blockchain technology", "internet of things", "5G networks", "edge computing", 
        "quantum computing", "virtual reality", "augmented reality", "digital transformation",
        "robotics", "autonomous vehicles", "smart homes", "wearable technology",
        "3D printing", "gesture recognition", "voice recognition", "biometric authentication"
    ],
    "Science": [
        "gene editing", "nanotechnology", "renewable energy", "space exploration", 
        "quantum physics", "climate science", "neuroscience", "synthetic biology",
        "astronomy", "particle physics", "materials science", "ecology",
        "evolutionary biology", "geology", "oceanography", "meteorology"
    ],
    "Health": [
        "telemedicine", "precision medicine", "mental health", "nutrition science", 
        "preventive healthcare", "wearable health devices", "genomics", "bioinformatics",
        "pandemic response", "vaccine development", "chronic disease management", "exercise science",
        "sleep science", "aging research", "public health policies", "healthcare AI"
    ],
    "Business": [
        "digital marketing", "remote work", "supply chain management", "business analytics", 
        "sustainable business practices", "entrepreneurship", "venture capital", "risk management",
        "organizational behavior", "customer experience", "business strategy", "market research",
        "e-commerce", "product development", "corporate social responsibility", "international trade"
    ],
    "Education": [
        "online learning", "education technology", "personalized learning", "STEM education", 
        "adult education", "early childhood education", "gamification in learning", "assessment methods",
        "educational psychology", "peer learning", "project-based learning", "lifelong learning",
        "digital literacy", "learning disabilities", "educational equity", "teacher development"
    ],
    "Environment": [
        "climate change", "sustainable development", "circular economy", "biodiversity conservation", 
        "water management", "renewable energy", "green building", "carbon capture",
        "waste reduction", "environmental policy", "ocean conservation", "deforestation",
        "sustainable agriculture", "air quality", "environmental justice", "wildlife protection"
    ],
    "Arts": [
        "digital art", "contemporary literature", "film production", "music composition", 
        "performing arts", "art history", "architecture", "design thinking",
        "visual storytelling", "animation techniques", "photography", "creative writing",
        "art therapy", "cultural heritage preservation", "fashion design", "public art"
    ],
    "History": [
        "ancient civilizations", "world wars", "industrial revolution", "cold war", 
        "civil rights movements", "colonial history", "cultural revolutions", "economic history",
        "technological innovations throughout history", "archaeological discoveries", 
        "historical figures", "medieval period", "renaissance", "historical methods"
    ],
    "Philosophy": [
        "ethics", "existentialism", "philosophy of mind", "political philosophy", 
        "epistemology", "metaphysics", "aesthetics", "logic",
        "philosophy of science", "philosophy of language", "eastern philosophy", "moral philosophy",
        "pragmatism", "philosophical anthropology", "philosophy of technology", "phenomenology"
    ],
    "Society": [
        "social media impact", "wealth inequality", "urbanization", "cultural diversity", 
        "demographic changes", "work-life balance", "privacy in digital age", "future of work",
        "digital inclusion", "social entrepreneurship", "intergenerational relations",
        "community building", "digital citizenship", "social cohesion", "civic engagement"
    ],
    "Programming": [
        "functional programming", "object-oriented programming", "reactive programming", 
        "serverless architecture", "progressive web apps", "microservices", "API design",
        "containerization", "distributed systems", "version control", "test-driven development",
        "continuous integration", "refactoring", "code quality", "pair programming"
    ],
    "Data Science": [
        "machine learning", "big data analytics", "natural language processing", "computer vision", 
        "predictive modeling", "data visualization", "statistical analysis", "deep learning",
        "reinforcement learning", "time series analysis", "recommendation systems", "clustering algorithms",
        "anomaly detection", "feature engineering", "data ethics", "explainable AI"
    ],
    "Cloud Computing": [
        "infrastructure as a service", "platform as a service", "software as a service", 
        "hybrid cloud", "multi-cloud strategies", "cloud security", "serverless computing",
        "cloud migration", "cloud cost optimization", "edge computing", "cloud AI services",
        "cloud storage solutions", "container orchestration", "virtual private clouds"
    ],
    "AI Ethics": [
        "algorithmic bias", "AI transparency", "responsible AI", "privacy concerns in AI", 
        "AI governance", "AI explainability", "automated decision-making ethics",
        "AI and employment", "AI regulation", "fairness in machine learning",
        "AI accountability", "human-AI collaboration", "AI safety", "AI and social good"
    ],
    "Cybersecurity": [
        "threat intelligence", "penetration testing", "security by design", "encryption technologies", 
        "network security", "endpoint security", "identity management", "security frameworks",
        "zero trust security", "vulnerability management", "security awareness training",
        "incident response", "cloud security", "IoT security", "supply chain security"
    ]
}

# Additional specific questions that are common in technical interviews or academic settings
specific_questions = [
    "How would you design a system that can handle millions of concurrent users?",
    "Explain the concept of eventual consistency in distributed systems.",
    "How do you ensure security in microservices architecture?",
    "Describe the principles of DevOps and how they improve software delivery.",
    "What strategies would you use to optimize a slow-performing database query?",
    "How does blockchain technology ensure transaction security?",
    "What are the tradeoffs between different NoSQL database types?",
    "How would you approach debugging a complex production issue?",
    "Explain how HTTP/3 improves upon HTTP/2.",
    "What considerations are important when designing a RESTful API?",
    "How does containerization improve application deployment?",
    "What are the challenges of implementing machine learning in production?",
    "How would you design a recommendation engine for an e-commerce website?",
    "Explain the concept of technical debt and strategies to manage it.",
    "How does TLS/SSL encryption work to secure internet communications?",
    "What are design patterns and when should they be applied?",
    "How would you approach scaling a web application horizontally?",
    "What are the benefits and challenges of serverless architectures?",
    "Explain the principles of functional programming and their advantages.",
    "How do you ensure data privacy in applications that collect user information?",
    "What methods would you use to test the reliability of a distributed system?",
    "How does a load balancer work and what algorithms can it use?",
    "What are the key considerations for designing a fault-tolerant system?",
    "How would you implement authentication and authorization in a web application?",
    "Explain the concept of idempotency in API design and why it's important.",
    "How do content delivery networks (CDNs) improve website performance?",
    "What strategies would you use for effective error handling in distributed systems?",
    "How would you design a system with high availability and disaster recovery?",
    "Explain the principles of domain-driven design and when to apply them.",
    "How do you manage dependencies in large software projects?",
    "What techniques would you use for optimizing frontend performance?",
    "How does garbage collection work in modern programming languages?",
    "Explain the concept of immutability and its benefits in programming.",
    "What are the challenges of implementing a microservices architecture?",
    "How would you approach data migration in a production environment?",
    "What strategies would you use for effective logging in distributed applications?",
    "How does WebAssembly change web application development?",
    "Explain how OAuth 2.0 works for authorization.",
    "What methods would you use to ensure code quality in a team setting?",
    "How does a content management system work behind the scenes?",
    "What considerations are important when designing a database schema?",
    "How would you implement a real-time notification system?",
    "Explain the concept of eventual consistency and when it's appropriate.",
    "What are microcontrollers and how are they programmed?",
    "How would you design an effective caching strategy for a web application?",
    "What technologies and approaches would you use for building a chatbot?",
    "How does a compiler work to transform source code into executable code?",
    "What considerations are important when designing for mobile-first applications?",
    "How would you implement internationalization in a web application?",
    "What techniques would you use for data visualization in a dashboard?",
    "How does MapReduce work for processing large datasets?",
    "What are smart contracts and how are they implemented?",
    "How would you approach building an accessible web application?",
    "Explain how a relational database index works and when to use it.",
    "What strategies would you employ for continuous learning in a technical role?",
    "How does a DNS resolution process work?",
    "What considerations are important when designing APIs for mobile applications?",
    "How would you implement feature flags in a continuous deployment environment?",
    "Explain how virtual machines work compared to containers.",
    "What methods would you use to test the security of a web application?",
    "How does WebRTC enable peer-to-peer communication in browsers?",
    "What considerations are important when designing systems for low-latency trading?",
    "How would you approach optimizing algorithms for performance?",
    "Explain how database transactions ensure data integrity."
]

def generate_unique_questions(count=1000):
    """Generate unique questions for language model testing"""
    questions = []
    
    # Add specific technical questions first
    questions.extend(specific_questions)
    
    # Generate questions using templates
    remaining = count - len(questions)
    
    while len(questions) < count:
        # Select a random category, question type, and template
        category = random.choice(categories)
        question_type = random.choice(list(question_templates.keys()))
        template = random.choice(question_templates[question_type])
        
        # Select topic(s) for the question
        if "{}" in template:
            num_placeholders = template.count("{}")
            selected_topics = random.sample(topics[category], min(num_placeholders, len(topics[category])))
            
            # Fill in the template with topics
            try:
                if num_placeholders == 1:
                    question = template.format(selected_topics[0])
                elif num_placeholders == 2:
                    # Make sure we have two different topics for comparison questions
                    if len(selected_topics) < 2:
                        selected_topics.append(random.choice([t for t in topics[category] if t != selected_topics[0]]))
                    question = template.format(selected_topics[0], selected_topics[1])
            except IndexError:
                # Fallback if something goes wrong with formatting
                question = f"{question_type.capitalize()} about {selected_topics[0]}?"
        else:
            question = template
        
        # Add the question if it's unique
        if question not in questions:
            questions.append(question)
    
    # Shuffle the questions to mix the specifically crafted ones with the generated ones
    random.shuffle(questions)
    
    # Trim to exactly the requested count
    return questions[:count]

# Generate 1000 unique test questions
test_questions = generate_unique_questions(1000)

# Save to JSON file
with open('test_questions_1000.json', 'w', encoding='utf-8') as f:
    json.dump(test_questions, f, ensure_ascii=False, indent=2)

print(f"Generated {len(test_questions)} unique test questions and saved to test_questions_1000.json")

# Print some sample questions
print("\nSample questions:")
for i, question in enumerate(random.sample(test_questions, 10)):
    print(f"{i+1}. {question}")
