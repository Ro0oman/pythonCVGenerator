# 🧠 Guía de IA Híbrida: Cloud vs Local

Este proyecto soporta tres tipos de "cerebros" para generar tu CV. Puedes alternar entre ellos fácilmente según tus necesidades de privacidad, coste o potencia.

---

## 1. Google Gemini (Cloud - Predeterminado) ☁️
Es la opción recomendada para el mejor resultado narrativo y ATS.
- **Ventajas**: Máxima calidad de redacción, alta velocidad, gran conocimiento de keywords de reclutamiento.
- **Coste**: Gratis (bajo cuota de API de Google) o céntimos (si excedes la cuota).
- **Configuración (`data.json`)**:
  ```json
  "llm_provider": "gemini",
  "model_name": "gemini-3.1-flash-lite-preview"
  ```

---

## 2. Ollama / Llama 3.2 (Local - Privacidad Total) 🏠
Ideal si quieres que tus datos del CV (nombre, email, teléfono) **NUNCA** salgan de tu PC.
- **Ventajas**: 100% Privado, coste $0 forever, funciona sin internet.
- **Requisitos**: Mínimo **6GB de RAM/VRAM**. Tener [Ollama](https://ollama.com/) instalado.
- **Configuración (`data.json`)**:
  ```json
  "llm_provider": "ollama",
  "model_name": "llama3.2"
  ```
- **Instalación**: 
  1. Descarga Ollama de ollama.com.
  2. El script descargará el modelo automáticamente la primera vez.

---

## 3. OpenAI GPT-4o (Cloud - Pago) 💰
Soporte de respaldo (Fallback) por si Gemini falla.
- **Ventajas**: Referencia en el mercado, muy robusto.
- **Coste**: Según uso de tokens en tu cuenta de OpenAI.
- **Configuración (`data.json`)**:
  ```json
  "llm_provider": "openai",
  "model_name": "gpt-4o"
  ```

---

## 🛠️ Cómo cambiar de IA paso a paso
1. Abre el archivo `data.json`.
2. Modifica el campo `"llm_provider"`. Los valores válidos son: `"gemini"`, `"openai"`, `"ollama"`.
3. Si usas `"ollama"`, asegúrate de que la aplicación Ollama esté abierta en tu Windows/Mac.
4. Ejecuta `python main.py`. ¡Listo!

---

## 🎨 Cómo Retocar tu CV (Modo Senior) 🖐️
A veces la IA no elige las palabras exactas que tú usarías. Para esos casos, hemos creado el **Modo Retoque**.

### Paso 1: Genera el CV normalmente
Ejecuta el script como siempre. Al terminar, verás un mensaje que dice:
`✍️ Archivo de retoque guardado: output/.../resume_to_retouch.json`

### Paso 2: Edita el contenido a tu gusto
1. Abre ese archivo `.json` con cualquier editor de texto (Notepad, VS Code).
2. Busca la sección `"optimized_data"` y cambia lo que quieras: el resumen, los bullets de experiencia o tus habilidades.
3. Guarda el archivo.

### Paso 3: Re-genera el PDF instantáneamente
Ejecuta el comando especial de renderizado:
```bash
python main.py --mode render --data output/tu_carpeta/resume_to_retouch.json
```
**¡Listo!** El PDF se generará en milisegundos con tus cambios manuales, sin gastar dinero en la API ni esperar a la IA.

---

> [!TIP]
> **Recomendación Senior**: Usa **Gemini** para generar tu CV inicial y **Llama 3.2 (Local)** para hacer iteraciones rápidas o retoques privados sin preocuparte por los tokens.
