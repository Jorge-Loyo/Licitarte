import re

with open('static/js/administracion.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazar alert() simples
content = re.sub(r'alert\("Error al cargar clientes: " \+ error\.message\);', 
                 'mostrarModalMensaje("Error", "Error al cargar clientes: " + error.message, "error");', content)
content = re.sub(r'alert\("Debe seleccionar un Organismo/Jurisdicción"\);',
                 'mostrarModalMensaje("Advertencia", "Debe seleccionar un Organismo/Jurisdicción", "error"); return;', content)
content = re.sub(r'alert\(id \? "Cliente actualizado" : "Cliente creado"\);',
                 'mostrarModalMensaje("Éxito", id ? "Cliente actualizado" : "Cliente creado", "success");', content)
content = re.sub(r'alert\("Error: " \+ result\.error\);',
                 'mostrarModalMensaje("Error", result.error, "error");', content)
content = re.sub(r'alert\("Error de conexión: " \+ error\.message\);',
                 'mostrarModalMensaje("Error", "Error de conexión: " + error.message, "error");', content)

# Reemplazar confirm() y eliminar
content = re.sub(r'if \(!confirm\("¿Eliminar este cliente\?"\)\) return;\n\n  const response = await fetch\(`/api/clientes/\$\{id\}`, \{ method: "DELETE" \}\);\n  const result = await response\.json\(\);\n\n  if \(result\.success\) \{\n    alert\("Cliente eliminado"\);\n    cargarClientes\(\);\n  \} else \{\n    alert\("Error: " \+ result\.error\);\n  \}',
                 '''mostrarModalConfirmar("¿Eliminar este cliente?", async () => {
    const response = await fetch(`/api/clientes/${id}`, { method: "DELETE" });
    const result = await response.json();
    if (result.success) {
      cargarClientes();
      mostrarModalMensaje("Éxito", "Cliente eliminado", "success");
    } else {
      mostrarModalMensaje("Error", result.error, "error");
    }
  });''', content)

# Reemplazar todos los alert() restantes con patrón genérico
content = re.sub(r'alert\(([^)]+)\);', r'mostrarModalMensaje("Mensaje", \1, "success");', content)

# Guardar
with open('static/js/administracion.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Reemplazos completados")
