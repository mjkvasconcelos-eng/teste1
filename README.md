# Guia Natural & Natura

Aplicativo informativo para consulta de produtos naturais, suplementos, vitaminas, chás, ervas, cosméticos e produtos de cuidados pessoais.

> **Importante:** o aplicativo é exclusivamente informativo. Não diagnostica, não prescreve tratamentos e não substitui orientação médica, farmacêutica ou de outro profissional de saúde. Dados de produtos devem ser obtidos de fontes oficiais/confiáveis e revisados periodicamente.

## Stack inicial

- Firebase Authentication
- Cloud Firestore
- Firebase Security Rules
- Front-end preparado para integração com Firebase

## Perfis

- `user`: consulta produtos e usa favoritos/histórico.
- `editor`: cria e edita produtos, sem administrar configurações críticas.
- `admin`: administração completa.

## Estrutura

```text
firebase/
  firestore.rules
  firestore.indexes.json
src/
  firebase/
    config.example.js
  data/
    schema.md
README.md
.env.example
```

## Configuração do Firebase

1. Crie um projeto no Firebase Console.
2. Ative **Authentication > Sign-in method > Email/Password**.
3. Crie o banco **Cloud Firestore**.
4. Copie as configurações do seu app web para as variáveis do `.env`.
5. Nunca publique credenciais privadas, service accounts ou arquivos com secrets.
6. Publique as regras de `firebase/firestore.rules`.
7. Publique os índices de `firebase/firestore.indexes.json` quando necessários.

### Variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores do seu projeto Firebase.

As configurações públicas do Firebase Web podem ser usadas no cliente, mas o acesso aos dados deve ser protegido pelas Security Rules.

## Modelo de dados

### `users/{uid}`

```text
name: string
email: string
role: "user" | "editor" | "admin"
favorites: string[]
createdAt: timestamp
```

### `products/{productId}`

```text
name: string
brand: string
category: string
subcategory: string
description: string
purpose: string
usage: string
ingestion: string
ingestible: boolean
ingredients: string[]
contraindications: string
adverseReactions: string
warnings: string
targetAudience: string
imageUrl: string
sourceName: string
sourceUrl: string
sourceDate: timestamp
updatedAt: timestamp
status: "draft" | "review" | "published"
```

### Regra de ingestão

Produtos que não são destinados à ingestão devem usar `ingestible: false` e o aplicativo deve mostrar **“Não se aplica”** no campo de ingestão. Nunca inferir ingestão a partir de o produto ser “natural”.

## Perfis e segurança

As regras do Firestore usam o campo `users/{uid}.role` para autorizar operações. Usuários comuns podem ler apenas produtos publicados; editores podem criar/editar produtos; administradores possuem controle administrativo.

Em produção, recomenda-se que a atribuição inicial de `admin` seja feita por processo administrativo seguro, e não por uma tela pública.

## Próximos passos

1. Criar as telas de login/cadastro.
2. Criar a home e busca de produtos.
3. Implementar favoritos e histórico.
4. Implementar painel administrativo.
5. Integrar upload de imagens com Firebase Storage.
6. Adicionar auditoria de alterações e revisão das fontes.
7. Adicionar testes das regras de segurança.
