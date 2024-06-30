from flask import Flask, request, render_template
import json

app = Flask(__name__)

# Load admission-related information from a JSON file
try:
    with open('admission_info.json', 'r') as f:
        admission_info = json.load(f)
except FileNotFoundError:
    admission_info = {}

# Context variables to remember previous questions and answers
context = {
    'program': None,
    'degree': None,
    'university': None
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_query = request.form['user_query']
        response = handle_user_query(user_query)
        
        return render_template('index.html', question=user_query, response=response)
    
    return render_template('index.html')

def handle_user_query(query):
    global context
    
    if 'documents' in query.lower() or 'requirements' in query.lower():
        return handle_requirements_query(query)
    elif 'deadlines' in query.lower() or 'deadline' in query.lower():
        return handle_deadlines_query(query)
    else:
        return "I'm sorry, I don't have enough information to answer your query. Please try rephrasing your question or check our admission information page."





def handle_requirements_query(query):
    global context
    program, degree, university = parse_query(query)
    update_context(program, degree, university)
    
    if not program or not university:
        return "I'm sorry, I couldn't find the program you're asking about. Please specify the program name and university."

    # Check if degree level is missing in the context
    if degree is None:
        return f"Please specify the degree level for the {program} program at {university}."
    
    # Now, use the degree level from the context to fetch requirements
    for uni in admission_info.get("admission_info", []):
        if uni["university"].lower() == university.lower():
            for prog in uni.get("programs", []):
                if prog["program_name"].lower() == program.lower() and prog["degree_level"].lower() == degree.lower():
                    requirements = prog['requirements']
                    
                    documents = []
                    additional_requirements = []

                    for req in requirements:
                        if isinstance(req, dict) and 'documents' in req:
                            documents.extend(req['documents'])
                        elif isinstance(req, str):
                            additional_requirements.append(req)

                    all_requirements = documents + additional_requirements
                    all_requirements_str = ', '.join(all_requirements)
                    
                    return f"The requirements to apply to the {prog['program_name']} {prog['degree_level']} program at {uni['university']} are: {all_requirements_str}."

    return "I'm sorry, I couldn't find the program you're asking about. Please specify the program name, degree level, and university."

def handle_deadlines_query(query):
    global context
    program, degree, university = parse_query(query)
    update_context(program, degree, university)
    
    if not program or not university:
        return "I'm sorry, I couldn't find the program or deadline type you're asking about. Please specify the program name and university."

    if degree is None:
        return f"Please specify the degree level for the {program} program at {university}."
    
    for uni in admission_info.get("admission_info", []):
        if uni["university"].lower() == university.lower():
            for prog in uni.get("programs", []):
                if prog["program_name"].lower() == program.lower() and prog["degree_level"].lower() == degree.lower():
                    deadlines = ", ".join([f"{k.replace('_', ' ')}: {v}" for k, v in prog["deadlines"].items()])
                    return f"The deadlines for the {program} {degree} program at {university} are: {deadlines}."

    return "I'm sorry, I couldn't find the program or deadline type you're asking about. Please specify the program name, degree level, and university."





context = {
    'query': None,
    'program': None,
    'degree': None,
    'university': None
}

def parse_query(query):
    program = context.get('program')
    degree = context.get('degree')
    university = context.get('university')

    # Example logic for parsing the query to extract program, degree, and university
    # Replace with your own parsing logic based on how queries are structured
    if "Psychology" in query and "Another University" in query:
        program = "Psychology"
        university = "Another University"
    elif "Computer Science" in query and "Example University" in query:
        program = "Computer Science"
        university = "Example University"
    elif "Business Administration" in query and "Example University" in query:
        program = "Business Administration"
        university = "Example University"

    # Example logic to extract degree level
    if "undergraduate" in query.lower():
        degree = "Undergraduate"
    elif "graduate" in query.lower():
        degree = "Graduate"

    return program, degree, university

def update_context(program, degree, university):
    global context
    if program:
        context['program'] = program
    if degree:
        context['degree'] = degree
    if university:
        context['university'] = university

def handle_requirements_query(query):
    global context
    program, degree, university = parse_query(query)
    update_context(program, degree, university)
    
    if not program or not university:
        return "I'm sorry, I couldn't find the program you're asking about. Please specify the program name and university."

    # Check if degree level is missing in the context
    if degree is None:
        # Store the current query in context to use later
        context['query'] = query
        return f"Please specify the degree level for the {program} program at {university}."

    # Use context to find and return requirements or deadlines
    for uni in admission_info.get("admission_info", []):
        if uni["university"].lower() == university.lower():
            for prog in uni.get("programs", []):
                if prog["program_name"].lower() == program.lower() and prog["degree_level"].lower() == degree.lower():
                    if 'requirements' in prog:
                        requirements = prog['requirements']
                        documents = []
                        additional_requirements = []

                        for req in requirements:
                            if isinstance(req, dict) and 'documents' in req:
                                documents.extend(req['documents'])
                            elif isinstance(req, str):
                                additional_requirements.append(req)

                        all_requirements = documents + additional_requirements
                        all_requirements_str = ', '.join(all_requirements)

                        return f"The requirements to apply to the {prog['program_name']} {prog['degree_level']} program at {uni['university']} are: {all_requirements_str}."
                    elif 'deadlines' in prog:
                        deadlines = prog['deadlines']
                        # Logic to format and return deadlines
                        return f"The deadlines for the {prog['program_name']} {prog['degree_level']} program at {uni['university']} are: {', '.join(deadlines.values())}."

    return "I'm sorry, I couldn't find the program you're asking about. Please specify the program name, degree level, and university."


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
