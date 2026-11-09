/**
 * Format a date in a time zone.
 * @param {Date} date
 * @param {string} [timeZone] IANA time zone; defaults to the runtime's local time zone.
 */
export function formatDate(date, timeZone) {
  return new Intl.DateTimeFormat("en-GB", {
    year: "numeric", month: "short", day: "2-digit",
    timeZone,
  }).format(date);
}
