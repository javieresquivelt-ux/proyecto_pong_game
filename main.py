# Import turtle y sys
import turtle
import sys

# Configuración de ventana
try:
    wn = turtle.Screen()
    wn.title("Pong Game - Proyecto Conquer")
    wn.bgcolor("darkblue")
    wn.setup(width=800, height=600)
    wn.tracer(0)
except Exception:
    sys.exit(0)

def input_seguro(titulo, prompt, por_defecto=""):
    """Muestra un diálogo de entrada de texto seguro con manejo de errores.

    Args:
        titulo (str): Título de la ventana del diálogo.
        prompt (str): Mensaje que se muestra al usuario.
        por_defecto (str, optional): Valor por defecto si se cancela. Defaults to "".

    Returns:
        str: Texto ingresado por el usuario o valor por defecto.

    Raises:
        SystemExit: Si hay error crítico, cierra el programa limpiamente.
    """
    try:
        resultado = wn.textinput(titulo, prompt)
        return resultado if resultado is not None else por_defecto
    except:
        sys.exit(0)

# 1. Nombres jugadores
nombre_izq = input_seguro("Jugador Izquierdo", "Tu nombre:", "Jugador 1")
if nombre_izq is None: sys.exit(0) # Doble chequeo por seguridad

nombre_der = input_seguro("Jugador Derecho", "Tu nombre:", "Jugador 2")
if nombre_der is None: sys.exit(0) # Doble chequeo por seguridad

# 2. Controles
try:
    input_seguro("📋 CONTROLES", "Jugador Izquierda = S ↑ / X ↓\nJugadorDerecha = K ↑ / M ↓\n⚡ Acelera cada 10 pts\nENTER →")
except:
    sys.exit(0)

# 3. Puntos objetivo VALIDADO
puntos_objetivo = 10
while True:
    try:
        entrada = wn.textinput(
            "🎯 PUNTOS (5-50)",
            "Número ENTERO 5-50:\n"
            "ENTER o CANCELAR = 10 pts (defecto)\n"
            "❌ NO: letras, <5, >50"
        )
    except:
        sys.exit(0) # Si cierran la ventana principal a la fuerza
    
    # Si cancela o da enter vacío, usa el default (break)
    if entrada is None or not entrada.strip():
        break
        
    try:
        nuevo = int(entrada.strip())
        if 5 <= nuevo <= 50:
            puntos_objetivo = nuevo
            break
    except ValueError:
        pass  # Repite silenciosamente

# --- CONTROLES ---
# Envolvemos toda la creación de objetos. Si la ventana murió en el paso anterior,
# esto captura el error y cierra limpiamente en lugar de mostrar el Traceback.

try:
    # Chequeo preventivo
    if wn._root is None: # Chequeo interno de Tkinter
        raise turtle.Terminator

    wn.update()

    # Objetos seguros
    paddle_left = turtle.Turtle()
    paddle_left.speed(0)
    paddle_left.shape("square")
    paddle_left.color("cyan")
    paddle_left.shapesize(stretch_wid=5, stretch_len=1)
    paddle_left.penup()
    paddle_left.goto(-350, 0)

    paddle_right = turtle.Turtle()
    paddle_right.speed(0)
    paddle_right.shape("square")
    paddle_right.color("magenta")
    paddle_right.shapesize(stretch_wid=5, stretch_len=1)
    paddle_right.penup()
    paddle_right.goto(350, 0)

    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 1.8
    ball.dy = 1.8

    # Línea central
    linea_central = turtle.Turtle()
    linea_central.speed(0)
    linea_central.color("gray")
    linea_central.penup()
    linea_central.goto(0, 300)
    linea_central.pendown()
    linea_central.pensize(3)
    linea_central.hideturtle()
    for i in range(20):
        linea_central.goto(0, linea_central.ycor() - 20)
        linea_central.penup()
        linea_central.goto(0, linea_central.ycor() - 20)
        linea_central.pendown()

    # Marcador
    score_left = 0
    score_right = 0
    pen_marcador = turtle.Turtle()
    pen_marcador.speed(0)
    pen_marcador.color("white")
    pen_marcador.penup()
    pen_marcador.hideturtle()
    pen_marcador.goto(0, 260)
    pen_marcador.write(f"{nombre_izq}: 0  {nombre_der}: 0  (a {puntos_objetivo})",
                       align="center", font=("Arial", 20, "bold"))

