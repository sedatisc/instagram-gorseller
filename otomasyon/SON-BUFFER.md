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

--- PostInput alanlari ---
  id

--- PostPublishingError alanlari ---
  message, rawError, supportUrl

--- Gonderi durumlari ---
  urun/kurdele-vazo-silk-parlak-3d-baski|gonderi
    {"id": "6b065ec0608549ccf25e2f5e", "status": "error", "dueAt": "2026-11-25T06:10:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": {"message": "An unknown error has occurred. Please retry the post again, and get in touch if this persists.", "rawError": "Failed to create media container for instagram: Timeout: Failed to create Instagram media: Request failed with status code 400: It takes too long to download the media.", "supportUrl": null}}
  urun/kurdele-vazo-silk-parlak-3d-baski|hikaye
    {"id": "6b065ec05d949f6c2a7038a6", "status": "error", "dueAt": "2026-11-25T06:50:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": {"message": "An unknown error has occurred. Please retry the post again, and get in touch if this persists.", "rawError": "Failed to create media container for instagram: Timeout: Failed to create Instagram media: Request failed with status code 400: It takes too long to download the media.", "supportUrl": null}}
  urun/retro-drenajli-saksi-ic-mekan-bitki-saksisi|gonderi
    {"id": "6b065ec2b6204bca46c4db6b", "status": "error", "dueAt": "2026-11-25T09:10:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": {"message": "An unknown error has occurred. Please retry the post again, and get in touch if this persists.", "rawError": "Failed to create media container for instagram: Timeout: Failed to create Instagram media: Request failed with status code 400: It takes too long to download the media.", "supportUrl": null}}
  urun/retro-drenajli-saksi-ic-mekan-bitki-saksisi|hikaye
    {"id": "6b065ec25d949f6c2a7038dd", "status": "error", "dueAt": "2026-11-25T09:50:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": {"message": "There is an issue with the media included. Please remove it and try to upload it again.", "rawError": "Failed to create media container for instagram: Only photo or video can be accepted as media type.: Failed to create Instagram media: Request failed with status code 400: The media could not be fetched from this URI: https://sermenkreatif.com/media/urun/a281256d-d617-48f4-8abb-a910b2098766.webp.Please check the limitations section in our development document for more information: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media#creating", "supportUrl": null}}
  urun/burgu-yilbasi-agaci-3d-baski-yilbasi-dekoru|gonderi
    {"id": "6b065ec340e1d58d12f7dda9", "status": "error", "dueAt": "2026-11-25T14:24:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": {"message": "An unknown error has occurred. Please retry the post again, and get in touch if this persists.", "rawError": "Failed to create media container for instagram: Timeout: Failed to create Instagram media: Request failed with status code 400: It takes too long to download the media.", "supportUrl": null}}
  urun/burgu-yilbasi-agaci-3d-baski-yilbasi-dekoru|hikaye
    {"id": "6b065ec322dfb7833a7afbc7", "status": "error", "dueAt": "2026-11-25T15:04:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": {"message": "An unknown error has occurred. Please retry the post again, and get in touch if this persists.", "rawError": "Failed to create media container for instagram: Timeout: Failed to create Instagram media: Request failed with status code 400: It takes too long to download the media.", "supportUrl": null}}
```
