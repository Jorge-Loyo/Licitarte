$content = Get-Content 'static\js\administracion.js' -Raw -Encoding UTF8

# Reemplazar todos los confirm() restantes
$content = $content -replace 'if \(!confirm\("([^"]+)"\)\) return;[\r\n\s]+const response', 'mostrarModalConfirmar("$1", async () => {`r`n  const response'
$content = $content -replace 'if \(!confirm\("([^"]+)"\)\)[\r\n\s]+return;[\r\n\s]+const response', 'mostrarModalConfirmar("$1", async () => {`r`n  const response'

# Cerrar las funciones que quedaron abiertas (agregar }); al final de cada función eliminar)
$content = $content -replace '(async function eliminar\w+\(id\) \{[\s\S]+?cargar\w+\(\);[\r\n\s]+\} else mostrarModalMensaje)', '$1'
$content = $content -replace '(\} else mostrarModalMensaje\("Mensaje", "Error: " \+ result\.error, "success"\);[\r\n]+\})', '$1`r`n  });`r`n}'

$content | Out-File 'static\js\administracion_fixed.js' -Encoding UTF8 -NoNewline

Write-Host "Archivo procesado. Revisa administracion_fixed.js"
