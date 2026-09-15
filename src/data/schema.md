# Modelo Firestore

## users/{uid}

- `name`: string
- `email`: string
- `role`: `user | editor | admin`
- `favorites`: array de IDs de produtos
- `createdAt`: timestamp

## products/{productId}

- `name`: string
- `brand`: string
- `category`: string
- `subcategory`: string
- `description`: string
- `purpose`: string
- `usage`: string
- `ingestion`: string
- `ingestible`: boolean
- `ingredients`: array de strings
- `contraindications`: string
- `adverseReactions`: string
- `warnings`: string
- `targetAudience`: string
- `imageUrl`: string
- `sourceName`: string
- `sourceUrl`: string
- `sourceDate`: timestamp
- `updatedAt`: timestamp
- `status`: `draft | review | published`

## categories/{categoryId}

- `name`: string
- `description`: string
- `imageUrl`: string
- `active`: boolean
