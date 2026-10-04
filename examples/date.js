const KST = new Intl.DateTimeFormat('en-CA', { timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit' })
const KO = new Intl.DateTimeFormat('ko-KR', { timeZone: 'Asia/Seoul', year: 'numeric', month: 'long', day: 'numeric' })

function parts(now) {
  const values = KST.formatToParts(now).filter(part => part.type !== 'literal')
  return Object.fromEntries(values.map(part => [part.type, Number(part.value)]))
}

function iso(value) {
  return `${value.year}-${String(value.month).padStart(2, '0')}-${String(value.day).padStart(2, '0')}`
}

function add(value, days) {
  const date = new Date(Date.UTC(value.year, value.month - 1, value.day + days))
  return { year: date.getUTCFullYear(), month: date.getUTCMonth() + 1, day: date.getUTCDate() }
}

export function kstToday(now = new Date()) {
  return iso(parts(now))
}

export function kstWeek(now = new Date()) {
  const today = parts(now)
  const day = new Date(Date.UTC(today.year, today.month - 1, today.day)).getUTCDay()
  const monday = add(today, day === 0 ? -6 : 1 - day)
  return Array.from({ length: 7 }, (_, index) => {
    const value = add(monday, index)
    return { iso: iso(value), day: value }
  })
}

export function formatKoreanDate(value) {
  if (!value) return ''
  const [year, month, day] = value.split('-').map(Number)
  return KO.format(new Date(Date.UTC(year, month - 1, day)))
}

export function daysUntil(deadline, today = kstToday()) {
  if (!deadline) return 0
  return Math.round((Date.parse(`${deadline}T00:00:00Z`) - Date.parse(`${today}T00:00:00Z`)) / 86400000)
}

export function deadlineState(deadline, today = kstToday()) {
  if (!deadline) return 'none'
  const days = daysUntil(deadline, today)
  if (days < 0) return 'overdue'
  if (days === 0) return 'today'
  if (days === 1) return 'tomorrow'
  return days <= 3 ? 'urgent' : 'normal'
}
