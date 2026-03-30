# Bug Reproductions Notes

## Definition
Reproductions allow testers to verify if a bug reported by someone else also occurs on their own device. They help customers determine if an issue is device-specific and assess its overall severity.

## Types
- **Positive Reproduction:** You experience the exact same bug using the same steps.
- **Negative Reproduction:** The function works correctly on your device (no bug found).
- **Important:** If you find a *different* bug, submit a new bug report instead of a reproduction.

## Reproduction Session
- **Duration:** 30 minutes to submit the report after clicking "Start reproduction".
- **Seat Reservation:** Your seat is held for the 30-minute window. If you don't submit or you cancel, the seat becomes available to others.

## Attachment Rules
- **Screencast:** Mandatory for all reproductions.
- **Duration:** Maximum 15 seconds (rare exceptions up to the length of the original tester's screencast).
- **Visibility:** Must show the current date and the URL bar (for website tests).
- **App Crashes:** Upload both a crash log and a coherent screencast.
- **Compliance:** All standard Bug Report Attachment rules apply. Non-compliance results in rejection.
- **Out of Scope (OOS):** Reproducing OOS bugs (e.g., live orders) leads to rejection and a warning.

## Concurrency and Visibility
- **One Task at a Time:** You cannot run reproductions simultaneously with Test Cases, Test Sessions, or Bug Fix/Report Confirmations.
- **Button Visibility:** "Start reproduction" appears for running tests, unreviewed functional bugs, and if reproduction slots are still available.
