import React, { useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const categories = ['Todos', 'Naturais', 'Suplementos', 'Chás e ervas', 'Natura', 'Cuidados pessoais'];

const products = [
  { id: 1, name: 'Chá de camomila', brand: 'Natural', category: 'Chás e ervas', emoji: '🌼', purpose: 'Tradicionalmente usado como bebida quente e relaxante.', usage: 'Preparar conforme as orientações da embalagem ou da fonte consultada.', ingestion: 'Produto destinado ao preparo de bebida.', adverse: 'Pode causar reações em pessoas sensíveis à camomila ou a plantas da mesma família.', warning: 'Confirme a origem e as orientações do produto antes do uso.' },
  { id: 2, name: 'Óleo essencial de lavanda', brand: 'Natural', category: 'Naturais', emoji: '🌿', purpose: 'Produto aromático usado em aplicações externas e aromáticas, conforme a apresentação.', usage: 'Seguir rigorosamente o rótulo. Não ingerir se a apresentação não for destinada ao uso oral.', ingestion: 'Não se aplica. Verifique o rótulo.', adverse: 'Pode causar irritação ou sensibilização em algumas pessoas.', warning: 'Óleos essenciais não devem ser ingeridos sem indicação específica do fabricante.' },
  { id: 3, name: 'Hidratante corporal', brand: 'Natura', category: 'Natura', emoji: '🧴', purpose: 'Cuidados e hidratação da pele.', usage: 'Aplicar sobre a pele conforme as instruções da embalagem.', ingestion: 'Não ingerir.', adverse: 'Pode ocorrer irritação ou sensibilidade individual.', warning: 'Uso externo. Evite contato com os olhos.' },
  { id: 4, name: 'Shampoo de cuidados capilares', brand: 'Natura', category: 'Cuidados pessoais', emoji: '🫧', purpose: 'Higiene e cuidados dos cabelos.', usage: 'Aplicar nos cabelos e couro cabeludo conforme o rótulo.', ingestion: 'Não ingerir.', adverse: 'Pode causar irritação em pessoas sensíveis aos ingredientes.', warning: 'Uso externo. Em caso de irritação, suspenda o uso.' },
  { id: 5, name: 'Suplemento vitamínico', brand: 'Exemplo', category: 'Suplementos', emoji: '💊', purpose: 'Complementação da alimentação quando o produto é autorizado e indicado para essa finalidade.', usage: 'Seguir exclusivamente a quantidade e frequência indicadas no rótulo.', ingestion: 'Somente se o produto for identificado como suplemento alimentar e destinado ao uso oral.', adverse: 'Reações variam conforme os ingredientes e a pessoa.', warning: 'Não é medicamento. Não exceda a recomendação do rótulo.' }
];

function App() {
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('Todos');
  const [selected, setSelected] = useState(null);
  const [favorites, setFavorites] = useState([]);

  const filtered = useMemo(() => products.filter(p => {
    const matchesCategory = category === 'Todos' || p.category === category;
    const text = `${p.name} ${p.brand} ${p.category}`.toLowerCase();
    return matchesCategory && text.includes(query.toLowerCase());
  }), [query, category]);

  const toggleFavorite = (id) => setFavorites(v => v.includes(id) ? v.filter(x => x !== id) : [...v, id]);

  if (selected) return <ProductDetails product={selected} favorite={favorites.includes(selected.id)} onFavorite={() => toggleFavorite(selected.id)} onBack={() => setSelected(null)} />;

  return (
    <div className="app">
      <header className="hero">
        <div className="brand"><div className="logo">🌿</div><div><strong>Guia Natural & Natura</strong><span>Informação simples para escolher melhor</span></div></div>
        <div className="heroText"><p className="eyebrow">GUIA DE PRODUTOS</p><h1>Encontre informações sobre o que você procura.</h1><p>Pesquise produtos naturais, suplementos e itens de cuidados pessoais em um só lugar.</p></div>
        <div className="search"><span>⌕</span><input value={query} onChange={e => setQuery(e.target.value)} placeholder="Buscar produto, marca ou categoria..." /></div>
      </header>

      <main>
        <section className="section"><div className="sectionHead"><h2>Categorias</h2><span>{filtered.length} produtos</span></div><div className="chips">{categories.map(c => <button key={c} className={category === c ? 'chip active' : 'chip'} onClick={() => setCategory(c)}>{c}</button>)}</div></section>

        <section className="section"><div className="sectionHead"><h2>Produtos</h2><span>Atualização informativa</span></div><div className="grid">{filtered.map(p => <article className="card" key={p.id} onClick={() => setSelected(p)}><div className="cardIcon">{p.emoji}</div><div className="cardBody"><small>{p.brand} · {p.category}</small><h3>{p.name}</h3><p>{p.purpose}</p><div className="cardFooter"><span>Ver detalhes</span><button onClick={e => { e.stopPropagation(); toggleFavorite(p.id); }} aria-label="Favoritar">{favorites.includes(p.id) ? '★' : '☆'}</button></div></div></article>)}</div>{filtered.length === 0 && <div className="empty">Nenhum produto encontrado. Tente outro termo.</div>}</section>

        <section className="notice"><div>ⓘ</div><p><strong>Informação importante</strong><br />Este aplicativo é informativo. Produtos naturais não são automaticamente seguros e cosméticos não devem ser ingeridos. Sempre confira o rótulo e a fonte oficial do produto.</p></section>
      </main>
      <footer>Guia Natural & Natura · Versão inicial · Login será adicionado futuramente.</footer>
    </div>
  );
}

function ProductDetails({ product, favorite, onFavorite, onBack }) {
  return <div className="app detailPage"><header className="detailHeader"><button className="back" onClick={onBack}>← Voltar</button><button className="fav" onClick={onFavorite}>{favorite ? '★ Favorito' : '☆ Favoritar'}</button></header><main><div className="detailHero"><div className="bigIcon">{product.emoji}</div><div><p className="eyebrow">{product.brand} · {product.category}</p><h1>{product.name}</h1><p>{product.purpose}</p></div></div><div className="detailGrid"><Info title="Para que serve" text={product.purpose} /><Info title="Modo de uso" text={product.usage} /><Info title="Ingestão" text={product.ingestion} /><Info title="Possíveis reações" text={product.adverse} /><Info title="Atenção" text={product.warning} /></div><div className="notice"><div>⚠</div><p><strong>Consulte a fonte e o rótulo.</strong><br />As informações desta tela são gerais e não substituem as orientações específicas do fabricante ou de um profissional habilitado.</p></div></main></div>;
}
function Info({ title, text }) { return <article className="info"><h3>{title}</h3><p>{text}</p></article>; }

createRoot(document.getElementById('root')).render(<App />);
