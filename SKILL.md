---
name: 968-adventure-portfolio-builder
description: Build or evolve a premium personal adventure portfolio website that combines amateur radio, drone photography, fine-art print sales, 4x4 overlanding, and community/service storytelling. Use when creating or updating a similar multi-hobby portfolio, especially when user-provided photos, watermarked galleries, expedition journals, or iterative WebDev edits are involved.
---

# 968 Adventure Portfolio Builder

## Overview

Use this skill to turn a personal, multi-disciplinary identity into a cohesive, cinematic portfolio website. The default expression is a field-journal aesthetic: deep navy, sand, signal orange, editorial serif headlines, compact mono labels, generous whitespace, subtle grain, and restrained motion.

## Workflow

1. **Understand the person and the site job.** Identify the core disciplines, location, credentials, equipment, audience, desired action, and whether the site is a portfolio, print storefront, journal, or service profile. Never invent personal equipment, certifications, prices, dates, or experiences; use clearly labeled placeholders only when the user agrees.
2. **Research visual references.** For requests that mention searching the web, use the web-research route and gather references for landscapes, field operations, and editorial photography. Prefer original or user-provided assets in the final website; do not copy third-party images into a commercial gallery without permission.
3. **Choose the visual system.** Declare a specific design direction before coding. Pair a display serif with a readable sans and mono metadata. Use an asymmetric editorial layout instead of generic centered cards. Design dark hero and field sections against warm paper/sand content sections.
4. **Initialize the WebDev project.** For a portfolio or static storefront, use the WebDev `web-static` scaffold. Read the static WebDev guidance first. Keep media outside `client/public` and `client/src/assets`; upload final assets with `manus-upload-file --webdev` and reference the returned `/manus-storage/...` path.
5. **Create or ingest visual assets.** Generate original hero/section visuals when the user has no assets. When a user supplies a portrait, vehicle, shack, or expedition photo, upload it and use it as the primary visual in the corresponding section. Preserve identity and the important objects in image edits.
6. **Compose the information architecture.** A strong default order is:
   - hero: location, one-line thesis, call sign/credential stats;
   - story: 3–4 pillars such as Signal, Frame, Range, Service;
   - drone field notes: experience, kit, workflow, landscape philosophy;
   - station operations: radio modes, QSL information, shack equipment;
   - 4x4 range: vehicle, modifications, recovery, rescue, convoy ethos;
   - route journal: dated expeditions and incidents;
   - print room: watermarked preview, title, location/category, edition, price, request CTA;
   - contact/community close.
7. **Protect preview images honestly.** Add visible coordinate/call-sign watermark overlays, low-resolution preview language, `draggable=false`, image drag prevention, and a context-menu deterrent. State clearly that front-end deterrents cannot prevent screenshots, screen photography, or developer-tools access. For real protection, propose authenticated/server-side delivery and signed URLs.
8. **Use real interactions.** Include anchor navigation, mobile menu, gallery filtering, carousel controls, request-print feedback, and keyboard-reachable buttons. Use `sonner` for staged actions. Keep payment or licensing flows as a clear request/placeholder unless a backend/payment integration is actually enabled.
9. **Add user-supplied details in structured form.** For equipment, show model, role/specification, and upgrade date only when known. For route journals, show date/status, route or region, objective, conditions, recovery lesson, and photo. For uncertain facts, use “Add details” or an editable data structure rather than guessing.
10. **Validate before delivery.** Run `pnpm check` and `pnpm build`. Capture a desktop and mobile preview; use a full-page capture for long editorial pages. Fix only concrete runtime, content, or layout defects. Save one checkpoint after the feature set is complete and deliver its `manus-webdev://...` link.

## Reusable Content Patterns

### Vehicle modification log

Use an editable array with fields:

```ts
{ category: "Suspension", item: "[user-provided upgrade]", specification: "[spec or purpose]", date: "[YYYY or month YYYY]" }
```

Group entries by suspension, tires/wheels, protection, recovery, communications, navigation, power, and storage. If the user has not supplied a value, display “Details to add” rather than fabricating it.

### Route journal

Use an array with fields:

```ts
{ date: "[date]", route: "[region / expedition]", status: "Expedition" | "Recovery", summary: "[short account]", lesson: "[practical takeaway]", image: "[storage path]" }
```

Make the journal scannable with a vertical timeline or horizontal cards. Include rescue and recovery experiences as operational learning, not as exaggerated claims.

### Image carousel

Implement a controlled carousel with:

- previous/next buttons with accessible labels;
- dot or thumbnail indicators;
- keyboard reachability;
- `aria-live` for the active slide title;
- one large protected image using the same `Watermark` overlay as the print gallery;
- caption, route/date, and a “recovery” or “expedition” tag;
- no autoplay by default; if autoplay is requested, pause on hover/focus and respect reduced motion.

Use the existing shadcn carousel only if it is quicker and remains visually consistent; otherwise use a small local state machine with `useState` and an array of slides.

### ADIF Recent QSOs updater

For static radio pages, bundle a deterministic parser at `scripts/update_recent_qsos.py` that reads an ADIF export and writes a small JSON file imported by the React page. Parse `QSO_DATE`, `TIME_ON`, `CALL`, `BAND`, `MODE`, and RST fields when present; sort newest first; preserve blank values as empty strings; and never invent contact records. Render an explicit empty state when the JSON array is empty. Keep the generated JSON in the site’s source tree only when the operator intentionally publishes it.

### DXpedition and contest calendar

Add a compact, source-linked calendar section to the amateur-radio page with `type`, `title`, `date`, `focus`, and `source` fields. Prefer official contest calendars and recognized DX calendars, show a “verify before operating” note for time-sensitive activity, and distinguish public event information from the operator’s own confirmed plans. Use responsive cards or a small table rather than an unbounded feed.

### System-prompt configuration

Use `templates/system-prompt-config.yaml` as the reusable prompt configuration. It contains one portfolio-builder system prompt and one amateur-radio logbook/DX-planning system prompt, plus conservative runtime defaults for A41DA, Oman, Asia/Muscat, source-linked calendars, and logbook privacy. Adapt the callsign and locale only when the operator supplies different values.

## Quality Guardrails

- Keep the page visually authored: avoid generic dashboard layouts and excessive pills.
- Preserve text contrast over photography with overlays or solid panels.
- Keep animations under 300ms for controls and respect `prefers-reduced-motion`.
- Do not represent generated visuals as the user’s real equipment or expedition evidence.
- Distinguish “ROAR radio shack” from a private home shack when the user corrects the location.
- Do not promise that right-click disabling makes images impossible to copy; describe it as a deterrent.
- Treat ADIF as operator-owned data: do not publish it automatically without an explicit export/publish step, and show an empty Recent QSOs state when no verified log is supplied.
- Link calendar entries to their source and label DXpedition dates as subject to change.
- Do not edit backend/server code unless the user explicitly asks for secure delivery, authentication, payments, or data persistence; then recommend upgrading from static to a backend-capable scaffold.

## Delivery Checklist

- [ ] User details, credentials, equipment, and locations are accurate.
- [ ] User-provided assets replace placeholders where available.
- [ ] Gallery previews show watermark and price/license context.
- [ ] Carousel and mobile menu work with keyboard-accessible controls.
- [ ] `pnpm check` passes.
- [ ] `pnpm build` passes.
- [ ] Desktop/mobile/full-page previews are visually checked.
- [ ] Final WebDev checkpoint is saved and linked.
