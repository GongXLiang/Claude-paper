import { test } from "node:test";
import assert from "node:assert/strict";
import { formatDate } from "./format.mjs";

// Instants near midnight UTC, so the calendar day depends on the time zone.
const LATE_UTC = new Date("2026-11-09T23:30:00Z"); // Shanghai (UTC+8): 10 Nov
const EARLY_UTC = new Date("2026-11-10T02:00:00Z"); // New York (UTC-5): 9 Nov

// Runs fn with the process's local time zone set to tz. Node applies
// process.env.TZ assignments at runtime, but on Windows deleting TZ does not
// re-detect the system zone, so the original zone is reassigned first.
function withLocalTimeZone(tz, fn) {
  const savedEnv = process.env.TZ;
  const savedZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  process.env.TZ = tz;
  try {
    fn();
  } finally {
    process.env.TZ = savedEnv ?? savedZone;
    if (savedEnv === undefined) delete process.env.TZ;
  }
}

test("formats an explicit UTC date", () => {
  assert.equal(formatDate(new Date("2026-11-09T23:30:00Z"), "UTC"), "09 Nov 2026");
});

test("defaults to the local time zone", () => {
  withLocalTimeZone("Asia/Shanghai", () => {
    assert.equal(formatDate(LATE_UTC), "10 Nov 2026");
  });
  withLocalTimeZone("America/New_York", () => {
    assert.equal(formatDate(EARLY_UTC), "09 Nov 2026");
  });
});

test("an explicit time zone overrides the local one", () => {
  withLocalTimeZone("Asia/Shanghai", () => {
    assert.equal(formatDate(LATE_UTC, "UTC"), "09 Nov 2026");
  });
});

test("explicit time zones cross the UTC day boundary", () => {
  assert.equal(formatDate(LATE_UTC, "Asia/Shanghai"), "10 Nov 2026");
  assert.equal(formatDate(EARLY_UTC, "UTC"), "10 Nov 2026");
  assert.equal(formatDate(EARLY_UTC, "America/New_York"), "09 Nov 2026");
});
