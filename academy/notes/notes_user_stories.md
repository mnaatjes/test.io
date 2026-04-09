# User Story Testing Notes

## Overview
User Stories explain expected behavior from a user's perspective. Your task is to confirm if the story works as intended.

## Reservation Rules
- **Timer:** 30 minutes to finish once reserved.
- **Limit:** Max 3 concurrent reservations.
- **Statuses:**
  - **Reserved:** All slots taken (may open up if others cancel/expire).
  - **Locked:** All executions finished.
  - **Limited:** You have 3 active reservations.

## Execution Outcomes
- **Yes:** Tested thoroughly and works.
- **No:** Does not work. Link a bug report if possible.
- **Not Possible to Test:** Blocked by technical issues (e.g., blank page, missing login).

## Comments
- **Mandatory for:** "No" and "Not Possible to Test".
- **For "Yes":** Use "n/a" if the video is clear; otherwise, add context.
- **Banned Phrases:** "Works as expected", "No issues found".

## Attachments (Screencasts)
- **Length:** Max 15 seconds.
- **Requirements:** Must show URL bar and current Date.
- **Visuals:** Clicks/taps must be visible (Desktop recordings or Android taps).

## Rejections
- Screencast > 15s.
- No Date/URL.
- Clicks not visualized.
- Comment is generic or redundant.
- Wrong status selected (e.g., selecting "No" when it actually works).
