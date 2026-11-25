# Buffer kontrolü

```
Kanal bağlı: sermenkreatif (679b445ca31978b79c5e06e4)
Instagram türleri: {'post': 'post', 'reel': 'reel', 'story': 'story'}
metadata.instagram alanları: firstComment: String, geolocation: InstagramGeolocationInput, isAiGenerated: Boolean, link: String, shouldShareToFeed: Boolean (ZORUNLU), stickerFields: InstagramStickerFieldsInput, type: PostType (ZORUNLU)
Hikaye bağlantı alanı: link
```

## 2026-11-25 gönderilerinin durumu

```
Sorulacak kayit: 6
  2026-11-25T09:10  6b065ec0608549ccf25e2f5e  urun/kurdele-vazo-silk-parlak-3d-baski|gonderi
  2026-11-25T09:50  6b065ec05d949f6c2a7038a6  urun/kurdele-vazo-silk-parlak-3d-baski|hikaye
  2026-11-25T12:10  6b065ec2b6204bca46c4db6b  urun/retro-drenajli-saksi-ic-mekan-bitki-saksisi|gonderi
  2026-11-25T12:50  6b065ec25d949f6c2a7038dd  urun/retro-drenajli-saksi-ic-mekan-bitki-saksisi|hikaye
  2026-11-25T17:24  6b065ec340e1d58d12f7dda9  urun/burgu-yilbasi-agaci-3d-baski-yilbasi-dekoru|gonderi
  2026-11-25T18:04  6b065ec322dfb7833a7afbc7  urun/burgu-yilbasi-agaci-3d-baski-yilbasi-dekoru|hikaye

--- Query alanlari ---
  account()
  assets(after, first, input)
  dailyPostingLimits(input)
  channel(input)
  channels(input)
  aggregatedPostMetrics(input)
  snippets(after, first, input)
  collaborationNotes(after, first, input)
  post(input)
  posts(after, first, input)
  contentItem(input)
  contentItems(after, first, input)
  tag(input)
  tagsV2(after, first, input)
  selectableTeamMembers(after, first, input)
  instagramAudio(input)
  searchInstagramAudio(input)
  trendingInstagramAudio(input)
  instagramAudioCatalog(input)
  searchInstagramAudioCatalog(input)
  configuration(input)
  postTemplate(input)
  postTemplates(after, first, input)
  ideaGroups(input)
  ideas(after, first, input)

--- Post alanlari --- 
  id, allowedActions, assets, author, channel, channelId, channelService, contentItemId, dueAt, error, externalLink, ideaId, isCustomScheduled, metadata, metrics, metricsUpdatedAt, notificationStatus, schedulingType, sentAt, sharedNow, shareMode, status, tags, text, via, createdAt, updatedAt

--- PostStatus alanlari --- 
  

--- PostError alanlari --- 
  

--- Gonderi durumlari (id, status, dueAt, sentAt, error, channelId, text) ---
  urun/kurdele-vazo-silk-parlak-3d-baski|gonderi -> SORGU HATASI: Buffer: Unknown argument "id" on field "Query.post".; Field "error" of type "PostPublishingError" must have a selection of subfields. Did you mean "error { ... }"?; Argument "Query.post(input:)" of type "PostInput!" is required, but it was not provided.
  urun/kurdele-vazo-silk-parlak-3d-baski|hikaye -> SORGU HATASI: Buffer: Unknown argument "id" on field "Query.post".; Field "error" of type "PostPublishingError" must have a selection of subfields. Did you mean "error { ... }"?; Argument "Query.post(input:)" of type "PostInput!" is required, but it was not provided.
  urun/retro-drenajli-saksi-ic-mekan-bitki-saksisi|gonderi -> SORGU HATASI: Buffer: Unknown argument "id" on field "Query.post".; Field "error" of type "PostPublishingError" must have a selection of subfields. Did you mean "error { ... }"?; Argument "Query.post(input:)" of type "PostInput!" is required, but it was not provided.
  urun/retro-drenajli-saksi-ic-mekan-bitki-saksisi|hikaye -> SORGU HATASI: Buffer: Unknown argument "id" on field "Query.post".; Field "error" of type "PostPublishingError" must have a selection of subfields. Did you mean "error { ... }"?; Argument "Query.post(input:)" of type "PostInput!" is required, but it was not provided.
  urun/burgu-yilbasi-agaci-3d-baski-yilbasi-dekoru|gonderi -> SORGU HATASI: Buffer: Unknown argument "id" on field "Query.post".; Field "error" of type "PostPublishingError" must have a selection of subfields. Did you mean "error { ... }"?; Argument "Query.post(input:)" of type "PostInput!" is required, but it was not provided.
  urun/burgu-yilbasi-agaci-3d-baski-yilbasi-dekoru|hikaye -> SORGU HATASI: Buffer: Unknown argument "id" on field "Query.post".; Field "error" of type "PostPublishingError" must have a selection of subfields. Did you mean "error { ... }"?; Argument "Query.post(input:)" of type "PostInput!" is required, but it was not provided.
```
