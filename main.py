#Import
import turtle

# Configuración de la ventana
wn = turtle.Screen()
wn.title("Pong - Python Turtle")
wn.bgcolor("darkblue")
wn.setup(width=800, height=600)
wn.tracer(0)

# Ingreso de nombres de jugadores
nombre_izq = wn.textinput("Jugador Izquierdo", "Ingresa tu nombre:")
if not nombre_izq:
    nombre_izq = "Jugador 1"

nombre_der = wn.textinput("Jugador Derecho", "Ingresa tu nombre:")
if not nombre_der:
    nombre_der = "Jugador 2"

# INSTRUCCIONES INTERACTIVAS
wn.textinput("📋 CONTROLES DEL JUEGO", """
CONTROLES:

PALETA IZQUIERDA:
• S = Mover ARRIBA
• X = Mover ABAJO

PALETA DERECHA:
• K = Mover ARRIBA  
• M = Mover ABAJO

⚡ CADA 10 PUNTOS TOTALES la pelota se acelera

Presiona ENTER para JUGAR""")

# Paleta izquierda
paddle_left = turtle.Turtle()
paddle_left.speed(0)
paddle_left.shape("square")
paddle_left.color("cyan")
paddle_left.shapesize(stretch_wid=5, stretch_len=1)
paddle_left.penup()
paddle_left.goto(-350, 0)

# Paleta derecha
paddle_right = turtle.Turtle()
paddle_right.speed(0)
paddle_right.shape("square")
paddle_right.color("magenta")
paddle_right.shapesize(stretch_wid=5, stretch_len=1)
paddle_right.penup()
paddle_right.goto(350, 0)

# Pelota
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 1.8
ball.dy = 1.8

# Línea central punteada
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

# Marcador con nombres
score_left = 0
score_right = 0
velocidad_actual = 1.0 

pen_marcador = turtle.Turtle()
pen_marcador.speed(0)
pen_marcador.color("white")
pen_marcador.penup()
pen_marcador.hideturtle()
pen_marcador.goto(0, 260)
pen_marcador.write("Izq: 0  Der: 0",
                   align="center", font=("Arial", 24, "bold"))

# Constantes
LIMITE_SUPERIOR = 250
LIMITE_INFERIOR = -250
PASO_PALETA = 20

# Funciones de movimiento
def mover_izquierda_arriba():
    """
    Mueve la paleta izquierda hacia arriba hasta el límite superior.
    Obtiene la posición Y actual, suma el paso de movimiento y aplica límites.
    No retorna nada (modifica el objeto paddle_left directamente).
    """
    y = paddle_left.ycor()
    y += PASO_PALETA
    if y > LIMITE_SUPERIOR:
        y = LIMITE_SUPERIOR
    paddle_left.sety(y)

def mover_izquierda_abajo():
    """
    Mueve la paleta izquierda hacia abajo hasta el límite inferior.
    Obtiene la posición Y actual, resta el paso de movimiento y aplica límites.
    No retorna nada (modifica el objeto paddle_left directamente).
    """
    y = paddle_left.ycor()
    y -= PASO_PALETA
    if y < LIMITE_INFERIOR:
        y = LIMITE_INFERIOR
    paddle_left.sety(y)

def mover_derecha_arriba():
    """
    Mueve la paleta derecha hacia arriba hasta el límite superior.
    Obtiene la posición Y actual, suma el paso de movimiento y aplica límites.
    No retorna nada (modifica el objeto paddle_right directamente).
    """
    y = paddle_right.ycor()
    y += PASO_PALETA
    if y > LIMITE_SUPERIOR:
        y = LIMITE_SUPERIOR
    paddle_right.sety(y)

def mover_derecha_abajo():
    """
    Mueve la paleta derecha hacia abajo hasta el límite inferior.
    Obtiene la posición Y actual, resta el paso de movimiento y aplica límites.
    No retorna nada (modifica el objeto paddle_right directamente).
    """
    y = paddle_right.ycor()
    y -= PASO_PALETA
    if y < LIMITE_INFERIOR:
        y = LIMITE_INFERIOR
    paddle_right.sety(y)

# Controles de teclado
wn.listen()
wn.onkeypress(mover_izquierda_arriba, "s")
wn.onkeypress(mover_izquierda_abajo, "x")
wn.onkeypress(mover_derecha_arriba, "k")
wn.onkeypress(mover_derecha_abajo, "m")

# FUNCIÓN PRINCIPAL DEL JUEGO
def juego():
    """
    Bucle principal del juego Pong.
    Actualiza la pantalla, mueve la pelota, detecta colisiones con bordes y paletas,
    actualiza puntajes y programa la siguiente llamada recursiva cada 10ms.
    No retorna nada (usa variables globales para scores).
    """
    global score_left, score_right, velocidad_actual

    wn.update()

    # Mover la pelota
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Bordes superior e inferior
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Bordes izquierda y derecha
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_left += 1
        pen_marcador.clear()
        pen_marcador.write(f"{nombre_izq}: {score_left}  {nombre_der}: {score_right}",
                           align="center", font=("Arial", 24, "bold"))

    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball.dx *= -1
        score_right += 1
        pen_marcador.clear()
        pen_marcador.write(f"{nombre_izq}: {score_left}  {nombre_der}: {score_right}",
                           align="center", font=("Arial", 24, "bold"))

    # Colisión paleta derecha
    if (340 < ball.xcor() < 350 and
        paddle_right.ycor() - 50 < ball.ycor() < paddle_right.ycor() + 50):
        ball.setx(340)
        ball.dx *= -1

    # Colisión paleta izquierda
    if (-350 < ball.xcor() < -340 and
        paddle_left.ycor() - 50 < ball.ycor() < paddle_left.ycor() + 50):
        ball.setx(-340)
        ball.dx *= -1

    # Velocidad progresiva (cada 10 puntos) - Lógica interna
    puntos_totales = score_left + score_right
    if puntos_totales > 0 and puntos_totales % 10 == 0:
        velocidad_actual *= 1.05
        ball.dx *= 1.001 # Aceleración muy leve continua para evitar saltos bruscos
        
    wn.ontimer(juego, 10)

# Inicia el juego
juego()
wn.mainloop()