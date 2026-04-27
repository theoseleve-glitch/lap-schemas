"""T173 — coach session note shapes.

Backs `POST /api/v1/sessions/:id/coach-notes` — a coach (or org
admin) attaches a free-text note to a driver's session. Used by
the coach/team for offline review feedback ("watch your apex on
turn 4 next time"); the driver sees these in their session
detail view.

Bounds:
  - `body` ∈ [1, 5000] chars: empty rejected (a blank note is
    UI-noise — silently ignore? no, surface as 422 so the coach
    knows their input was rejected); 5000 is generous for a
    qualitative review note without becoming a doc-dumping ground

Authoring identity (`author_user_id`) is captured on the server
side — the client doesn't supply it. Multiple notes per session
are allowed (a coach can leave several observations during one
review session, or different coaches can each leave one).

The note is org-scoped indirectly: the endpoint validates that
the calling user shares an org with the session's driver before
allowing the write. No FK to Organization on the note row
itself — a driver may belong to multiple orgs and the note's
"context" is the coach<->driver relationship that the auth
check enforces. Cross-org leakage is prevented at the endpoint,
not the schema.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from lap_schemas.v1.ids import UUID7


class CoachSessionNoteCreate(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    body: str = Field(min_length=1, max_length=5000)


class CoachSessionNote(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID7
    session_id: UUID7
    # Nullable post-author-deletion: the ORM uses ON DELETE SET
    # NULL on author_user_id so the note row survives a user
    # purge (review history is preserved). At creation time the
    # value is always set; only later listings can carry None.
    author_user_id: UUID7 | None = None
    body: str
    created_at: datetime
