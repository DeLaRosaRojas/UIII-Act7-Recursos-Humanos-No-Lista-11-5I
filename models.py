from django.db import models

# ==========================================
# MODELO: DEPARTAMENTO
# ==========================================
class Departamento(models.Model):
    nombre_departamento = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    id_gerente_departamento = models.ForeignKey(
        "Empleado_RRHH",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="departamentos_gerenciados"
    )
    fecha_creacion = models.DateField()
    num_empleados = models.IntegerField()

    def __str__(self):
        return self.nombre_departamento


# ==========================================
# MODELO: PUESTO
# ==========================================
class Puesto(models.Model):
    nombre_puesto = models.CharField(max_length=100, unique=True)
    descripcion_puesto = models.TextField()
    salario_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    salario_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    nivel_jerarquico = models.CharField(max_length=50)
    habilidades_requeridas = models.TextField()

    def __str__(self):
        return self.nombre_puesto


# ==========================================
# MODELO: EMPLEADO_RRHH
# ==========================================
class Empleado_RRHH(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()
    cargo = models.ForeignKey(
        Puesto,
        to_field="nombre_puesto",
        on_delete=models.SET_NULL,
        null=True,
        related_name="empleados_con_puesto"
    )
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.ForeignKey(
        Departamento,
        to_field="nombre_departamento",
        on_delete=models.SET_NULL,
        null=True,
        related_name="empleados_del_departamento"
    )
    estado_empleado = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# ==========================================
# MODELO: AUSENCIA
# ==========================================
class Ausencia(models.Model):
    id_empleado = models.ForeignKey(
        Empleado_RRHH,
        on_delete=models.CASCADE,
        related_name="ausencias"
    )
    tipo_ausencia = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_aprobacion = models.CharField(max_length=50)
    motivo_ausencia = models.TextField()
    comentarios = models.TextField()

    def __str__(self):
        return f"Ausencia de {self.id_empleado} ({self.tipo_ausencia})"


# ==========================================
# MODELO: EVALUACION DE DESEMPEÑO
# ==========================================
class Evaluacion_Desempeno(models.Model):
    id_empleado = models.ForeignKey(
        Empleado_RRHH,
        on_delete=models.CASCADE,
        related_name="evaluaciones_recibidas"
    )
    fecha_evaluacion = models.DateField()
    calificacion = models.DecimalField(max_digits=4, decimal_places=2)
    comentarios_evaluador = models.TextField()
    objetivos_establecidos = models.TextField()
    fecha_proxima_evaluacion = models.DateField()
    id_evaluador = models.ForeignKey(
        Empleado_RRHH,
        on_delete=models.SET_NULL,
        null=True,
        related_name="evaluaciones_realizadas"
    )

    def __str__(self):
        return f"Evaluación {self.id} para {self.id_empleado}"


# ==========================================
# MODELO: CAPACITACION
# ==========================================
class Capacitacion(models.Model):
    nombre_capacitacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    proveedor = models.CharField(max_length=100)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_horas = models.IntegerField()
    es_obligatoria = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_capacitacion


# ==========================================
# MODELO: PARTICIPACION EN CAPACITACION
# ==========================================
class Participacion_Capacitacion(models.Model):
    id_empleado = models.ForeignKey(
        Empleado_RRHH,
        on_delete=models.CASCADE,
        related_name="participaciones_capacitacion"
    )
    id_capacitacion = models.ForeignKey(
        Capacitacion,
        on_delete=models.CASCADE,
        related_name="participantes"
    )
    fecha_inscripcion = models.DateField()
    estado_participacion = models.CharField(max_length=50)
    calificacion_obtenida = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_finalizacion = models.DateField()

    def __str__(self):
        return f"{self.id_empleado} en {self.id_capacitacion}"
