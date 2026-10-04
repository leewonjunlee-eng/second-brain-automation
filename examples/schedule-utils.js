const ISO = /^(\d{4})-(\d{2})-(\d{2})$/
const TIME = /^([01]\d|2[0-3]):([0-5]\d)$/

function dateParts(value) {
  const match = String(value || '').match(ISO)
  if (!match) throw Error('기준 날짜가 올바르지 않다.')
  return { year: Number(match[1]), month: Number(match[2]), day: Number(match[3]) }
}

function valid(year, month, day) {
  const date = new Date(year, month - 1, day)
  if (date.getFullYear() !== year || date.getMonth() !== month - 1 || date.getDate() !== day) {
    throw Error('올바른 날짜를 입력해야 한다.')
  }
  return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`
}

export function parseScheduleWhen(value, contextDate) {
  const input = String(value || '').trim().replace(/[～–—]/g, '~')
  const context = dateParts(contextDate)
  if (TIME.test(input)) return { date: contextDate, end_date: contextDate, time: input, all_day: false }

  let match = input.match(/^(\d{1,2})\s*~\s*(\d{1,2})일$/)
  if (match) {
    const start = valid(context.year, context.month, Number(match[1]))
    const end = valid(context.year, context.month, Number(match[2]))
    if (end < start) throw Error('종료일은 시작일보다 빠를 수 없다.')
    return { date: start, end_date: end, time: '', all_day: true }
  }

  match = input.match(/^(\d{1,2})일$/)
  if (match) {
    const date = valid(context.year, context.month, Number(match[1]))
    return { date, end_date: date, time: '', all_day: true }
  }

  match = input.match(/^(\d{1,2})\/(\d{1,2})\s+([0-2]\d:[0-5]\d)$/)
  if (match && TIME.test(match[3])) {
    const date = valid(context.year, Number(match[1]), Number(match[2]))
    return { date, end_date: date, time: match[3], all_day: false }
  }
  throw Error('지원하지 않는 일시다.')
}

export function eventOccursOn(event, day) {
  const end = String(event?.end_date || event?.date || '')
  return Boolean(ISO.test(day) && String(event?.date || '') <= day && day <= end)
}
