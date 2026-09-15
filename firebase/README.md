# Firebase — Guia Natural & Natura

Projeto Firebase: `natura-a22fe`

## Firestore

Coleção principal: `products`

Campos recomendados:

- `name`
- `brand`
- `category`
- `description`
- `purpose`
- `usage`
- `ingestion`
- `ingestible` (boolean)
- `ingredients` (array)
- `contraindications`
- `adverseReactions`
- `targetAudience`
- `warnings`
- `imageUrl`
- `source`
- `sourceUrl`
- `updatedAt`
- `status` (`draft` ou `published`)

Coleção `categories`:

- `name`
- `description`
- `active`
- `order`

Coleção `users`:

- `role`: `admin` ou `editor`
- `displayName`
- `email`

## Segurança

As regras de `firestore.rules` permitem consulta pública somente para produtos com `status == "published"`. Cadastro e edição exigem usuário autenticado com função `editor` ou `admin`; exclusão exige `admin`.

## Próximo passo no Firebase Console

1. Ative o Firestore Database.
2. Ative Authentication > Sign-in method > Email/Password quando a área administrativa for liberada.
3. Publique `firebase/firestore.rules`.
4. Crie um documento em `users` com o UID do administrador e `role: "admin"`.
5. Depois, a interface administrativa poderá cadastrar e editar os produtos.

A configuração Web fica em `firebase/firebase-config.js`.
