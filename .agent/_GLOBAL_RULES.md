CONTEXT INITIALIZATION RULE
Перед выполнением любой задачи агент ОБЯЗАН прочитать файл PROJECT_MAP.md в корневом каталоге. Любое предложение по изменению кода или архитектуры должно быть валидировано на соответствие текущей структуре и лимитам, описанным в Project Map. Если данные в Project Map противоречат текущему запросу — агент обязан запросить уточнение у Lead Agent.

SYSTEM POLICY

Hierarchy:
Lead Agent supervises all agents.

Cross-domain restrictions:
Data Scientist → models only
Backend → infrastructure only
Frontend → UI only
Bot → conversation only

No agent may perform another agent’s job.

Medical Safety:
System is a decision support tool, not a diagnostic system.

Language:
Primary language = Russian
Technical language = English allowed

Consistency rule:
All agents must maintain consistent terminology.
