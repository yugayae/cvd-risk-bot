# Модульная структура frontend

## 📁 Структура модулей

```
frontend/js/
├── constants.js              # Все константы и тексты
├── validation.js             # Валидация данных
├── api.js                    # API запросы
├── utils/
│   ├── normalization.js      # Нормализация данных
│   ├── interpretation.js    # Генерация интерпретаций
│   ├── form-handlers.js     # Обработчики формы
│   └── warnings.js          # Правила предупреждений
└── render/
    ├── patient-report.js    # Рендеринг отчета для пациента
    └── doctor-report.js     # Рендеринг отчета для врача
```

## 🔄 Миграция

Для использования модульной структуры:

1. **Вариант 1: ES6 модули (рекомендуется)**
   - Использовать `<script type="module">` в HTML
   - Требует сервер (не работает с file://)

2. **Вариант 2: Bundler (Webpack/Vite)**
   - Собрать все модули в один файл
   - Работает везде

3. **Вариант 3: Постепенная миграция**
   - Оставить текущий script.js
   - Постепенно переносить функции в модули
   - Использовать модули там, где возможно

## 📝 Использование

### Пример импорта:

```javascript
// main.js
import { validatePatientData } from './js/validation.js';
import { fetchPrediction } from './js/api.js';
import { renderPatientResult } from './js/render/patient-report.js';
import { normalizePrediction } from './js/utils/normalization.js';
```

### Пример использования:

```javascript
// В обработчике формы
const payload = collectFormData(form, currentLang);
const normalized = normalizePayload(payload);
const validation = validatePatientData(normalized);

if (validation.isValid) {
    const raw = await fetchPrediction(normalized);
    const data = normalizePrediction(raw);
    renderPatientResult(data, currentLang, validation, PATIENT_LABELS);
}
```

## ⚠️ Важно

- Все модули используют ES6 синтаксис
- Для работы в браузере нужен сервер или bundler
- Константы нужно будет экспортировать из constants.js
- Текущий script.js продолжает работать независимо


