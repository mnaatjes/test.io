# Bug Report Standards Notes

## Quick Summary
- **Severity:** Mandatory for functional bugs (select BEFORE filling the report).
- **Title:** Use the formula **What? + Where? + When?** Describe what happened, not what didn't happen.
- **URL:** Valid link copied directly from the browser.
- **Steps to Reproduce:**
  - 1st step: Access landing page URL or open mobile app (with name).
  - Middle steps: Separate user actions.
  - Last step: The action that triggers the bug (must NOT be "Observe").
- **Actual Result:** Detailed explanation of what happened. Must NOT be the same as the title or the simple opposite of the expected result.
- **Expected Result:** Clear description of correct behavior. Must NOT be a minor negative variation of the actual result.
- **Environment:** Must match the exact device/browser from your invitation list.

## Writing a Great Title
- Put yourself in the shoes of someone who has never tested the app.
- Answer: What is the bug? Where did it happen? When is it triggered?
- Avoid generic phrases like "does not work".
- **Example:** `"Checkout" button from the Cart page navigates users to an "Error 500" page`.

## Steps to Reproduce Rules
- Numbering is handled automatically.
- Keep steps general unless the bug is data-specific.
- Use the minimum number of steps necessary.

## Professionalism and Edits
- **No Placeholders:** Reports must be complete when submitted.
- **Realistic Inputs:** Avoid random characters (e.g., use "Michael" instead of "asdfg").

## The "AI-Proofing" Rules (Strict Enforcement)
1. **Step 1 is ALWAYS the URL:** Do not say "Access landing page." Use `1. Open https://...`
2. **Steps = Actions ONLY:** No "Notes," "Observations," or "Results" allowed in steps. If you can't click it, don't write it.
3. **One Bug Per Report:** Never report two different components (e.g., Detail Page vs. Quickview) in one report.
4. **No Speculation:** Never say "I think," "Maybe," or "Customers will be confused." Stick to visible UI facts.
5. **The Title Formula:** `[Action/Bug] + [Location] + [Trigger]` (e.g., "Quantity skips 1 to 3 on Details Page when clicking +").
