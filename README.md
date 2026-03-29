# Test.io Account and Gig Work Management

This project is dedicated to managing Test.io account details, academy progress, and active testing cycles using a directive-based CLI agent.

## Directory Structure

```text
/srv/test.io/
├── .agents/                 # Internal YAML logic and global identity
├── bin/                     # Gemini CLI executable/scripts
├── workspace/               # Active Testing Area
│   ├── current_cycle/       # Files for the specific test cycle
│   └── scratchpad.md        # Quick notes and observations
├── evidence/                # Raw Data Acquisition (The "Dirty" Folder)
│   ├── recordings/          # Screen captures from i3wm
│   ├── logs/                # Terminal outputs, dmesg, journalctl
│   └── screenshots/         # Captured visual bugs
├── reports/                 # Processed Submissions (The "Clean" Folder)
│   ├── drafts/              # YAML-based bug reports in progress
│   └── submitted/           # Archived Markdown files sent to Test IO
├── academy/                 # Learning & Certification
│   └── notes/               # Course-specific documentation and quiz prep
├── docs/                    # Personal Standards
│   └── reproduction_checklist.md # "Golden Path" for verifying bugs
└── README.md                # Project overview and directory map
```

### Module Descriptions

- **.agents/**: Contains the core configuration and modular logic that drives the AI assistant.
- **bin/**: Custom scripts and binary tools specifically for this environment.
- **workspace/**: The primary staging area for active testing work.
- **evidence/**: A repository for raw, unedited proof (logs, videos, images).
- **reports/**: Where bug reports are drafted in YAML and archived in Markdown.
- **academy/**: A central repository for study materials and progress tracking.
- **docs/**: Standard operating procedures and checklists to ensure quality.
