class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def parse_to_int_list(s: str) -> list[float]:
    try:
        # Retire les parenthèses et les espaces
        s_clean = s.strip().strip("()").replace(" ", "")
        # Sépare les valeurs par la virgule
        parts = s_clean.split(",")
        # Convertit chaque élément en int
        return [float(part) for part in parts]
    except (ValueError, AttributeError):
        raise ValueError(f"Format invalide : '{s}' (attendu : '(x, y)')")
    
def parse_to_three_tuple(s: str) -> tuple[int]:
    try:
        # Retire les parenthèses et les espaces
        s_clean = s.strip().strip("()").replace(" ", "")
        # Sépare les valeurs par la virgule
        parts = s_clean.split(",")
        # Convertit chaque élément en int
        return [int(part) for part in parts]
    except (ValueError, AttributeError):
        raise ValueError(f"Format invalide : '{s}' (attendu : '(r, g, b)')")