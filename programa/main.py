import sys
import os

# Ensure modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules import ui, auth, admin, game

def main():
    # Play intro once
    ui.intro_animation()
    
    while True:
        opcion = ui.mostrar_menu_principal()
        
        if opcion == 'A':
            if auth.login_admin():
                admin.menu_administrativo()
        elif opcion == 'J':
            # Player flow
            player = auth.registrar_jugador()
            if player:
                game.iniciar_juego(player)
        elif opcion == 'S':
            ui.print_msg("¡Gracias por jugar! Guardando datos...")
            # Save data if needed
            sys.exit()
        else:
            ui.print_error("Opción inválida.")

if __name__ == "__main__":
    main()
