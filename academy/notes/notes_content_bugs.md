# Content Bugs Notes

## Definition
Content bugs relate to the actual content of websites or apps (text, labels, pictures, videos, icons, links, data, etc.).

## Typical Examples
- Broken links or images (404s).
- Defective redirections.
- Missing text (e.g., empty tooltips).
- Missing content/data.
- Missing translations (e.g., French labels on an English site).
- Missing products in search results (if the search function itself works).
- Inconsistent content (e.g., 4/5 icons have tooltips, 1 doesn't).

## Repetitive Problems Rule
- **Policy:** Submit ONLY ONCE even if it occurs on multiple URLs, links, or pages.
- State in the single report that other instances are also concerned.
- **Examples:** Multiple broken product pictures, multiple 404 download links, or multiple missing translations.
- **Rejection:** Individual bug reports for every occurrence will be rejected.

## Functional Upgrade Criteria
- **Upgrade:** Report as functional if the content bug PREVENTS functionality.
- **Navigation Components:** Linking problems in the navigation menu, header, footer, or breadcrumb navigation (e.g., a "COVID-19 Dashboard" link in the header failing) are typically **LOW** functional bugs.
- **Exception:** It remains a content problem if the functionality is easily/intuitively reachable via a different path or option.

## Documentation
- **Screenshots:** Mandatory for all content reports.

## Out of Scope
- Spelling problems (typos).
- Dummy text or missing content on staging environments (often intentional).

## Image Guide
- **Broken Images:** Fail to load (error icon, blank space). Caused by incorrect URLs, server issues, or corruption.
- **Placeholder Images:** Intentionally used temporary representations (geometric shapes, solid colors, icons). **NOT a bug.**
