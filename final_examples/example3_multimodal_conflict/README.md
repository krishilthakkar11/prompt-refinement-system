# Example 3: Multi-Modal with Conflicts

## Description
Demonstrates multi-modal processing with conflicting information across text, image, and document sources.

## Input
Three conflicting sources:
- **Text**: "Build me an app like BookMyShow" (movie booking)
- **Image**: Swiggy food delivery app interface
- **Document**: Smart home automation system requirements (PDF)

## Expected Behavior
- Detect conflicts across all three modalities
- Provide evidence from each source
- Document impact of conflicts
- Source attribution for requirements

## Actual Results
- **Completeness: 0.67**
- **Modalities: text, image, document**
- **Requirements: 1**
- **Conflicts: 1** (with evidence from all three sources)
  - Issue: "Conflicting domains and requirements"
  - Evidence: text (BookMyShow), document (Smart Home), image (food delivery)
  - Impact: "Unclear project scope and objectives"

## What It Shows
- Cross-modal conflict detection (not just pairwise)
- Evidence-based conflict documentation
- Non-resolution approach (flags but doesn't auto-decide)
- Source traceability across modalities
