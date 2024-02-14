CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY,
    descripcion TEXT NOT NULL,
    fecha_creacion TEXT NOT NULL,
    completada INTEGER
);
