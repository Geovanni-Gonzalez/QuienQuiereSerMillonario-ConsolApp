from . import ui

def menu_administrativo():
    while True:
        print("\n--- MENÚ ADMINISTRATIVO ---")
        print("1. Gestión de Preguntas")
        print("2. Gestión de Juegos")
        print("3. Historial de Juegos")
        print("4. Estadísticas")
        print("5. Retornar")
        
        op = input("Seleccione: ")
        if op == '5': break
        elif op == '1':
            gestion_preguntas()
        elif op == '2':
            gestion_juegos()
        elif op == '3':
            admin_historial()
        elif op == '4':
            admin_estadisticas()
        else:
            ui.print_msg("Opción no implementada aún.")


def gestion_juegos():
    """
    Menu for generating new game files.
    Input: User choice.
    Output: None (Creates files).
    Restrictions: Requires valid ID generation logic.
    """
    from . import data_manager
    import random
    
    ui.print_msg("--- GESTIÓN DE JUEGOS ---")
    print("1. Generar Nuevo Juego")
    print("2. Retornar")
    
    op = input("Seleccione: ")
    if op == '1':
        questions = data_manager.load_questions()
        if len(questions) < 15:
            ui.print_error(f"No hay suficientes preguntas. Se requieren 15, hay {len(questions)}.")
            return

        selected = random.sample(questions, 15)
        # Verify 15 unique -> random.sample ensures uniqueness if list is unique
        
        filename = data_manager.save_new_game(selected)
        ui.print_msg(f"¡Juego generado exitosamente! Guardado en: {filename}")

def admin_historial():
    """
    Viewer for game history.
    Input: Filter options.
    Output: Formatted table of records.
    Restrictions: Reads from specific text file.
    """
    from . import data_manager
    ui.print_msg("--- HISTORIAL DE JUEGOS ---")
    print("1. Filtrar por Rango de Fecha (No implementado en detalle)")
    print("2. Filtrar por Nombre de Jugador")
    print("3. Filtrar por Monto Ganado (Mayor a)")
    print("4. Ver Todos")
    
    op = input("Seleccione: ")
    records = data_manager.load_history()
    
    filtered = []
    if op == '2':
        name = input("Nombre a buscar: ").lower()
        filtered = [r for r in records if name in r['nombre'].lower()]
    elif op == '3':
        try:
            monto = int(input("Monto mínimo: "))
            filtered = [r for r in records if r['premio'] >= monto]
        except:
            ui.print_error("Monto inválido")
    else:
        filtered = records
        
    print(f"\n{'FECHA':<12} | {'JUGADOR':<20} | {'PREMIO':<10} | {'CORRECTAS'}")
    print("-" * 60)
    for r in filtered:
        print(f"{r['fecha_inicio']:<12} | {r['nombre']:<20} | {r['premio']:<10} | {r['correctas']}")

def admin_estadisticas():
    """
    Dashbord for game statistics.
    Input: None (Reads history).
    Output: Prints aggregate stats (Wins, Losses, Prizes).
    Restrictions: None.
    """
    from . import data_manager
    records = data_manager.load_history()
    
    total_games = len(records)
    # Win = Max prize (15000) or just logic? Usually answering all 15.
    wins = len([r for r in records if r['correctas'] == 15 and r['premio'] == 15000]) # Assuming 15000 is top prize
    losses = total_games - wins
    total_prizes = sum(r['premio'] for r in records)
    
    prizes_non_zero = [r['premio'] for r in records if r['premio'] > 0]
    max_prize = max(prizes_non_zero) if prizes_non_zero else 0
    min_prize = min(prizes_non_zero) if prizes_non_zero else 0
    
    ui.print_msg("--- ESTADÍSTICAS ---")
    print(f"Total Juegos: {total_games}")
    print(f"Juegos Ganados (15 aciertos): {wins}")
    print(f"Juegos Perdidos: {losses}")
    print(f"Suma Premios Entregados: {total_prizes}")
    print(f"Premio Máximo Otorgado: {max_prize}")
    print(f"Premio Mínimo Otorgado (>0): {min_prize}")
    input("\nPresione Enter para continuar...")


def gestion_preguntas():
    from . import data_manager
    while True:
        print("\n--- GESTIÓN DE PREGUNTAS ---")
        print("1. Listar Preguntas")
        print("2. Agregar Pregunta")
        print("3. Modificar Pregunta")
        print("4. Eliminar Pregunta")
        print("5. Retornar")
        
        op = input("Seleccione: ")
        if op == '5': break
        
        questions = data_manager.load_questions()
        
        if op == '1':
            ui.print_msg("--- Lista de Preguntas ---")
            for q in questions:
                print(f"ID: {q['id']} | {q['question']}")
                print(f"   Correcta: {q['correct']}")
                print(f"   Incorrectas: {', '.join(q['options'])}")
                
        elif op == '2':
            ui.print_msg("--- Agregar Pregunta ---")
            q_text = input("Pregunta: ")
            c_text = input("Respuesta Correcta: ")
            w1 = input("Incorrecta 1: ")
            w2 = input("Incorrecta 2: ")
            w3 = input("Incorrecta 3: ")
            
            new_id = str(data_manager.get_next_question_id())
            new_q = {
                'id': new_id,
                'question': q_text,
                'options': [w1, w2, w3],
                'correct': c_text
            }
            questions.append(new_q)
            data_manager.save_questions(questions)
            ui.print_msg(f"Pregunta agregada con ID {new_id}")
            
        elif op == '4':
            qid = input("ID de pregunta a eliminar: ")
            # TODO: Check if used in active game (future phase)
            found = False
            for i, q in enumerate(questions):
                if q['id'] == qid:
                    questions.pop(i)
                    found = True
                    break
            if found:
                data_manager.save_questions(questions)
                ui.print_msg("Pregunta eliminada.")
            else:
                ui.print_error("ID no encontrado.")
        
        elif op == '3':
             # Modification Logic (similar to add but finding ID first)
             pass

