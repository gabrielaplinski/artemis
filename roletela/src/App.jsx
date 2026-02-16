import { useState, useEffect } from "react";
import { adicionarTitulo, listarTitulos, sortearTitulo } from "./services/api";

export default function App() {
  const [titulos, setTilulos] = useState([])
  const [sorteado, setSorteado] = useState(null)
  const [novoTitulo, setAdicionado] = useState("")
  const [novaPlataforma, setNovaPlataforma] = useState("")

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
    setTilulos(lista)
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
        <li><button className="bg-gray-700 px-5 py-2 rounded-lg hover:cursor-pointer" >Netflix</button></li>
        <li><button className="bg-gray-700 px-5 py-2 rounded-lg hover:cursor-pointer" >Crunchyroll</button></li>
        <li><button className="bg-gray-700 px-5 py-2 rounded-lg hover:cursor-pointer" >Disney+</button></li>
        <li><button className="bg-gray-700 px-5 py-2 rounded-lg hover:cursor-pointer" >GloboPlay</button></li>
        <li><button className="bg-gray-700 px-5 py-2 rounded-lg hover:cursor-pointer" >HBOMax</button></li>
        <li><button className="bg-gray-700 px-5 py-2 rounded-lg hover:cursor-pointer" >AppleTV</button></li>
        <li><button className="bg-gray-700 px-5 py-2 rounded-lg hover:cursor-pointer" >PrimeVideo</button></li>
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
