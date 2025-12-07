# 💾 **PROTOCOLOS DE BACKUP**

## 🎯 **PROPÓSITO**

Protocolos obligatorios para prevenir pérdida de datos y permitir rollback seguro en colaboraciones humano-IA, especialmente en entornos productivos.

**Regla de Oro:** *Nunca modificar sin backup. Nunca asumir que "no pasará nada".*

---

## ⚠️ **REGLAS FUNDAMENTALES**

### **1. BACKUP ANTES DE CUALQUIER MODIFICACIÓN**
- ✅ **Obligatorio:** Backup completo antes de iniciar
- ✅ **Obligatorio:** Backup por archivo antes de modificar
- ✅ **Obligatorio:** Documentar ubicación de backups
- ❌ **Prohibido:** Modificar sin backup verificado

### **2. TIPOS DE BACKUP REQUERIDOS**

#### **Backup Completo del Proyecto:**
- Código fuente completo
- Base de datos (si aplica)
- Archivos de configuración
- Documentación existente
- Variables de entorno

#### **Backup por Archivo (.bak):**
- Crear archivo.ext.bak antes de modificar archivo.ext
- Mantener versión original intacta
- Documentar cambios realizados
- Verificar integridad del backup

#### **Backup de Estado del Sistema:**
- Configuraciones de servidor
- Estados de servicios
- Logs relevantes
- Dependencias y versiones

---

## 🔄 **PROTOCOLOS OPERATIVOS**

### **PROTOCOLO 1: INICIO DE PROYECTO**
```
1. Crear backup completo del estado inicial
2. Documentar ubicación del backup
3. Verificar integridad del backup
4. Establecer estrategia de backup incremental
5. Definir puntos de rollback críticos
```

### **PROTOCOLO 2: ANTES DE CADA MODIFICACIÓN**
```
1. Identificar archivos a modificar
2. Crear backup .bak de cada archivo
3. Documentar propósito de la modificación
4. Verificar que backup es accesible
5. Proceder con modificación
```

### **PROTOCOLO 3: DURANTE MODIFICACIONES**
```
1. Una modificación a la vez
2. Verificar funcionamiento después de cada cambio
3. Documentar cada paso realizado
4. Crear checkpoints en modificaciones complejas
5. Mantener comunicación constante con humano
```

### **PROTOCOLO 4: ROLLBACK DE EMERGENCIA**
```
1. Detener modificaciones inmediatamente
2. Identificar último estado funcional conocido
3. Restaurar desde backup más reciente
4. Verificar funcionamiento del sistema
5. Documentar causa del rollback
```

---

## 📁 **ESTRUCTURA DE BACKUP RECOMENDADA**

### **Para Proyectos de Desarrollo:**
```
project-name/
├── backups/
│   ├── full-backup-YYYY-MM-DD-HH-MM/
│   ├── incremental-YYYY-MM-DD-HH-MM/
│   └── emergency-rollback/
├── src/
│   ├── file1.js
│   ├── file1.js.bak
│   ├── file2.py
│   └── file2.py.bak
└── docs/
    ├── BACKUP_LOG.md
    └── ROLLBACK_PROCEDURES.md
```

### **Para Sitios Web:**
```
website/
├── backups/
│   ├── code-backup-YYYY-MM-DD/
│   ├── database-backup-YYYY-MM-DD.sql
│   └── config-backup-YYYY-MM-DD/
├── public_html/
│   ├── index.php
│   ├── index.php.bak
│   └── config.php.bak
└── logs/
    └── backup-log.txt
```

---

## 🚨 **SITUACIONES DE ALTO RIESGO**

### **Entornos Productivos:**
- ⚠️ **Riesgo Crítico:** Modificaciones directas en producción
- ✅ **Protocolo:** Backup completo + staging + validación
- ✅ **Rollback:** Plan de rollback en menos de 5 minutos

### **Bases de Datos:**
- ⚠️ **Riesgo Crítico:** Modificaciones de esquema o datos
- ✅ **Protocolo:** Dump completo + transacciones + verificación
- ✅ **Rollback:** Scripts de rollback probados

### **Archivos de Configuración:**
- ⚠️ **Riesgo Crítico:** Cambios en configuraciones críticas
- ✅ **Protocolo:** Backup + documentación + validación
- ✅ **Rollback:** Configuración anterior verificada

---

## 📋 **CHECKLIST DE BACKUP**

### **Antes de Iniciar Proyecto:**
- [ ] ¿Existe backup completo del estado inicial?
- [ ] ¿Está documentada la ubicación del backup?
- [ ] ¿Se ha verificado la integridad del backup?
- [ ] ¿Está definida la estrategia de backup incremental?
- [ ] ¿Existen procedimientos de rollback documentados?

