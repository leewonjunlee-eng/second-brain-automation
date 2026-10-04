import test from 'node:test'
import assert from 'node:assert/strict'
import { kstToday, kstWeek, daysUntil, deadlineState } from '../examples/date.js'
import { parseScheduleWhen, eventOccursOn } from '../examples/schedule-utils.js'

test('KST just before and after midnight', () => {
  assert.equal(kstToday(new Date('2026-02-28T14:59:59Z')), '2026-02-28')
  assert.equal(kstToday(new Date('2026-02-28T15:00:00Z')), '2026-03-01')
})

test('local timezone independence and leap day', () => {
  assert.equal(kstToday(new Date('2024-02-29T00:00:00Z')), '2024-02-29')
  assert.deepEqual(kstWeek(new Date('2026-03-01T00:00:00Z')).map(item => item.iso), ['2026-02-23', '2026-02-24', '2026-02-25', '2026-02-26', '2026-02-27', '2026-02-28', '2026-03-01'])
})

test('Sunday and year crossing', () => {
  assert.deepEqual(kstWeek(new Date('2027-01-03T00:00:00Z')).map(item => item.iso), ['2026-12-28', '2026-12-29', '2026-12-30', '2026-12-31', '2027-01-01', '2027-01-02', '2027-01-03'])
})

test('deadline states', () => {
  assert.equal(daysUntil('2026-10-05', '2026-10-04'), 1)
  assert.equal(deadlineState('2026-10-04', '2026-10-04'), 'today')
  assert.equal(deadlineState('2026-10-01', '2026-10-04'), 'overdue')
})

test('valid schedule forms', () => {
  assert.equal(parseScheduleWhen('17:00', '2026-10-01').all_day, false)
  assert.equal(parseScheduleWhen('2~3일', '2026-10-01').date, '2026-10-02')
  assert.equal(parseScheduleWhen('2/28 10:00', '2026-10-01').date, '2026-02-28')
})

test('invalid hour, day, reversed range, and unsupported form', () => {
  assert.throws(() => parseScheduleWhen('24:00', '2026-10-01'))
  assert.throws(() => parseScheduleWhen('2/31 10:00', '2026-10-01'))
  assert.throws(() => parseScheduleWhen('3~2일', '2026-10-01'))
  assert.throws(() => parseScheduleWhen('next week', '2026-10-01'))
})

test('occurrence includes endpoints and excludes outside dates', () => {
  const event = { date: '2026-10-02', end_date: '2026-10-03' }
  assert.equal(eventOccursOn(event, '2026-10-02'), true)
  assert.equal(eventOccursOn(event, '2026-10-03'), true)
  assert.equal(eventOccursOn(event, '2026-10-01'), false)
  assert.equal(eventOccursOn(event, '2026-10-04'), false)
})
