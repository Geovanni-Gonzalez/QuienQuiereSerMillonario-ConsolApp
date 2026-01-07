from . import ui

PRIZES = [100, 200, 300, 400, 500, 1000, 2000, 2500, 4000, 5000, 7000, 8500, 9500, 12000, 15000]
SAFE_ZONES = [500, 2500, 5000, 15000]
SAFE_INDICES = [4, 7, 9, 14] # 0-indexed

from . import data_manager, ui
import datetime
import random

def iniciar_juego(player):
    """
    Main Game Loop.
    Input: player (dict) - Metadata of current player.
    Output: None (Saves result to file).
    Restrictions: Requires at least one game file in IndiceJuegos.txt.
    """
    # 1. Select random game
    idx_files = data_manager.get_game_files()
    if not idx_files:
        ui.print_error("No hay juegos generados. Contacte al administrador.")
        return

    game_file = random.choice(idx_files)
    game_data = data_manager.load_game_content(game_file)
    if not game_data:
        ui.print_error("Error cargando archivo de juego.")
        return

    ui.print_msg(f"¡Bienvenido {player['nombre']}! Juego cargado: {game_file}")
    
    start_time = datetime.datetime.now()
    
    # State
    current_level = 0
    prize_won = 0
    lifelines = {'50:50': True, 'CHANGE': True}
    questions = game_data['questions']
    
    while current_level < 15:
        q = questions[current_level]
        prize_current = PRIZES[current_level]
        
    while current_level < 15:
        q = questions[current_level]
        prize_current = PRIZES[current_level]
        
        ui.print_game_status(current_level, prize_current, SAFE_ZONES)
        ui.print_question(q['text'], q['options'])
        
        print("\n Comodines disponibles:", end=" ")
        if lifelines['50:50']: print("(C) 50:50", end=" ")
        if lifelines['CHANGE']: print("(X) Cambio Pregunta", end=" ")
        print("\n (R) Retirarse")
        
        ans = input("\n Su respuesta (1-4, C, X, R): ").upper()

        
        # Lifeline 50:50
        if ans == 'C' and lifelines['50:50']:
            lifelines['50:50'] = False
            correct = q['correct_idx'] - 1
            opts = [0, 1, 2, 3]
            opts.remove(correct)
            removed = random.sample(opts, 2)
            
            print(f"\n --- 50:50 APLICADO ---")
            temp_ops = []
            for i in range(4):
                if i in removed:
                    temp_ops.append("---")
                else:
                    temp_ops.append(q['options'][i])
            ui.print_question(q['text'], temp_ops)
            
            ans = input("\n Su respuesta (1-4, R): ").upper()


        # Lifeline Change
        if ans == 'X' and lifelines['CHANGE']:
            lifelines['CHANGE'] = False
            exclude = [x['id'] for x in questions]
            new_q_data = data_manager.get_random_question_excluding(exclude)
            
            if new_q_data:
                # Need to format new question to match current structure (shuffled)
                # Helper logic similar to Admin save
                all_ops = new_q_data['options'] + [new_q_data['correct']]
                random.shuffle(all_ops)
                correct_idx = all_ops.index(new_q_data['correct']) + 1
                
                # Replace current question object
                q = {
                    'id': new_q_data['id'],
                    'text': new_q_data['question'],
                    'options': all_ops,
                    'correct_idx': correct_idx,
                    'full_correct_answer': new_q_data['correct']
                }
                questions[current_level] = q # Update list
                ui.print_msg("¡Pregunta Cambiada!")
                continue # Restart loop to reprint new question
            else:
                ui.print_error("No hay preguntas disponibles para cambio.")

        # Logic
        if ans == 'R':
            ui.print_msg(f"Te has retirado con ₡ {prize_won}")
            break
            
        if ans.isdigit() and 1 <= int(ans) <= 4:
            if int(ans) == q['correct_idx']:
                ui.print_msg("¡Correcto!")
                prize_won = prize_current
                current_level += 1
                input("Presione Enter para continuar...")
            else:
                ui.print_error(f"Incorrecto. La respuesta era: {q['full_correct_answer']}")
                # Drop to safe zone
                safe_prize = 0
                for safe in SAFE_ZONES:
                    if prize_won >= safe:
                        safe_prize = safe
                prize_won = safe_prize
                ui.print_msg(f"Fin del juego. Te llevas ₡ {prize_won}")
                break
        else:
            ui.print_error("Opción no válida.")

    # End Game
    end_time = datetime.datetime.now()
    
    # Save History
    record = {
        "cedula": player['cedula'],
        "nombre": player['nombre'],
        "sexo": player['sexo'],
        "fecha_inicio": start_time.strftime("%d/%m/%Y"),
        "hora_inicio": start_time.strftime("%H:%M:%S"),
        "fecha_fin": end_time.strftime("%d/%m/%Y"),
        "hora_fin": end_time.strftime("%H:%M:%S"),
        "archivo": game_file,
        "premio": prize_won,
        "correctas": current_level
    }
    data_manager.save_game_record(record)
    ui.print_msg("Juego guardado en historial.")

