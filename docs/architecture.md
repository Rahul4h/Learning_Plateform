# Architecture Blueprint

## Product Summary

This project is an interactive article delivery platform. A reader opens an article, sees highlighted phrases, and clicks them to load related supporting content in a modal. The supporting content may be text, image, audio, or YouTube video. A right sidebar contains structured article sections such as introduction, detailed explanation, and additional resources.

## Core Domain Models

### Article

Represents the main learning content.

Recommended fields:

- `id`
- `title`
- `slug`
- `body`
- `body_format`
- `is_published`
- `created_at`
- `updated_at`

Notes:

- `body_format` can be `plain`, `html`, or `markdown`
- `slug` is useful for frontend URLs and admin readability

### Highlight

Represents a clickable phrase inside an article and the content it should open.

Recommended fields:

- `id`
- `article` (FK to `Article`)
- `label`
- `start_offset`
- `end_offset`
- `content_type`
- `title`
- `text_content`
- `media_url`
- `youtube_url`
- `sort_order`
- `created_at`

Notes:

- `label` is the displayed or matched phrase
- `start_offset` and `end_offset` avoid ambiguity when the same word appears more than once
- Keep content fields nullable because only one or two will be needed based on `content_type`

### Section

Represents expandable sidebar content for the article.

Recommended fields:

- `id`
- `article` (FK to `Article`)
- `title`
- `content`
- `sort_order`
- `created_at`

## Why This Design Is Better

- Avoids weak matching based only on a repeated word
- Keeps the API aligned with frontend behavior
- Supports future admin editing
- Makes modal rendering type-driven and predictable
- Keeps MVP simple without forcing a separate media table too early

## Recommended App Responsibilities

### `articles`

Owns article listing and article detail responses.

Files:

- `models.py`: article model
- `serializers.py`: article list/detail serializers
- `views.py`: list/detail API views
- `services.py`: composition helpers if article detail embeds related content

### `highlights`

Owns highlight validation and highlight API responses.

Files:

- `models.py`: highlight model and content-type validation
- `serializers.py`: highlight serializer
- `views.py`: article-specific highlight list API

### `sections`

Owns article sidebar content.

Files:

- `models.py`: section model
- `serializers.py`: section serializer
- `views.py`: article-specific section list API

### `common`

Shared enums or constants.

Files:

- `constants.py`: `BodyFormat` and `HighlightContentType`

## API Recommendation

### Option A: Split Endpoints

- `GET /api/articles/`
- `GET /api/articles/{id}/`
- `GET /api/articles/{id}/highlights/`
- `GET /api/articles/{id}/sections/`

Best when frontend loads pieces separately.

### Option B: Composed Article Detail

`GET /api/articles/{id}/`

Returns:

- article body
- highlights
- sections

Best for simpler frontend integration and fewer requests.

Recommended MVP: use both.

## Response Example

```json
{
  "id": 1,
  "title": "Climate and Bangladesh",
  "body": "Bangladesh faces multiple climate risks...",
  "body_format": "plain",
  "highlights": [
    {
      "id": 10,
      "label": "Bangladesh",
      "start_offset": 0,
      "end_offset": 10,
      "content_type": "image",
      "title": "Map of Bangladesh",
      "media_url": "https://cdn.example.com/images/bd-map.jpg"
    }
  ],
  "sections": [
    {
      "id": 50,
      "title": "Introduction",
      "content": "This section explains the article context.",
      "sort_order": 1
    }
  ]
}
```

## Frontend Interaction Flow

1. Frontend loads article detail
2. Frontend renders article text
3. Highlight metadata maps clickable spans or phrases
4. User clicks a highlight
5. Modal opens
6. Frontend switches renderer based on `content_type`
7. Sidebar sections render as accordion items

## Validation Rules

- `start_offset` must be less than `end_offset`
- highlight offsets must stay inside article body length
- for `text` type, require `text_content`
- for `image` or `audio`, require `media_url`
- for `youtube`, require `youtube_url`

## Security Notes

- Sanitize HTML if `body_format = html`
- Validate uploaded or stored media URLs
- Restrict unsafe embeds
- Prefer allowlisted domains for video embeds if needed

## Scale Notes

- Add `select_related("article")` for highlight and section queries
- Add indexes on `article_id` and `sort_order`
- Store media externally in production
- Add caching later only after measuring repeated access

## MVP First, Advanced Later

MVP:

- basic article CRUD through admin
- highlight click behavior
- modal content rendering
- sidebar sections

Advanced:

- markdown parsing
- precise text tokenization
- analytics on clicked highlights
- authoring UI for selecting highlight ranges
