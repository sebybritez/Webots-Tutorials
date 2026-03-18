from controller import Robot

# Crear la instancia del robot
robot = Robot()

# Configurar el tiempo de paso (milisegundos)
timestep = int(robot.getBasicTimeStep())

# Velocidad máxima permitida para el e-puck
MAX_SPEED = 6.28

# Configurar motores
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Configurar los sensores de suelo (Ground Sensors)
# gs0: izquierda, gs1: centro, gs2: derecha
gs = []
gs_names = ['gs0', 'gs1', 'gs2']
for name in gs_names:
    sensor = robot.getDevice(name)
    sensor.enable(timestep)
    gs.append(sensor)

# Bucle principal de la simulación
while robot.step(timestep) != -1:
    # Leer valores de los sensores
    # Generalmente: Negro < 400 y Blanco > 600
    val_left = gs[0].getValue()
    val_center = gs[1].getValue()
    val_right = gs[2].getValue()

    # Velocidades base
    left_speed = MAX_SPEED * 0.5
    right_speed = MAX_SPEED * 0.5

    # Lógica de seguimiento
    if val_center < 450:
        # El centro está en la línea: ir recto
        left_speed = MAX_SPEED * 0.8
        right_speed = MAX_SPEED * 0.8
    elif val_left < 450:
        # Se sale por la derecha (línea a la izquierda): girar a la izquierda
        left_speed = -MAX_SPEED * 0.2
        right_speed = MAX_SPEED * 0.5
    elif val_right < 450:
        # Se sale por la izquierda (línea a la derecha): girar a la derecha
        left_speed = MAX_SPEED * 0.5
        right_speed = -MAX_SPEED * 0.2
    else:
        # Si no ve nada, que avance lento para buscar
        left_speed = MAX_SPEED * 0.2
        right_speed = MAX_SPEED * 0.2

    # Aplicar velocidades
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)
