# Buffer kontrolü

```
Kanal bağlı: sermenkreatif (679b445ca31978b79c5e06e4)
Instagram türleri: {'post': 'post', 'reel': 'reel', 'story': 'story'}
metadata.instagram alanları: firstComment: String, geolocation: InstagramGeolocationInput, isAiGenerated: Boolean, link: String, shouldShareToFeed: Boolean (ZORUNLU), stickerFields: InstagramStickerFieldsInput, type: PostType (ZORUNLU)
Hikaye bağlantı alanı: link
```

## 2026-11-26 gönderilerinin durumu

```
Sorulacak kayit: 6
  2026-11-26T12:38  6b074977bffb0dd07330e887  urun/cizgi-sanati-susler-yilbasi-agaci-susu|gonderi
  2026-11-26T17:24  6b074978209be591e2df6b62  urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski|gonderi
  2026-11-26T00:45  6b0755bbb8e2338b856567d8  urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti|gonderi
  2026-11-26T01:04  6b075a5da791bea1b22d20ec  urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti|hikaye
  2026-11-26T13:18  6b075c92b96dd8d351671ec5  urun/cizgi-sanati-susler-yilbasi-agaci-susu|hikaye
  2026-11-26T18:04  6b075c93a791bea1b22e954f  urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski|hikaye

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

--- Asset alanlari ---
  id, mimeType, source, status, thumbnail, type

--- Gonderi durumlari ---
  urun/cizgi-sanati-susler-yilbasi-agaci-susu|gonderi
    {"id": "6b074977bffb0dd07330e887", "status": "scheduled", "dueAt": "2026-11-26T09:38:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": null, "assets": [{"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-1.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-1.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-2.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-2.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-3.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-3.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-4.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-4.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-5.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-5.jpg", "type": "image"}]}
  urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski|gonderi
    {"id": "6b074978209be591e2df6b62", "status": "scheduled", "dueAt": "2026-11-26T14:24:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": null, "assets": [{"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-1.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-1.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-2.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-2.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-3.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-3.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-4.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-4.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-5.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-5.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-6.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-6.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-7.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-7.jpg", "type": "image"}, {"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-8.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/678b7c63059ccaa03b8bf7012788a3f7635987c3/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-8.jpg", "type": "image"}]}
  urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti|gonderi
    {"id": "6b0755bbb8e2338b856567d8", "status": "sent", "dueAt": "2026-11-25T21:45:00.000Z", "sentAt": "2026-11-25T21:45:45.816Z", "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": null, "assets": [{"id": "17976315813173761", "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-1.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-1.jpg", "type": "image"}, {"id": "17976315912173761", "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-2.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-2.jpg", "type": "image"}, {"id": "17976315930173761", "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-3.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-3.jpg", "type": "image"}, {"id": "17976315951173761", "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-4.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-4.jpg", "type": "image"}, {"id": "17976315969173761", "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-5.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-5.jpg", "type": "image"}, {"id": "17976315987173761", "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-6.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/0bbd22fe81d7099e024b85425b1129e52a96a8e2/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-6.jpg", "type": "image"}]}
  urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti|hikaye
    {"id": "6b075a5da791bea1b22d20ec", "status": "sent", "dueAt": "2026-11-25T22:04:00.000Z", "sentAt": "2026-11-25T22:04:53.777Z", "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": null, "assets": [{"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/2587ec2217d28ee7666ce38b8f6708a04eeb8d30/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-1.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/2587ec2217d28ee7666ce38b8f6708a04eeb8d30/gorsel/urun/vidali-yapim-tahtasi-tornavidali-sok-tak-egitici-oyuncak-seti-1.jpg", "type": "image"}]}
  urun/cizgi-sanati-susler-yilbasi-agaci-susu|hikaye
    {"id": "6b075c92b96dd8d351671ec5", "status": "scheduled", "dueAt": "2026-11-26T10:18:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": null, "assets": [{"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/364723950a5a49f400d9016f3212038a09e0d4c1/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-1.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/364723950a5a49f400d9016f3212038a09e0d4c1/gorsel/urun/cizgi-sanati-susler-yilbasi-agaci-susu-1.jpg", "type": "image"}]}
  urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski|hikaye
    {"id": "6b075c93a791bea1b22e954f", "status": "scheduled", "dueAt": "2026-11-26T15:04:00.000Z", "sentAt": null, "notificationStatus": null, "schedulingType": "automatic", "sharedNow": false, "shareMode": "customScheduled", "channelId": "679b445ca31978b79c5e06e4", "error": null, "assets": [{"id": null, "mimeType": "image/jpeg", "source": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/364723950a5a49f400d9016f3212038a09e0d4c1/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-1.jpg", "thumbnail": "https://raw.githubusercontent.com/sedatisc/instagram-gorseller/364723950a5a49f400d9016f3212038a09e0d4c1/gorsel/urun/6-bolmeli-tezgah-duzenleyici-silk-parlak-3d-baski-1.jpg", "type": "image"}]}
```
