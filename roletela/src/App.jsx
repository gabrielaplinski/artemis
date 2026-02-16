import { useState, useEffect } from "react";
import { adicionarTitulo, listarTitulos, sortearTitulo } from "./services/api";

export default function App() {
  const [titulos, setTitulos] = useState([])
  const [sorteado, setSorteado] = useState(null)
  const [novoTitulo, setAdicionado] = useState("")
  const [novaPlataforma, setNovaPlataforma] = useState("")
  const [filtroAtivo, setFiltroAtivo] = useState(null)

  useEffect(() => {
  buscarLista()
  }, [])

  async function sortear() {
    const escolhido = await sortearTitulo()
    setSorteado(escolhido)    
  }

  async function adicionar() {
    await adicionarTitulo(novoTitulo, novaPlataforma)
    await buscarLista()
    setAdicionado("")    
  }

  async function buscarLista() {
    const lista = await listarTitulos()
    setTitulos(lista)
  }

  async function filtrar(plataforma) {
    if (plataforma === filtroAtivo) {
      setFiltroAtivo(null)
      await buscarLista()
    } else {
      setFiltroAtivo(plataforma)
      const lista = await filtrarTitulos(plataforma)
      setTitulos(lista)
    }
  }

  function BotaoPlataforma({ nome, onClick}) {
    return (
      <li>
        <button onClick={onClick} className="...">{nome}</button>
      </li>
    )
  }

  return (
    <div className="bg-gray-900 text-white p-50 flex flex-wrap items-center justify-center">
      <h1 className="text-5xl text-center font-bold mb-20 w-full">RoleTela</h1>
      <nav className="mb-10 w-full flex flex-row justify-between" >
        <div className="columns-2" >
          <button
            onClick={sortear}
            className="bg-red-800 hover:bg-red-600 hover:cursor-pointer active:bg-red-500 text-white font-semibold px-6 py-1 rounded-lg transition-colors"
          >
            Sortear
          </button>
          {sorteado && (
            <p className="mt-6 text-xl text-yellow-700" >
              {sorteado.titulo}
            </p>
          )}
          {sorteado && (
            <p className="mt-2 mb-10 text-xl text-yellow-700" >
              {sorteado.plataforma}
            </p>
          )}
        </div>
        <div className="flex items-center justify-center gap-5" >
          <input type="text" value={novoTitulo} id="iNovoTitulo" onChange={(e) => setAdicionado(e.target.value)} placeholder="Novo título" className="border" />
          <select value={novaPlataforma} id="iNovaPlataforma" onChange={(e) => setNovaPlataforma(e.target.value)}>
            <option>Netflix</option>
            <option>Crunchyroll</option>
            <option>Disney+</option>
            <option>GloboPlay</option>
            <option>HBOMax</option>
            <option>AppleTV</option>
            <option>PrimeVideo</option>
          </select>
          <button onClick={adicionar} className="bg-green-600 font-semibold px-3 rounded-lg hover:cursor-pointer transition-colours" >Adicionar</button>
        </div>
      </nav>

      <ul className="w-full flex flex-row gap-5 justify-center" >
        <BotaoPlataforma nome="Netflix" onClick={ () => filtrar("Netflix")} />
        <BotaoPlataforma nome="Crunchyroll" onClick={ () => filtrar("Crunchyroll")} />
        <BotaoPlataforma nome="Disney+" onClick={ () => filtrar("Disney")} />
        <BotaoPlataforma nome="GloboPlay" onClick={ () => filtrar("GloboPlay")} />
        <BotaoPlataforma nome="HBOMax" onClick={ () => filtrar("HBOMax")} />
        <BotaoPlataforma nome="AppleTV" onClick={ () => filtrar("AppleTV")} />
        <BotaoPlataforma nome="PrimeVideo" onClick={ () => filtrar("PrimeVideo")} />
      </ul>

      <ul className="pt-30 flex flex-wrap gap-6 items-center justify-center" >
        {titulos.map((titulo, index) => (
          <li key={index} className="basis-md" >
            {titulo.id} - {titulo.titulo} — {titulo.plataforma}
            <input type="checkbox" id="iAssistido" />
          </li>
        ))}
      </ul>
    </div>
  )
};
