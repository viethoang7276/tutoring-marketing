---
name: edlintics-concept-carousel
description: Build an Edlintics Instagram concept carousel (Definition or This vs That) from the saved templates in Canva or Claude Design, reusing or generating on-brand action illustrations. Use for any Tue/Thu/Sat concept post or a weekly design batch.
---

# Edlintics concept carousel

Build one finished carousel draft per concept, for European CFA/ACCA and business students. Always start from a template copy and fill its placeholders. Never draw a layout from scratch, and never overwrite a template.

## Approval gates (always)
- Content approval, design approval and permission to publish are separate. Build designs only for posts whose content (caption and first comment included) is approved on the Content Desk.
- Keep every edit transaction open (`finalize: keep_open`). Send a preview sheet and ask before you `commit`.
- Never publish, schedule or post, and never create recurring jobs, unless Hoang explicitly authorises it.
- A timeout is not proof that nothing happened. Re-read the design before retrying.

## Templates (copy, never edit the original)
| Format | Canva template | Claude Design artboards (canvas "Edlintics Post Templates") |
|---|---|---|
| Definition | DAHYuPFDiDU | Main (cover), DefTree, DefIdea, Cta |
| This vs That | DAHYuGf21MI | VsCover, VsCompare, Cta |
| Puzzle | DAHYuGZYL_E | PuzQ, PuzA, Cta (follow the edlintics-puzzle-visuals skill) |

Claude Design canvas: https://claude.ai/artifact/7yg3KS9LosoEoZEqEP2GAp. It is a replica of the Canva templates (same positions, sizes and colours). Its fonts are Source Serif 4 and Inter, standing in for the Canva brand fonts. Posts sit in a "Posts" row under the templates, as copies of the template artboards with the content filled in.

The gold-standard samples are DAHYuQbDjXA (Definition, Opportunity cost) and DAHYubD8sQY (This vs That, Markup vs margin).

