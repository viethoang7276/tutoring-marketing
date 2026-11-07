---
name: edlintics-meta-ads-setup
description: Set up, rebuild or repair an Edlintics Meta ad campaign through the meta-ads MCP so it passes Meta's rules first time. Covers the delivery-goal rule, the price vs no-price test split, the Development-mode block on new creatives, placements, AI extras, checks and the publish gate. Use when ads show an error, stay on "Preparing", or a campaign must be created or duplicated. Learned 5 Nov 2026.
---

# Meta ads setup

Account `535582635765592` (currency VND, no decimals, so 550000 means 550,000 VND). Page `108471317472449`. Instagram `17841432834644119`. Pixel `1000075088350707`. Business facts and targeting choices: memory note `tutoring-ads-facts`.

## Gates
- Show Hoang each ad change first. A "go" covers only what was shown.
- Publishing starts spending, so publish only on an explicit go, after he has seen the draft.
- Pause is reversible. Permanently deleting or discarding a draft is not: the discard tool lists what it removes, and Hoang must confirm that list.
- Do not use "Review and publish" in Ads Manager while unrelated drafts exist: it publishes all of them.

## Rules Meta enforces (each one cost us a failed attempt)
| Error | Meaning | What to do |
|---|---|---|
| 1885760 | Under a lowest-cost campaign, every ad set must use the same delivery goal | Choose one goal before building. To change it, build a new campaign |
| 1504040 | A published ad set's goal and attribution window are locked | Build a new campaign; do not try to edit it |
| 3858462 | Percentage spend limits need a total | Use fixed `daily_min_spend_target` and `daily_spend_cap` on each ad set, and set the percentages to 0 |
| 1885183 | The post was made by an app in Development mode | Hoang switches the app to Live (see below); no other route through the MCP |
| "link_data is missing link" on `source_ad_id` | A draft ad cannot be copied by its id | Make a new creative, or copy it in Ads Manager |
| `user_os` rejects "Mac OS X" | Value not accepted | Use "iOS" only, or leave it out |

## Delivery goal
Choose a goal the pixel can feed. Check `ads_get_dataset_stats` first: with no Purchase events, a Purchase goal sits on "Preparing" with no error at all. Use `LANDING_PAGE_VIEWS` until real purchases fire (REQ-0009), and read the ad set's `optimization_goal`, not its name: the old side A was named LPV but ran on Purchase.

Under `OUTCOME_SALES`, an LPV ad set still needs `promoted_object` `{"pixel_id":"1000075088350707","custom_event_type":"PURCHASE"}` and `destination_type` WEBSITE.

## Build order
1. Create the campaign. It stages as a draft. Check the returned spec: Meta may attach a `product_catalog_id` on its own. Clear it with `promoted_object: {}`, since a published catalog cannot be removed, and confirm it on read-back.
2. Create one ad set per side with identical targeting. Set both sides to half the budget with the fixed limits above.
3. Reuse existing creatives with `{"creative_id": "..."}` plus `source_ad_id`. These still work in Development mode.
4. New creatives use `placement_customizations`: 4:5 as the fallback, and 9:16 for Instagram `story`, `reels`, `ig_search`. There is no `url_tags` input, so put the UTM tags in `link_url`.
5. Read back with `object_state=draft`: every `active_errors` empty, right ad count per ad set, budget, goal, placements, no catalog.
6. Show the previews. On a go, publish with `ads_activate_entity` on the campaign, then confirm through a live read-back. "PUBLISHING" is not proof.

## Do not set for him
- `self_ai_disclosure`: Hoang's decision. On 4 Nov he chose the AI label on for the video ads.
- `targeting_automation.advantage_audience: 0`: only for a reason he states. Without it, age ranges are suggestions, not limits.

## AI extras
Hoang wants them off except Relevant comments, the Book now button and the AI label. New creatives come back with many extras opted in. The MCP refuses this change on ads with two media sizes, so the toggle must be done in Ads Manager. Check `advantage_plus_creative_enhancements` after creating, and tell him what is on.

## App in Development mode
App "Edlintics Ads Reporting" `3030719937268223` (Meta for Developers). Changing it to Live is a permission change, so Hoang does it himself, or says go first. It may ask for a privacy policy URL.

## After any change
Update hub `ads/latest` (the Ads tab reads it) and `status.md`. Delivery can take up to 24 hours after review, so read errors and delivery status before reaching a conclusion.
