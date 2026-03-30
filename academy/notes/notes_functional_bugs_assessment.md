# Functional Bugs: Assessment and Severity Notes

## Definition
Bugs related to the functionality of a piece of software (action-response failure).
- **Examples:** Button doesn’t submit, search doesn’t react, app crashes.

## Identification Strategy
- **Education Guesses:** Analyze product behavior by testing different scenarios.
- **Evidence:** Provide proof that something is not working as intended (e.g., field validated in some cases but not others).
- **Consistently Identical Behavior:** If a feature consistently works the same way without obvious problems, it is likely intended (Usability Suggestion).
- **Upgrade from Visual/Content:** If a visual or content problem hinders functionality, report it as a functional bug.

## Severity Assessment Factors
- **Functional Impact:** How relevant is the functionality to the whole product?
- **Extent:** How many users, products, or items are affected?
- **Workarounds:** Is there an intuitive/easy alternative route? (Showstopper = No workaround for core functionality).
- **Potential Loss of Sales:** Financial impact on the customer.
- **Comparison:** Compare to previously approved bugs in the same test.

## Severity Levels
### LOW
- Minimal impact on usage.
- Few users/items concerned.
- Broken feature has an easy workaround.
### HIGH
- Serious impact, but main functionality is intact.
- Large number of users/items concerned.
- Non-trivial functionality broken with no workaround.
- Important functionality broken but workaround exists.
### CRITICAL
- Prevents core functionality (Showstopper in main process like checkout).
- Potential and notable loss of sales.

## Special Categories
- **Edge Case Bugs:** Occur via unusual/uncommon sets of actions. Forwarded as **Low** if relevant; otherwise rejected.
- **Forced Bugs:** Generally **OUT OF SCOPE**. Caused by non-typical behavior (e.g., tapping multiple elements at once, fast-paced clicking, full RAM, modified OS).
