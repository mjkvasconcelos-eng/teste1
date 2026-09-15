# Guia Natural & Natura

Aplicativo informativo para consulta de produtos naturais, suplementos, vitaminas, chás, ervas, cosméticos e produtos de cuidados pessoais.

> **Importante:** o aplicativo é exclusivamente informativo. Não diagnostica, não prescreve tratamentos e não substitui orientação médica, farmacêutica ou de outro profissional de saúde. Dados de produtos devem ser obtidos de fontes oficiais/confiáveis e revisados periodicamente.

## Fase atual

A primeira versão será **aberta e sem tela de login**. O login, cadastro e controle de perfis ficarão preparados para uma etapa futura, quando o aplicativo precisar de favoritos sincronizados, painel administrativo e controle de usuários.

## Stack inicial

- Front-end web responsivo
- Cloud Firestore
- Firebase Security Rules preparada para a futura autenticação
- Firebase Authentication planejado para a próxima etapa

## Perfis futuros

- `user`: consulta produtos e usa favoritos/histórico.
- `editor`: cria e edita produtos, sem administrar configurações críticas.
- `admin`: administração completa.

## Estrutura

```text
firebase/
  firestore.rules
  firestore.indexes.json
src/
  data/
    schema.md
README.md
.env.example
```

## Configuração do Firebase

1. Crie um projeto no Firebase Console.
2. Crie o banco **Cloud Firestore**.
3. Publique as regras de `firebase/firestore.rules`.
4. Publique os índices de `firebase/firestore.indexes.json` quando necessários.
5. A autenticação será ativada em uma etapa futura.

### Variáveis de ambiente

O arquivo `.env.example` fica reservado para a futura integração do front-end com o Firebase.

Nunca publique credenciais privadas, service accounts ou arquivos com secrets.

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

## Segurança futura

As regras do Firestore já consideram os perfis `user`, `editor` e `admin`, mas a interface de autenticação ficará para uma etapa posterior. Quando o login for implementado, a atribuição inicial de `admin` deverá ser feita por processo administrativo seguro.

## Próximos passos

1. Criar a interface principal sem login.
2. Criar home e busca de produtos.
3. Criar categorias e página de detalhes.
4. Adicionar dados reais somente após revisão das fontes.
5. Depois implementar login/cadastro Firebase.
6. Implementar favoritos e histórico por usuário.
7. Implementar painel administrativo.
8. Integrar upload de imagens com Firebase Storage.
9. Adicionar auditoria de alterações e testes das regras.
