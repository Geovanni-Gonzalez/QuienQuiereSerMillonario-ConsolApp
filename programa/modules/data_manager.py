import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = BASE_DIR

def get_path(filename):
    """
    Resolves the absolute path for a data file.
    Input: filename (str).
    Output: Absolute path (str).
    """
    return os.path.join(DATA_DIR, filename)

def cargar_accesos():
    """
    Loads admin credentials from Acceso.txt.
    Input: None.
    Output: Dictionary {user: password}.
    Restrictions: File must exist.
    """
    path = get_path("Acceso.txt")
    creds = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 2:
                    creds[parts[0]] = parts[1]
    return creds

def load_questions():
    """
    Returns a list of dictionaries:
    [{'id': '1', 'question': '...', 'options': [...], 'correct': '...'}]
    """
    path = get_path("Preguntas.txt")
    questions = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 6:
                    questions.append({
                        'id': parts[0],
                        'question': parts[1],
                        'options': [parts[2], parts[3], parts[4]], # Wrong options
                        'correct': parts[5]
                    })
    return questions

def save_questions(questions_list):
    path = get_path("Preguntas.txt")
    with open(path, "w", encoding="utf-8") as f:
        for q in questions_list:
            # Format: ID,Pregunta,W1,W2,W3,Correct
            line = f"{q['id']},{q['question']},{q['options'][0]},{q['options'][1]},{q['options'][2]},{q['correct']}\n"
            f.write(line)

def get_next_question_id():
    qs = load_questions()
    if not qs: return 1
    return max(ids) + 1 if ids else 1

def save_new_game(questions):
    """
    Saves a list of 15 questions to a new game file.
    Updates IndiceJuegos.txt
    Returns the filename.
    """
    # 1. Determine next game ID
    idx_path = get_path("IndiceJuegos.txt")
    game_id = 1
    existing_files = []
    if os.path.exists(idx_path):
        with open(idx_path, "r") as f:
            existing_files = [line.strip() for line in f if line.strip()]
            if existing_files:
                # Assuming naming format ListaPreguntasXX.txt
                # Extract XX
                last = existing_files[-1]
                try:
                    num = int(last.replace("ListaPreguntas", "").replace(".txt", ""))
                    game_id = num + 1
                except:
                    game_id = len(existing_files) + 1

    filename = f"ListaPreguntas{game_id}.txt"
    full_path = get_path(filename)
    
    import datetime
    now = datetime.datetime.now()
    date_str = now.strftime("%d/%m/%Y")
    time_str = now.strftime("%H:%M:%S")

    with open(full_path, "w", encoding="utf-8") as f:
        # Header: ID, Date, Time
        f.write(f"{game_id},{date_str},{time_str}\n")
        # Questions using specific format from spec:
        # 100,PreguntaA,Op3,Op1,Respuesta,Op2,3
        # Wait, spec says: 100,PreguntaA,Opcion3,Opcion1,Respuesta,Opcion2,3
        # The last digit '3' implies position of correct answer (1-based index)
        
        import random
        for i, q in enumerate(questions):
            # We need to shuffle options and track the correct index
            all_ops = q['options'] + [q['correct']]
            random.shuffle(all_ops)
            
            # Find index of correct answer (1-4)
            correct_idx = all_ops.index(q['correct']) + 1
            
            # Line format based on spec example: 
            # ID(fake?), Question, Op1, Op2, Op3, Op4, CorrectIdx
            # Spec Example: 100,PreguntaA,Opcion3,Opcion1,Respuesta,Opcion2,3
            # Use q['id'] as logical ID
            
            line = f"{q['id']},{q['question']},{all_ops[0]},{all_ops[1]},{all_ops[2]},{all_ops[3]},{correct_idx}\n"
            f.write(line)

    # Update Index
    with open(idx_path, "a") as f:
        f.write(f"{filename}\n")
        
    return filename

def load_history():
    path = get_path("HistorialJuegos.txt")
    records = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 10:
                    records.append({
                        "cedula": parts[0],
                        "nombre": parts[1],
                        "sexo": parts[2],
                        "fecha_inicio": parts[3],
                        "hora_inicio": parts[4],
                        "fecha_fin": parts[5],
                        "hora_fin": parts[6],
                        "archivo": parts[7],
                        "premio": int(parts[8]),
                        "correctas": int(parts[9])
                    })
    return records

def save_game_record(record):
    path = get_path("HistorialJuegos.txt")
    # Record dict to CSV line
    line = f"{record['cedula']},{record['nombre']},{record['sexo']},{record['fecha_inicio']},{record['hora_inicio']},{record['fecha_fin']},{record['hora_fin']},{record['archivo']},{record['premio']},{record['correctas']}\n"
    with open(path, "a", encoding="utf-8") as f:
        f.write(line)

def get_game_files():
    path = get_path("IndiceJuegos.txt")
    if os.path.exists(path):
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def load_game_content(filename):
    """
    Parses a game file.
    Returns: { 'header': {...}, 'questions': [...] }
    """
    path = get_path(filename)
    if not os.path.exists(path): return None
    
    data = {'questions': []}
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if not lines: return None
        
        # Header
        parts = lines[0].strip().split(",")
        data['header'] = {'id': parts[0], 'date': parts[1], 'time': parts[2]}
        
        # Questions
        for line in lines[1:]:
            parts = line.strip().split(",")
            if len(parts) >= 7:
                 # ID,Question,Op1,Op2,Op3,Op4,CorrectIdx
                data['questions'].append({
                    'id': parts[0],
                    'text': parts[1],
                    'options': [parts[2], parts[3], parts[4], parts[5]],
                    'correct_idx': int(parts[6]), # 1-based
                    'full_correct_answer': parts[1+int(parts[6])] # Helper to store the text of correct answer
                })
    return data

def get_random_question_excluding(exclude_ids):
    """
    For 'Change Question' lifeline.
    """
    all_qs = load_questions()
    available = [q for q in all_qs if q['id'] not in exclude_ids]
    if available:
        import random
        return random.choice(available)
    return None



