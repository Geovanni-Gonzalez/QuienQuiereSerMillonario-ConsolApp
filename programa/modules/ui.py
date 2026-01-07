import os

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m" # Gold-ish
    RED = "\033[91m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_BLUE = "\033[44m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def intro_animation():
    clear_screen()
    import time
    
    # Simple "Loading" effect
    print("\n\n\n")
    print(f"{Colors.BLUE}{'Cargando Estudio de Grabación...':^60}{Colors.RESET}")
    time.sleep(1)
    clear_screen()
    
    # ASCII ART
    logo = f"""
    {Colors.YELLOW}
       $$$$$$\  $$$$$$$\  $$$$$$$\  
      $$  __$$\ $$  __$$\ $$  __$$\ 
      $$ /  \__|$$ |  $$ |$$ |  $$ |
      \$$$$$$\  $$$$$$$  |$$ |  $$ |
       \____$$\ $$  ____/ $$ |  $$ |
      $$\   $$ |$$ |      $$ |  $$ |
      \$$$$$$  |$$ |      $$$$$$$  |
       \______/ \__|      \_______/ 
    {Colors.RESET}
    """
    
    lines = logo.split("\n")
    for line in lines:
        print(f"{Colors.BOLD}{line:^60}{Colors.RESET}")
        time.sleep(0.1)
        
    print(f"\n{Colors.CYAN}{'¿Quién Quiere Ser Millonario?':^60}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    time.sleep(1)

def mostrar_menu_principal():
    clear_screen()
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}{'¿QUIÉN QUIERE SER MILLONARIO?':^60}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}")
    print("\n")
    print(f"      {Colors.CYAN}[ A ]{Colors.RESET}   Opciones Administrativas")
    print("\n")
    print(f"      {Colors.CYAN}[ J ]{Colors.RESET}   Opciones de Jugador")
    print("\n")
    print(f"      {Colors.CYAN}[ S ]{Colors.RESET}   Salir")
    print("\n")
    print(f"{Colors.BLUE}{'-'*60}{Colors.RESET}")
    return input(f" {Colors.YELLOW}Seleccione una opción > {Colors.RESET}").upper()

def print_game_status(level, prize, safe_zones):
    clear_screen()
    print("\n")
    safe_txt = f"{Colors.GREEN} *** ZONA SEGURA ***{Colors.RESET}" if prize in safe_zones else ""
    print(f"{Colors.BOLD} NIVEL {level+1}/15  ---  PREMIO ACUMULADO: {Colors.YELLOW}₡ {prize}{Colors.RESET}{safe_txt}")
    print(Colors.BLUE + "-" * 60 + Colors.RESET)

def print_question(text, options):
    print(" " + "_"*58)
    print(f"| {Colors.WHITE}{text:^56}{Colors.RESET} |")
    print(" " + "-"*58)
    
    # Options layout:
    row1 = f" {Colors.CYAN}1:{Colors.RESET} {options[0]:<23} | {Colors.CYAN}2:{Colors.RESET} {options[1]:<23}"
    row2 = f" {Colors.CYAN}3:{Colors.RESET} {options[2]:<23} | {Colors.CYAN}4:{Colors.RESET} {options[3]:<23}"
    
    print(f"|{row1}|")
    print(f"|{row2}|")
    print(" " + "-"*58)

def print_msg(msg):
    print(f"\n{Colors.GREEN}[INFO]{Colors.RESET} {msg}")
    input(" Presione Enter para continuar...")

def print_error(msg):
    print(f"\n{Colors.RED}[ERROR]{Colors.RESET} {msg}")
    input(" Presione Enter para continuar...")


