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
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-50">
      <h1 className="text-5xl font-bold mb-8">RoleTela</h1>
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
        <p className="mt-6 text-xl text-yellow-700" >
          {sorteado.plataforma}
        </p>
      )}

      <input type="text" value={novoTitulo} id="iNovoTitulo" onChange={(e) => setAdicionado(e.target.value)} placeholder="Novo título" />
      <select value={novaPlataforma} id="iNovaPlataforma" onChange={(e) => setNovaPlataforma(e.target.value)}>
        <option>Netflix</option>
        <option>Crunchyroll</option>
        <option>Disney+</option>
        <option>GloboPlay</option>
        <option>HBOMax</option>
        <option>AppleTV</option>
        <option>PrimeVideo</option>
      </select>
      <button onClick={adicionar}>Adicionar</button>

      <ul>
        {titulos.map((titulo, index) => (
          <li key={index}>
            {titulo.id} - {titulo.titulo} — {titulo.plataforma}
          </li>
        ))}
      </ul>
    </div>
  )
};
