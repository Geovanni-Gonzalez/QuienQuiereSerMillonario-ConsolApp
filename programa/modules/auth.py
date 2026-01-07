from . import data_manager, ui

def login_admin():
    """
    Authenticates the administrative user.
    Input: User input via console (user, password).
    Output: Boolean (True if valid, False otherwise).
    Restrictions: Case sensitive check against loaded credentials.
    """
    ui.print_msg("--- INGRESO ADMINISTRATIVO ---")
    user = input("Usuario: ")
    pwd = input("Clave: ")
    
    admins = data_manager.cargar_accesos()
    if user in admins and admins[user] == pwd:
        ui.print_msg("¡Bienvenido Administrador!")
        return True
    else:
        ui.print_error("Credenciales incorrectas.")
        return False

def registrar_jugador():
    """
    Registers or Logs in a player.
    Input: Console interactions (ID, Name, Sex).
    Output: Dictionary with player info.
    Restrictions: ID must be 9 digits. Sex must be Hombre/Mujer.
    """
    ui.print_msg("--- REGISTRO DE JUGADOR ---")
    while True:
        cedula = input("Cédula (9 dígitos): ")
        if cedula.isdigit() and len(cedula) == 9:
            break
        ui.print_error("Cédula inválida. Debe tener exactamente 9 dígitos numéricos.")
        
    nombre = input("Nombre completo: ")
    while True:
        sexo = input("Sexo (Hombre/Mujer): ").capitalize()
        if sexo in ["Hombre", "Mujer"]:
            break
        ui.print_error("Sexo inválido. Ingrese 'Hombre' o 'Mujer'.")
    
    return {"cedula": cedula, "nombre": nombre, "sexo": sexo}
