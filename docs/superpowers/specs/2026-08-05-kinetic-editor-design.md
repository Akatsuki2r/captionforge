# Design Spec: Kinetic Editor for CaptionForge

## Overview
The Kinetic Editor is a visual, timeline-based interface for CaptionForge that replaces the static table. It enables precise, high-end subtitle timing and kinetic word-level styling (highlighting) for high-retention content creation.

## Key Features
1. **Visual Timeline**: A `QWidget` drawing the audio waveform, with subtitle segments rendered as draggable/resizable rectangles.
2. **Kinetic Highlighting**: Right-click context menu on a word in a caption to toggle kinetic styles (`[HIGHLIGHT]`).
3. **Preset Styles**: 3 pre-baked visual motion presets applied to the exported ASS output.

## Technical Approach
### Timeline Component (`src/ui/timeline_editor.py`)
- Custom `QWidget` using `QPainter` to draw:
  - Audio waveform (using `librosa` or `wave` to get amplitude data).
  - Subtitle blocks (rectangles) keyed by start/end time.
- Interaction logic:
  - Drag to move blocks (slip-editing).
  - Resize handles for start/end points.
  - Context menu for kinetic styling.

### Word-Level Highlighting (`src/services/subtitle_service.py`)
- Update `export_ass` to parse `[HIGHLIGHT]` tags in the text and inject ASS override codes (e.g., `{\c&H0000FF&}`) for specific words.

### Motion Presets
- Hardcoded ASS template configurations mapped to "Preset 1", "Preset 2", "Preset 3" in the UI.

## Data Flow
- `MainWindow` holds the `SubtitleService` data model.
- `TimelineEditor` observes/renders this model.
- Editing actions (drag/drop/click) update the model and signal the `MainWindow` to re-sync.
- Final export triggers the updated `export_ass` with kinetic tag parsing.

## Testing Strategy
- Unit tests for `SubtitleService` tag parsing.
- UI tests for timeline drag-and-drop constraints.

---
*Status: Draft for Review.*