except (turtle.Terminator, AttributeError, Exception):
    # Si algo falla al crear los objetos, salimos limpiamente
    sys.exit(0)

# Constantes
LIMITE_SUPERIOR = 250
LIMITE_INFERIOR = -250
PASO_PALETA = 20

# Movimientos
def mover_izquierda_arriba():
    """Mueve la paleta izquierda hacia arriba, respetando límites de pantalla."""
    try: paddle_left.sety(min(paddle_left.ycor() + PASO_PALETA, LIMITE_SUPERIOR))
    except: pass

def mover_izquierda_abajo():
    """Mueve la paleta izquierda hacia abajo, respetando límites de pantalla."""
    try: paddle_left.sety(max(paddle_left.ycor() - PASO_PALETA, LIMITE_INFERIOR))
    except: pass

def mover_derecha_arriba():
    """Mueve la paleta derecha hacia arriba, respetando límites de pantalla."""
    try: paddle_right.sety(min(paddle_right.ycor() + PASO_PALETA, LIMITE_SUPERIOR))
    except: pass

def mover_derecha_abajo():
    """Mueve la paleta derecha hacia abajo, respetando límites de pantalla."""
    try: paddle_right.sety(max(paddle_right.ycor() - PASO_PALETA, LIMITE_INFERIOR))
    except: pass

def salir_juego():
    """Cierra la ventana del juego limpiamente."""
    try: wn.bye()
    except: sys.exit(0)

# Controles + ESC global
try:
    wn.listen()
    wn.onkeypress(mover_izquierda_arriba, "s")
    wn.onkeypress(mover_izquierda_abajo, "x")
    wn.onkeypress(mover_derecha_arriba, "k")
    wn.onkeypress(mover_derecha_abajo, "m")
    wn.onkeypress(salir_juego, "Escape")
except:
    sys.exit(0)

def juego():
    """Loop principal del juego de Pong.

    Maneja movimiento de pelota, colisiones, puntuación, victoria y aceleración.
    Se ejecuta recursivamente cada 10ms con ontimer.
    
    Globals:
        score_left (int): Puntos del jugador izquierdo.
        score_right (int): Puntos del jugador derecho.
    """
    global score_left, score_right

    # Verificación de vida de la ventana dentro del loop
    try:
        wn.update()
    except (turtle.Terminator, Exception):
        sys.exit(0)

    # Victoria?
    if score_left >= puntos_objetivo or score_right >= puntos_objetivo:
        pen_marcador.clear()
        ganador = nombre_izq if score_left >= puntos_objetivo else nombre_der
        pen_marcador.goto(0, 200)
        pen_marcador.write(f"¡{ganador} GANADOR!\n({score_left}-{score_right})", 
                           align="center", font=("Arial", 32, "bold"))
        pen_marcador.goto(0, 120)
        pen_marcador.write("ESC para salir", align="center", font=("Arial", 20, "normal"))
        return

    # Mueve pelota
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)
    
    # Bordes Y
    if ball.ycor() > 290: ball.sety(290); ball.dy *= -1
    if ball.ycor() < -290: ball.sety(-290); ball.dy *= -1
    
    # Puntos
    if ball.xcor() > 390:
        ball.goto(0,0); ball.dx *= -1; score_left += 1
        pen_marcador.clear()
        pen_marcador.write(f"{nombre_izq}: {score_left}  {nombre_der}: {score_right}  (a {puntos_objetivo})",
                           align="center", font=("Arial", 20, "bold"))
    if ball.xcor() < -390:
        ball.goto(0,0); ball.dx *= -1; score_right += 1
        pen_marcador.clear()
        pen_marcador.write(f"{nombre_izq}: {score_left}  {nombre_der}: {score_right}  (a {puntos_objetivo})",
                           align="center", font=("Arial", 20, "bold"))
    
    # Colisiones paletas
    if (340 < ball.xcor() < 350) and (paddle_right.ycor()-50 < ball.ycor() < paddle_right.ycor()+50):
        ball.setx(340); ball.dx *= -1
    if (-350 < ball.xcor() < -340) and (paddle_left.ycor()-50 < ball.ycor() < paddle_left.ycor()+50):
        ball.setx(-340); ball.dx *= -1
    
    # Aceleración
    if (score_left + score_right) % 10 == 0 and score_left + score_right > 0:
        ball.dx *= 1.005
        
    wn.ontimer(juego, 10)

# Inicio
try:
    juego()
    wn.mainloop()
except:
    sys.exit(0)