## Definition format: 8 pages, in this order
1. **Cover:** "[Term] is ——". The line continues onto page 2.
2. **Fan tree:** the term with the 5 idea titles as branches.
3. **Idea 1**
4. **Idea 2**
5. **Idea 3**
6. **CTA, mid-carousel.** Logo, "Learn business concepts the clear way", "Visit www.edlintics.com", the "Comment 'Learn' and we will send you a free course" bubble, and the desk illustration. In the top right, the swipe cue: "Swipe for 2 more ideas" (bold 28px #2960C7, aligned to the end, at about left 560, top 52, width 366), next to a 64px #2960C7 circle at 944,40 holding a white arrow. The arrow is the path `M2 10H14V5L22 12L14 19V14H2Z` in a 24×24 viewBox, drawn at 32px at 960,56.
7. **Idea 4**
8. **Idea 5.** The footer reads "Save this for your next exam", not "Swipe for the next idea".

In Canva the template has a single idea page and the CTA at the end, so:
1. Copy the whole design (copy-design fails when `page_numbers` has duplicates).
2. Add pages with `merge-designs insert_pages`.
3. Move the CTA after idea 3 with `reorder_page`.

### Idea page layout (1080×1350)
- **Kicker:** "[TERM] · N OF 5" at top 88, grey, 26px, bold.
- **Title:** "N. Short title" at top 146, serif 68px. It must fit on one line, so about 26 characters at most.
- **Body:** at top 296, 42px, 3 lines at most, one plain-language explanation.
- **Example:** starts with "Example:" and uses a concrete US dollar ($) scenario, 3 lines at most. Place it at about top 494 when the body runs to 3 lines, or 466 when it runs to 2.
- **Illustration:** delete the old diagram first, then `insert_fill` at top 680, left 88, 640×360.
- **Template elements:** the Sigma mascot (bottom right) and the footer come with the template.

### Copy rules
- Short sentences, everyday words, one idea per page.
- Examples use real numbers. Check the arithmetic.
- The 5 ideas build on each other: what it is, how to count it, where it hides, what it is not, how it is used.

## This vs That format: 3 pages
1. **Cover:** "[THIS] VS [THAT]".
2. **Comparison page:**
   - Two cards. Each has a name, a one-line rule, a worked example (both sides use the same numbers), and a USED FOR section with 2 items.
   - Six icon frames. Fill them with `update_fill`.
3. **CTA**

## Graphics: reuse first, generate only when nothing fits
**Library:**
- Canva folder: **Edlintics · Brand graphics** (FAHYugebSqU).
- Catalog: the project doc `claude/brand-graphics.md`, with a repo copy at `docs/content-workflow/brand-graphics.md`.

For every image placeholder:
1. **Search the catalog** by concept and tags. If a match fits (same idea, right kind: a 16:9 illustration for idea pages, a square icon for small frames), reuse it by media ID.
2. **If nothing fits**, generate a new image:
   - Run `mcp__Canva__generate-image`, then `get-generate-image-job` to get the media ID.
   - Look at the result.
   - Regenerate it if it has text, off-brand colours or a mismatched style.
3. **File every new image straight away:**
   - Move it into the folder: `move-item-to-folder`, with the media ID as item_id and to_folder_id `FAHYugebSqU`.
   - Add a row to the catalog: `project_read`, append the row, `project_write`. Write all the rows once at the end of a run.
4. Never put the old mascot characters into image placeholders.

The images are flat, not true vectors, because uploading SVGs to Canva is blocked by the proxy.

Canva exports can't be downloaded into the cloud workspace or onto the Mac (the proxy blocks them). So in Claude Design, raster illustrations stay as labelled placeholders until Hoang drops them in. Diagrams are drawn as HTML/SVG, which is real vector.

**Prompt for idea illustrations:**
> Flat vector illustration, clean simple shapes, friendly cartoon style, white background, limited palette: royal blue #2960C7, navy #0D1523, light blue #C9D8F5, warm gold #C2922F accents. [person + ACTION that shows the idea]. No text, no letters, no logos.

**Prompt for icons:**
> Flat vector icon, single centered object, white background, royal blue #2960C7, navy #0D1523 outlines, light blue fill, small gold #C2922F accent, friendly and simple, no text. [object + action]

## Weekly design batch
Use this when Hoang says "build the week", or after he approves content.
1. Read the Content Desk (https://claude.ai/artifact/RV9TtccfdAkHVQX3zpkv61) with ArtifactData. Collect next week's posts whose content approval is current and whose design hasn't been built.
2. Plan every graphic first. Resolve reuse from the catalog in one pass, and list only the images that must be generated.
3. Start all the image jobs together. Then build the posts one design at a time, with transactions kept open.
4. File the new graphics and update the catalog once.
5. Send one preview sheet for the week, labelled by post ID. Ask once whether to save all, some or none, and commit only what's approved.
6. Write each design ID and edit URL back onto its post, with status `awaiting_design_approval`. Do not schedule anything.

## Brand tokens
- **Colours:** ink #0D1523, blue #2960C7, tints #C9D8F5 and #E8EEFB, grey #5B6475, gold #C2922F, paper #FBFAF6.
- **Fonts:** in Canva, serif titles use fontRef YACgEfdj394. Font placeholders are fine, because Hoang fixes fonts in Canva.
- **Logo:** Canva asset MAHYcDuPL7o. On the Claude Design canvas it is the blob `/_blob/9b018dea4aba534b6ce07619209632fb`.

## Canva edit-design notes
- **Reading:** `read-design` with `open_transaction: true`, `fields: ["design_content"]`, and a `page_indices` filter. A read without a transaction returns text only.
- **Editing:** one page per call. Check the returned thumbnail before moving on.
- **`insert_shape`** takes `path`, `view_box_width`, `view_box_height`, `color` and `corner_rounding`.
- **`add_text`** adds 16px black text, so follow it with `format_text` (a second call, using the new IDs).
- **Saving:** commit only after approval, with `finalize: commit` and no operations. Cancel read-only transactions.
- **Naming:** "SAMPLE · [Format] · [Term]" for samples, "[date time] · [Format] · [Term]" for real posts.