### **Antes de Cada Modificación:**
- [ ] ¿Se identificaron todos los archivos a modificar?
- [ ] ¿Se crearon archivos .bak para cada archivo?
- [ ] ¿Está documentado el propósito de la modificación?
- [ ] ¿Se verificó acceso a los backups?
- [ ] ¿Se estableció criterio de éxito/fallo?

### **Durante Modificaciones:**
- [ ] ¿Se está modificando un archivo a la vez?
- [ ] ¿Se verifica funcionamiento después de cada cambio?
- [ ] ¿Se documentan los pasos realizados?
- [ ] ¿Se mantiene comunicación con el humano?
- [ ] ¿Se crean checkpoints en modificaciones complejas?

---

## 🛠️ **HERRAMIENTAS Y COMANDOS**

### **Backup de Archivos (Linux/Mac):**
```bash
# Backup individual
cp file.txt file.txt.bak

# Backup con timestamp
cp file.txt file.txt.$(date +%Y%m%d_%H%M%S).bak

# Backup de directorio completo
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz /path/to/directory
```

### **Backup de Base de Datos:**
```bash
# MySQL
mysqldump -u user -p database_name > backup_$(date +%Y%m%d_%H%M%S).sql

# PostgreSQL
pg_dump -U user database_name > backup_$(date +%Y%m%d_%H%M%S).sql
```

### **Verificación de Integridad:**
```bash
# Verificar archivo
md5sum file.txt > file.txt.md5
md5sum -c file.txt.md5

# Verificar backup
diff original.txt backup.txt
```

---

## 📊 **REGISTRO DE BACKUP**

### **Template de Log de Backup:**
```markdown
# BACKUP LOG

## Backup Completo
- **Fecha:** YYYY-MM-DD HH:MM:SS
- **Ubicación:** /path/to/backup
- **Tamaño:** XXX MB
- **Verificación:** ✅ Exitosa / ❌ Fallida
- **Notas:** Descripción del estado del sistema

## Backups Incrementales
| Fecha | Archivo | Ubicación | Verificado | Notas |
|-------|---------|-----------|------------|-------|
| | | | | |

## Rollbacks Realizados
| Fecha | Motivo | Backup Usado | Resultado | Lecciones |
|-------|--------|--------------|-----------|-----------|
| | | | | |
```

---

## 🔄 **PROCEDIMIENTOS DE ROLLBACK**

### **Rollback de Archivo Individual:**
```
1. Detener proceso que usa el archivo
2. Renombrar archivo actual: file.txt -> file.txt.failed
3. Restaurar backup: file.txt.bak -> file.txt
4. Verificar integridad del archivo restaurado
5. Reiniciar proceso y verificar funcionamiento
6. Documentar causa del rollback
```

### **Rollback de Proyecto Completo:**
```
1. Detener todos los servicios relacionados
2. Crear backup del estado actual (para análisis)
3. Restaurar desde backup completo más reciente
4. Verificar integridad de archivos restaurados
5. Reiniciar servicios en orden correcto
6. Verificar funcionamiento completo del sistema
7. Documentar incidente y lecciones aprendidas
```

---

## ⚡ **CASOS DE EMERGENCIA**

### **Pérdida de Datos Crítica:**
1. **NO PÁNICO** - Detener todas las operaciones
2. **Evaluar** alcance del daño
3. **Identificar** último backup confiable
4. **Restaurar** desde backup verificado
5. **Validar** integridad de datos restaurados
6. **Documentar** incidente completo

### **Corrupción de Sistema:**
1. **Aislar** sistema afectado
2. **Identificar** causa de corrupción
3. **Restaurar** desde backup limpio
4. **Implementar** medidas preventivas
5. **Monitorear** sistema restaurado
6. **Actualizar** procedimientos de backup

---

## 🎯 **MEJORES PRÁCTICAS**

### **Frecuencia de Backup:**
- **Proyectos activos:** Backup diario mínimo
- **Entornos productivos:** Backup antes de cada deploy
- **Modificaciones críticas:** Backup inmediatamente antes
- **Archivos individuales:** Backup antes de cada modificación

### **Retención de Backups:**
- **Backups diarios:** Mantener 7 días
- **Backups semanales:** Mantener 4 semanas
- **Backups mensuales:** Mantener 12 meses
- **Backups críticos:** Mantener indefinidamente

### **Verificación de Backups:**
- **Integridad:** Verificar checksums regularmente
- **Accesibilidad:** Probar restauración mensualmente
- **Completitud:** Validar que incluye todos los archivos necesarios
- **Documentación:** Mantener logs actualizados

---

**🎯 Propósito:** Prevenir pérdida de datos y permitir rollback seguro  
**⚡ Regla de Oro:** Backup antes de modificar, siempre  
**🛡️ Resultado:** Confianza para innovar sin miedo a errores irreversibles