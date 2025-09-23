
import pandas as pd
import re
from typing import Iterable, List

EXCLUDE_KEYWORDS = [
    'region','регион','grade','класс',
    'total','итог','sum','сумма','overall','общий',
    'fio','name','фамилия','имя','отчество','id','uid'
]

TASK_PATTERNS = [
    r'^task\\s*\\d+$',
    r'^q\\s*\\d+$',
    r'^question\\s*\\d+$',
    r'^t\\s*\\d+$',
    r'^\\d+$',
    r'задач\\w*\\s*\\d+$',   # Задача 1, Задачи 2
    r'вопрос\\w*\\s*\\d+$'   # Вопрос 1
]

def normalize_region(s: str) -> str:
    if not isinstance(s, str):
        return ''
    return s.strip().lower()

def to_region_group(region_raw: str, mo_synonyms: Iterable[str]) -> str:
    r = normalize_region(region_raw)
    for syn in mo_synonyms:
        if syn in r:
            return 'MO'
    return 'Rest'

def _find_region_col(df: pd.DataFrame) -> str:
    # ищем колонку с регионом
    for c in df.columns:
        lc = str(c).lower()
        if 'region' in lc or 'регион' in lc:
            return c
    # если не нашли — пробуем популярные варианты
    for cand in ['Регион','region','Region','Субъект','субъект']:
        if cand in df.columns: return cand
    raise ValueError("Не нашёл колонку региона. Переименуй её в 'region' или 'Регион'.")

def _detect_task_cols(df: pd.DataFrame, task_prefix: str, task_count: int) -> List[str]:
    # 1) явный префикс task1..taskK
    task_cols = [c for c in df.columns if str(c).lower().startswith(task_prefix)]
    if task_cols:
        return task_cols

    # 2) регулярки по часто встречающимся паттернам
    pats = [re.compile(p, flags=re.IGNORECASE) for p in TASK_PATTERNS]
    by_regex = [c for c in df.columns if any(p.match(str(c).strip()) for p in pats)]
    if by_regex:
        return by_regex

    # 3) все числовые столбцы, кроме служебных
    num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    def _is_excluded(col: str) -> bool:
        lc = str(col).lower()
        return any(k in lc for k in EXCLUDE_KEYWORDS)
    auto = [c for c in num_cols if not _is_excluded(c)]

    # safety: требуем хотя бы 3 столбца-«задачи», иначе лучше упасть с подсказкой
    if len(auto) >= 3:
        return auto

    raise ValueError(
        "No task columns found.\n"
        "Что делать: либо переименуй задачи в понятный формат (напр. 'Task 1'),\n"
        "либо укажи явные названия колонок задач (я добавлю поддержку списка в config при необходимости).\n"
        f"Колонки в таблице: {list(df.columns)}"
    )

def clean_and_tidy(df: pd.DataFrame, mo_synonyms, task_prefix='task', task_count=10) -> pd.DataFrame:
    region_col = _find_region_col(df)
    task_cols = _detect_task_cols(df, task_prefix, task_count)

    core = df[[region_col, 'grade'] + task_cols].copy()
    core['region_group'] = core[region_col].apply(lambda x: to_region_group(x, mo_synonyms))

    tidy_rows = []
    for _, row in core.iterrows():
        for t in task_cols:
            tidy_rows.append({
                'grade': row['grade'],
                'region_group': row['region_group'],
                'task_id': str(t),
                'score': row[t]
            })
    tidy = pd.DataFrame(tidy_rows).dropna(subset=['score'])
    return tidy
